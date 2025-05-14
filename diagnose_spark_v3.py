
import os
import platform
import subprocess
from pathlib import Path

def print_section(title):
    print(f"\n=== {title} ===")

def check_env():
    print_section("Environment Variables")
    print(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Python: {platform.python_version()}")
    print(f"JAVA_HOME: {os.environ.get('JAVA_HOME', '❌ NOT SET')}")
    print(f"HADOOP_HOME: {os.environ.get('HADOOP_HOME', '❌ NOT SET')}")
    print(f"SPARK_HOME: {os.environ.get('SPARK_HOME', '❌ NOT SET')}")
    print(f"PYSPARK_PYTHON: {os.environ.get('PYSPARK_PYTHON', '❌ NOT SET')}")
    print(f"PATH contains JAVA_HOME/bin: {'java' in os.environ.get('PATH', '').lower()}")
    print(f"PATH contains Hadoop bin: {'hadoop' in os.environ.get('PATH', '').lower()}")

def check_executables():
    print_section("Executable Availability")
    for cmd in ['java', 'python', 'winutils', 'spark-submit']:
        try:
            result = subprocess.run(["where", cmd], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"✅ {cmd}: {result.stdout.strip()}")
            else:
                print(f"❌ {cmd} not found in PATH")
        except Exception as e:
            print(f"❌ Error checking {cmd}: {e}")

def check_java_version():
    print_section("Java Version")
    try:
        result = subprocess.run(["java", "-version"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        print(result.stderr or result.stdout)
    except Exception as e:
        print(f"❌ java -version failed: {e}")

def check_winutils():
    print_section("winutils Test")
    try:
        result = subprocess.run(["winutils", "ls", "C:\\"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        print(result.stdout or result.stderr)
    except Exception as e:
        print(f"❌ winutils.exe failed: {e}")

def check_spark_session():
    print_section("SparkSession Test")
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName("DiagnoseTest").getOrCreate()
        spark.range(5).show()
        spark.stop()
        print("✅ SparkSession started successfully.")
    except Exception as e:
        print(f"❌ SparkSession failed: {e}")

if __name__ == "__main__":
    check_env()
    check_executables()
    check_java_version()
    check_winutils()
    check_spark_session()
