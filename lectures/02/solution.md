# Solution

## Exercise 1

Run setup specified in [/services/hdfs/README.md](../../services/hdfs/README.md).

Result:

```
NAME             READY   STATUS    RESTARTS   AGE
pod/datanode-0   1/1     Running   0          5m45s
pod/datanode-1   1/1     Running   0          5m35s
pod/datanode-2   1/1     Running   0          5m20s
pod/namenode-0   1/1     Running   0          6m50s

NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
service/datanode   ClusterIP   10.152.183.32    <none>        9864/TCP            5m45s
service/namenode   ClusterIP   10.152.183.115   <none>        9870/TCP,9000/TCP   6m50s

NAME                        READY   AGE
statefulset.apps/datanode   3/3     5m45s
statefulset.apps/namenode   1/1     6m50s
```

## Exercise 2

### Task 1

```bash
kubectl run interactive --rm -i --tty --image apache/hadoop:3 -- /bin/bash
```

### Task 2

Command:  
```bash
hdfs dfs -ls /
```

Output:  
```
bash-4.2$ hdfs dfs -ls /
Found 20 items
-rw-r--r--   1 root   root      12082 2019-03-05 17:36 /anaconda-post.log
dr-xr-xr-x   - root   root       4096 2019-05-16 14:58 /bin
drwxr-xrwx   - root   root       4096 2024-09-09 13:15 /data
drwxr-xr-x   - root   root        380 2024-09-09 13:15 /dev
drwxr-xr-x   - root   root       4096 2024-09-09 13:15 /etc
drwxr-xr-x   - root   root       4096 2018-04-11 04:59 /home
dr-xr-xr-x   - root   root       4096 2019-05-16 14:55 /lib
dr-xr-xr-x   - root   root       4096 2019-05-16 14:58 /lib64
drwxr-xr-x   - root   root       4096 2018-04-11 04:59 /media
drwxr-xr-x   - root   root       4096 2018-04-11 04:59 /mnt
drwxr-xr-x   - hadoop root       4096 2024-09-09 13:15 /opt
dr-xr-xr-x   - root   root          0 2024-09-09 13:15 /proc
dr-xr-x---   - root   root       4096 2019-05-16 14:58 /root
drwxr-xr-x   - root   root       4096 2024-09-09 13:15 /run
dr-xr-xr-x   - root   root       4096 2019-05-16 14:57 /sbin
drwxr-xr-x   - root   root       4096 2018-04-11 04:59 /srv
dr-xr-xr-x   - root   root          0 2024-09-09 13:15 /sys
drwxrwxrwt   - root   root       4096 2024-09-09 13:16 /tmp
drwxr-xr-x   - root   root       4096 2019-03-05 17:34 /usr
drwxr-xr-x   - root   root       4096 2019-03-05 17:34 /var
```

Command:
```bash
ls -laL /
```

Output:
```
bash-4.2$ ls -laL /
total 84
drwxr-xr-x    1 root   root  4096 Sep  9 13:15 .
drwxr-xr-x    1 root   root  4096 Sep  9 13:15 ..
-rw-r--r--    1 root   root 12082 Mar  5  2019 anaconda-post.log
dr-xr-xr-x    1 root   root  4096 May 16  2019 bin
drwxr-xrwx    2 root   root  4096 Sep  9 13:15 data
drwxr-xr-x    5 root   root   380 Sep  9 13:15 dev
drwxr-xr-x    1 root   root  4096 Sep  9 13:15 etc
drwxr-xr-x    2 root   root  4096 Apr 11  2018 home
dr-xr-xr-x    1 root   root  4096 May 16  2019 lib
dr-xr-xr-x    1 root   root  4096 May 16  2019 lib64
drwxr-xr-x    2 root   root  4096 Apr 11  2018 media
drwxr-xr-x    2 root   root  4096 Apr 11  2018 mnt
drwxr-xr-x    1 hadoop root  4096 Sep  9 13:15 opt
dr-xr-xr-x 3736 root   root     0 Sep  9 13:15 proc
dr-xr-x---    1 root   root  4096 May 16  2019 root
drwxr-xr-x    1 root   root  4096 Sep  9 13:15 run
dr-xr-xr-x    1 root   root  4096 May 16  2019 sbin
drwxr-xr-x    2 root   root  4096 Apr 11  2018 srv
dr-xr-xr-x   13 root   root     0 Sep  9 13:15 sys
drwxrwxrwt    1 root   root  4096 Sep  9 13:16 tmp
drwxr-xr-x    1 root   root  4096 Mar  5  2019 usr
drwxr-xr-x    1 root   root  4096 Mar  5  2019 var
```

Command:
```bash
export HADOOP_USER_NAME=root
hdfs dfs -fs hdfs://namenode:9000 -ls /
```

Output:
```
bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -ls /
bash-4.2$
```
*Please note, that this command takes a while to execute.*

### Task 3

Command:
```bash
hdfs dfs -fs hdfs://namenode:9000 -ls /
```

Output:
```
bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -ls /
bash-4.2$
```

### Task 4

Command:
```bash
echo "Hello World" > test.txt
```

Output:
```bash
bash-4.2$ echo "Hello World" > test.txt
bash-4.2$ ls | grep "test.txt"
test.txt
bash-4.2$ cat test.txt
Hello World
```

### Task 5

Command:
```bash
hdfs dfs -fs hdfs://namenode:9000 -put test.txt /test.txt
```

Output:
```
bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -put test.txt /test.txt
bash-4.2$
```

Command:
```bash
hdfs dfs -fs hdfs://namenode:9000 -ls /
```

Output:
```
bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -ls /
Found 1 items
-rw-r--r--   3 root supergroup         12 2024-09-09 13:25 /test.txt
```

### Task 6

Command:
```bash
hdfs dfs -fs hdfs://namenode:9000 -cat /test.txt
```

Output:
```
bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -cat /test.txt
Hello World
```

### Task 7

Command:
```bash
hdfs dfs -fs hdfs://namenode:9000 -rm /test.txt
```

Output:
```
bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -rm /test.txt
Deleted /test.txt
```

## Exercise 3

*Continue from the previous exercise, in terms of interactive container.*

### Task 1

Command:
```bash
wget -O alice-in-wonderland.txt https://www.gutenberg.org/files/11/11-0.txt
hdfs dfs -fs hdfs://namenode:9000 -put alice-in-wonderland.txt /alice-in-wonderland.txt
```

Output:
```
bash-4.2$ wget -O alice-in-wonderland.txt https://www.gutenberg.org/files/11/11-0.txt
s dfs -fs hdfs://name--2024-09-09 13:40:46--  https://www.gutenberg.org/files/11/11-0.txt
node:9000 -put alice-in-wonderland.txt /alice-in-wonderland.txtResolving www.gutenberg.org (www.gutenberg.org)... 152.19.134.47, 2610:28:3090:3000:0:bad:cafe:47
Connecting to www.gutenberg.org (www.gutenberg.org)|152.19.134.47|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 154638 (151K) [text/plain]
Saving to: 'alice-in-wonderland.txt'

100%[=============================================>] 154,638      657KB/s   in 0.2s   

2024-09-09 13:40:47 (657 KB/s) - 'alice-in-wonderland.txt' saved [154638/154638]

bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -put alice-in-wonderland.txt /alice-in-wonderland.txt
bash-4.2$
```

Command:
```bash
hdfs dfs -fs hdfs://namenode:9000 -ls /
```

Output:
```
bash-4.2$ hdfs dfs -fs hdfs://namenode:9000 -ls /
Found 1 items
-rw-r--r--   3 root supergroup     154638 2024-09-09 13:41 /alice-in-wonderland.txt
bash-4.2$
```

## Exercise 4

Apply the config map and deploy interactive pod (with attached storage) through [hdfs-cli.yaml file](../../services/hdfs/hdfs-cli.yaml) in [/services/hdfs/](../../services/hdfs/). 

Command:
```bash
kubectl apply -f hdfs-cli.yaml
```

Output:
```
kubectl apply -f hdfs-cli.yaml
configmap/hdfs-config created
pod/hdfs-cli created
```

Connect to the interactive pod:

Command:
```bash
kubectl exec -it hdfs-cli -- /bin/bash
```

We can now ditch the `-fs hdfs://namenode:9000` part of the commands, as the config map has set the default file system to `hdfs://namenode:9000`.	

Command:
```bash
hdfs dfs -fs hdfs://namenode:9000 -ls /
```

Output:
```
bash-4.2$ hdfs dfs -ls /
Found 1 items
-rw-r--r--   3 root supergroup     154638 2024-09-09 13:41 /alice-in-wonderland.txt
```

Wanna read it?
Run: `hdfs dfs -cat /alice-in-wonderland.txt`

## Exercise 5

### Task 2

Command:
```bash
kubectl run interactive --rm -i --tty --image python:3.11 -- /bin/bash
```
*Copy files over, by using nano or vim.*

Commands:
```bash
apt update && apt install nano
# Copy files using nano
pip install hdfs
```

Output:  Alice in wonderworld is printed

## Exercise 6

Command:
```bash
# Copy counting-job.py to the interactive pod using nano or vim
python counting-job.py
```

*Modify simple-client to read `word-count.json`.*  
Resulting File: `file-reader.py`

Command:
```bash
python file-reader.py
```

Output:
```
root@interactive:/# python3 file-ready.py 
Listing contents of the HDFS root directory:
['alice-in-wonderland.txt', 'word-count.json', 'write.txt']
Enter filename to read: word-count.json
Reading contents of file:
[["the", 1515], ["and", 717], ["to", 706], ["a", 611], ["of", 493], ["she", 485], ["said", 416], ["it", 347], ["in", 346], ["was", 327]]
```

## Exercise 7

Copy remaining files to the interactive pod using nano or vim.

Install packages

Commands:
```bash
pip install -r requirements.txt
```

Run the script

Command:
```bash
python counting-avro.py
```

Output:
```
root@interactive:/# python counting-avro.py
{'type': 'record', 'name': '__Record1', 'fields': [{'name': 'count', 'type': 'int'}, {'name': 'word', 'type': 'string'}]}


[{'count': 1515, 'word': 'the'}, {'count': 717, 'word': 'and'}, {'count': 706, 'word': 'to'}, {'count': 611, 'word': 'a'}, {'count': 493, 'word': 'of'}, {'count': 485, 'word': 'she'}, {'count': 416, 'word': 'said'}, {'count': 347, 'word': 'it'}, {'count': 346, 'word': 'in'}, {'count': 327, 'word': 'was'}]
```

Now we can inspect the avro file, using tool made earlier.

Command:
```bash
python file-reader.py
```

Output:
```
root@interactive:/# python file-reader.py
Listing contents of the HDFS root directory:
['alice-in-wonderland.txt', 'word-count.avro', 'word-count.json', 'write.txt']
Enter filename to read: word-count.avro
Reading contents of file:
Objavro.codenullavro.schema�{"name": "__Record1", "type": "record", "fields": [{"name": "count", "type": "int"}, {"name": "word", "type": "string"}]}�[;�N?��c�d�����n�the�
                                                                                                                                                                                   and�
                                                                                                                                                                                        to�    a�of�she�said�it�in�was�[;�N?��c�d����� 
```

## Exercise 8

Run the script

Command:
```bash
python counting-parquet.py
```

Output:
```
root@interactive:/# python counting-parquet.py
   ***  START  OF  THE  PROJECT  GUTENBERG  EBOOK  ALICE'S  ADVENTURES  IN  WONDERLAND  ***  [Illustration]  Alice’s  ...  years,  loving  childhood:  gather  _their_  tale,  ago:  sorrows,  joys,  remembering  child-life,  happy  days.  E END
0      1      1   3    5        2          2      2        2           2   2           2    3               1       11  ...       1       1           1       1        1      1     1         1      1            1            1      1      1    2

[1 rows x 5278 columns]
```

Output:
```
# Waaayyyy to long of a file to show it here.
```

## Exercise 9

### Description

The objective of this exercise is to create a fictive data source. We want to create a Python program that enables the simulation of multiple data sources. The fictive data source could be a sensor that measures the wattage of an electricity line. The sample rate of the sensor will be adjustable. However, this will default to 1Hz. The ID of the sensor must differentiate the six data streams and the valid range of the wattage for these electricity lines is between ±600MW. 

You need to write a program simulates the above-mentioned information. The program at this stage may only provide a single temporal aspect ("real_time"). However, the schema must accommodate other temporal aspects such as "edge prediction" in the future. 

You have the role of a data engineer and are required to store the samples from the sensors in HDFS for later analysis. 


**Tasks**:

1. Which file format is most suitable for storing sensor samples?
2. How will you design the folder structure of your sensor samples?
3. Define a common schema for the fictive data sources
4. Write a Python program for the fictive data source that simulates the six sensors. Make use of the knowledge from exercises 5 to 8.
5. Write a Kubernetes deployment for your Python program. 
    - How will you use the same Python program for each of the stations?
    - How will you write the Dockerfile and which image will you start from?
6. Write a short description of how you will deploy these data sources in Kubernetes together with your thoughts and conclusion to the two first questions in our Discord channel!

### Solution

#### Task 1

The most suitable file format for storing sensor samples, would be the Parquet file format.  
This is heavily affected by two aspects:

- Easy addition of new entries, which in this system would happen often, on a single record basis.
- Parquet is uptomized for querying a subset of columns. The data is to be stored for later analysis, and therefore it is likely that only a subset of the columns would be used in an analysis. 

Drawbacks of Parquet is that it would be efficient to store each sensor in their own files. Avro would be more efficient in this case, as it is a row-based format.
Avro is often used across application and for event based data, which sensor data could be considered. However, the later analysis would be more efficient with Parquet in regards to analyzing only a few columns.

#### Task 2

Due to the use of Parquet, it is ideal to split the data into multiple files, where each file represents a sensor.  
Each sensor has an ID, which can either be an integer, UUID or some other unique identifier.

In order to allow for other data storage in the hfds, the sensors will be stored in a folder system that represents the data source such as `<source>/<sensor_id>/<temporal_aspect>/<date>/<correlaction_id>`.  
As this system monitors electricity lines, the source would be `powergrid/elecricity_lines/wattage_offset`.  
Wich represents:

- **powergrid**: The main source of the data, which is the power grid of the region.
- **electricity_lines**: Where in the powergrid are we talking, which is the electricity lines.
- **wattage_offset**: The data that is stored, which is the wattage offset of the electricity lines.

The `sensor_id` allows to group data by sensor, hereafter by the temporal aspect, date and correlation ID, giving a clear overview of the data.

Therefore sensors would have the full path of `powergrid/elecricity_lines/wattage_offset/<sensor_id>/<temporal_aspect>/<date>/<correlaction_id>.parquet`.

*Another folder structure could be used, based on the other data saved, such as if all data stored is about the power grid, the `powergrid` folder could be removed.*

#### Task 3

The schema for the fictive data sources would be as follows:

```parquet
message SensorData {
   required binary sensor_id (UTF8);
   required binary correlation_id (UTF8);
   required int32 schema_version;
   required double modality;
   required binary unit (UTF8);
   required binary temporal_aspect (UTF8);
   required binary created_at (TIMESTAMP(isAdjustedToUTC=true, unit=MILLIOS));
}
```

Translated format from Parquet to Avro

```avro
{
  "type": "record",
  "name": "SensorData",
  "fields": [
    {"name": "sensor_id", "type": "string"},
    {"name": "correlation_id", "type": "string"},
    {"name": "schema_version", "type": "int"},
    {"name": "modality", "type": "double"},
    {"name": "unit", "type": "string"},
    {"name": "temporal_aspect", "type": "string"},
    {"name": "created_at", "type": "long"}
  ]
}
```

Example JSON format of the data:

```json
{
  "sensor_id": "sensor_1",
  "correlation_id": "correlation_1",
  "schema_version": 1,
  "modality": 17.25,
  "unit": "MW",
  "temporal_aspect": "real_time",
  "created_at": 1631184000000
}
```

Notes:

- **sensor_id**: The unique identifier of the sensor.
- **correlation_id**: The unique identifier of the correlation, which could be a group of sensors or the machine that processes the data.
- **schema_version**: The version of the schema used.
- **modality**: The value of the sensor, which is the wattage of the electricity line.
- **unit**: The unit of the modality, which is `MW`. By using string, this can be extended later.
- **temporal_aspect**: The temporal aspect of the data, which is the `real_time` or `edge_prediction`.
- **created_at**: The timestamp of when the data was created in microseconds. Microseconds is used to allow for more precise timestamps with high sample rates.

#### Task 4

The python application has been created in the folder [powergrid-sampler](./powergrid-sampler).  
The application is built as a webapp (allowing for healthchecks) that simulates the sensors, and stores the data in the format described above.

#### Task 5

The deployment for Kubernetes is written in the [k8s directory in powergrid-sampler](./powergrid-sampler/k8s).  
The deployment, with appending services is written to simulate to instanses, monitoring 10 sensors each.

Services allow for the sensors to be monitored, and the health of the sensors to be checked.

A [Dockerfile](./powergrid-sampler/docker/dockerfile) is written to build the application.  
This is based on the `python:3-alpine` image. The alpine variant is used to reduce the size of the image and make it as lightweight as possible, while we just use the latest version in the v3 group.  
For production builds, this should be pinned to a specific version, to ensure that the build is reproducable, but for this exercise, the latest version is used for simplicity.

The Dockerfile is build on top of previus experince with Python and Docker, such as the [flask-quiz](https://github.com/The0mikkel/flask-quiz/blob/main/dockerfile) project, which I made for hosting quizes for reading up to exams.  
The primse, is to install requirements, make a non-root user, copy the files and run the application using gunicorn (due to using flask for the web healthcheck).
