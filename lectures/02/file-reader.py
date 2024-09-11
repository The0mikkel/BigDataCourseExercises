from client import get_hdfs_client


def main(filename):
    print("Reading contents of file:")
    with client.read("/" + filename, encoding="utf-8", delimiter="\n") as reader:
        for line in reader:
            print(line)


if __name__ == "__main__":
    client = get_hdfs_client()
    print("Listing contents of the HDFS root directory:")
    print(client.list("/"))
    
    # Get filename from input
    filename = input("Enter filename to read: ")
    
    main(filename)
