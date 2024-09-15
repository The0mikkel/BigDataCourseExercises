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
            
    def append(self, hdfs_path, data: SensorData):
        try:
            with self.reader(hdfs_path, encoding="utf-8") as reader:
                df = pd.DataFrame.from_dict(data.toObject(), orient="index").transpose()
                df.to_parquet(hdfs_path, engine='fastparquet', append=True)

                self.client.upload(hdfs_path, hdfs_path, overwrite=True)
        except:
            print("File not found, creating new file.")
            self.write(hdfs_path, data)

    def write(self, hdfs_path, data: SensorData, overwrite=True):
        # Check path exists on local client
        with self.reader(hdfs_path, encoding="utf-8") as reader:
            path = hdfs_path.split("/")
            path.pop()
            hdfs_dir = "/".join(path)
            if not os.path.exists(hdfs_dir):
                os.makedirs(hdfs_dir)
            
            df = pd.DataFrame.from_dict(data.toObject(), orient="index").transpose()
            df.to_parquet(hdfs_path)

            self.client.upload(hdfs_path, hdfs_path, overwrite)
