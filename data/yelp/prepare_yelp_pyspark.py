from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower
import os
from pathlib import Path


# Initialize Spark
spark = SparkSession.builder \
    .appName("Yelp Preprocessing") \
    .getOrCreate()


BASE_DIR = Path(__file__).parent.resolve()
BUSINESS_PATH = BASE_DIR / "../../yelp_data/yelp_academic_dataset_business.json"
REVIEW_PATH = BASE_DIR / "../../yelp_data/yelp_academic_dataset_review.json"
OUTPUT_PATH = BASE_DIR / "filtered_yelp_reviews.parquet"

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Categories we care about
categories_of_interest = ["restaurant", "bar", "hotel", "nightlife", "attraction", "cafe", "museum"]

# Load JSON files
print("🚀 Loading business.json...")
business_df = spark.read.json(BUSINESS_PATH)

print("🚀 Loading review.json...")
review_df = spark.read.json(REVIEW_PATH)

# Filter businesses based on category
print("🔍 Filtering categories...")
filtered_business = business_df.filter(
    lower(col("categories")).rlike("|".join(categories_of_interest))
).select(
    "business_id", "name", "city", "latitude", "longitude", "stars", "review_count", "categories"
)

# Limit review length and filter to avoid NULLs
print("🧹 Filtering and truncating reviews...")
filtered_reviews = review_df.select(
    "business_id", "text", "stars", "date"
).filter(
    (col("text").isNotNull()) & (col("stars").isNotNull())
).withColumn(
    "review_text", col("text").substr(1, 700)
).select(
    "business_id", "review_text", col("stars").alias("review_stars"), "date"
)

# Join business + reviews
print("🔗 Joining...")
joined_df = filtered_reviews.join(filtered_business, on="business_id", how="inner")

# Final schema
final_df = joined_df.select(
    "business_id", "name", "city", "latitude", "longitude",
    "review_text", "review_stars", "categories"
)

# Save as Parquet
print(f"💾 Saving output to: {OUTPUT_PATH}")
final_df.write.mode("overwrite").parquet(OUTPUT_PATH)
print(f"✅ Parquet saved to: {OUTPUT_PATH}")
print("✅ Done! Ready for FAISS/Gemini pipeline.")
