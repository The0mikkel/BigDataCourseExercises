from hdfs_client import get_hdfs_client
from data import SensorData
import os

import pandas as pd

class Client:
    def __init__(self):
        self.client = get_hdfs_client()

    def reader(self, hdfs_path, encoding="utf-8"):
        return self.client.read(hdfs_path, encoding=encoding)

    def read(self, hdfs_path):
        with self.reader(hdfs_path) as reader:
            return pd.read_parquet(reader)
        
    def read_all(self, hdfs_path):
        # Read all in subdirectories
        files = self.get_files(hdfs_path)
        dfs = []
        for file in files:
            print("Reading file: " + file)
            dfs.append(self.read(file))
            
        return pd.concat(dfs)
    
    def get_files(self, hdfs_path):
        # Get all files recursively in subdirectories
        files = self.client.list(hdfs_path, status=True)
        filenames = []
        for file in files:
            # If file does not have a "." in the name, it is a directory
            filename = file[0]
            if "." not in filename:
                filenames += self.get_files(hdfs_path + "/" + filename + "/")
            else:
                filenames.append(hdfs_path + "/" + filename)
                
        return filenames

            
    def append(self, hdfs_path, data: SensorData):
        try:
            df = pd.DataFrame.from_dict(data.toObject(), orient="index").transpose()
            df.to_parquet(hdfs_path, engine='fastparquet', append=True)

            self.client.upload(hdfs_path, hdfs_path, overwrite=True)
        except:
            print("File not found, creating new file.")
            self.write(hdfs_path, data)

    def write(self, hdfs_path, data: SensorData, overwrite=True):
        # Check path exists on local client   
        path = hdfs_path.split("/")
        path.pop()
        hdfs_dir = "/".join(path)
        if not os.path.exists(hdfs_dir):
            os.makedirs(hdfs_dir)
        
        df = pd.DataFrame.from_dict(data.toObject(), orient="index").transpose()
        df.to_parquet(hdfs_path)

        self.client.upload(hdfs_path, hdfs_path, overwrite)
