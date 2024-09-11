""" HDFS client module """

from hdfs import InsecureClient
import os

# Get host from environment variable
HDFS_HOST = os.getenv("HDFS_HOST", "http://namenode:9870")
HDFS_USER_NAME = os.getenv("HDFS_USER_NAME", "root")


def get_hdfs_client(
    url: str = HDFS_HOST, username: str = HDFS_USER_NAME
) -> InsecureClient:
    """Get an HDFS client"""
    return InsecureClient(url=url, user=username)
