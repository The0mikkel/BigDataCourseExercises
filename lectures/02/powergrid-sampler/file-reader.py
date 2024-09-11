import pandas as pd

from hdfs_client import get_hdfs_client

def read(filename):
    print("Reading contents of file:")
    with client.read("/" + filename, encoding="utf-8", delimiter="\n") as reader:
        for line in reader:
            print(line)
            
def read_parquet(filename):
    print("Reading contents of file:")
    with client.read("/" + filename, encoding="utf-8", delimiter="\n") as reader:
        df = pd.read_parquet("/" + filename)
        print(df)
        
def read_parquet_folder(folder):
    print("Reading contents of folder:")
    df = pd.read_parquet("/" + folder)
    print(df)

def delete(filename):
    print("Deleting file: " + filename)
    client.delete("/" + filename)

if __name__ == "__main__":
    client = get_hdfs_client()
    print("Listing contents of the HDFS root directory:")
    print(client.list("/"))
    
    # Get filename from input
    filename = input("Enter filename to read: ")
    print("")
    
    # Get action from input
    print("Available actions: read, read_parquet, read_parquet_folder, delete")
    action = input("Enter action to perform: ")
    
    if action == "read":
        read(filename)
    elif action == "read_parquet":
        read_parquet(filename)
    elif action == "read_parquet_folder":
        read_parquet_folder(filename)
    elif action == "delete":
        delete(filename)
