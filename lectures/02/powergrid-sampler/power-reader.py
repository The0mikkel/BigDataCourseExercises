import pandas as pd

from hdfs_client import get_hdfs_client

powergridFolder = "/powergrid/elecricity_lines/wattage_offset/"

def read_parquet_folder(folder):
    return pd.read_parquet("/" + folder)
    
if __name__ == "__main__":
    client = get_hdfs_client()
    print(f"Listing contents of the HDFS \"{powergridFolder}\" directory:")
    
    df = read_parquet_folder(powergridFolder)
    
    # Sort data
    df = df.sort_values(by=["created_at", "sensor_id", "correlation_id"])
    
    # Pretty print
    print(df)
    