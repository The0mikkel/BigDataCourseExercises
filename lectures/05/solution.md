# Solution

- [Solution](#solution)
|- [Prerequisits](#prerequisits)
|- [Exercise 1](#exercise-1)
||- [Hive metastore](#hive-metastore)
||- [Hive](#hive)
|- [Exercise 2](#exercise-2)
||- [Upload file](#upload-file)
||- [Connect to hive](#connect-to-hive)
|||- [Show cataloges](#show-cataloges)
|||- [Create database](#create-database)
|||- [Create table](#create-table)
|||- [Query table](#query-table)
|||- [Count number of words in the text](#count-number-of-words-in-the-text)
|||- [Find the 10 most used words](#find-the-10-most-used-words)
|- [Exercise 3](#exercise-3)
||- [Upload backblaze data](#upload-backblaze-data)
||- [Create table for backblaze data](#create-table-for-backblaze-data)
||- [Questions regarding Backblaze data](#questions-regarding-backblaze-data)
|||- [Total count of each model](#total-count-of-each-model)
|||- [What is the capacity of the different hard drive models](#what-is-the-capacity-of-the-different-hard-drive-models)
|||- [What is the total capacity of all hard drive for each model](#what-is-the-total-capacity-of-all-hard-drive-for-each-model)

## Prerequisits

In order to prepare for the exercises, HDFS  must be running.

This can be installed from the `services` directory:

```bash
kubectl apply -f ../../services/hdfs/.
```

## Exercise 1

### Hive metastore

The first task is to deploy a PostgreSQL database for the Hive metastore.

This can be done by running the following command:

```bash
helm install postgresql \
  --version=12.1.5 \
  --set auth.username=root \
  --set auth.password=pwd1234 \
  --set auth.database=hive \
  --set primary.extendedConfiguration="password_encryption=md5" \
  --repo https://charts.bitnami.com/bitnami \
  postgresql
```

Which returns: 

```txt
NAME: postgresql
LAST DEPLOYED: Mon Sep 30 14:44:55 2024
NAMESPACE: mialb21
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: postgresql
CHART VERSION: 12.1.5
APP VERSION: 15.1.0

** Please be patient while the chart is being deployed **

PostgreSQL can be accessed via port 5432 on the following DNS names from within your cluster:

    postgresql.mialb21.svc.cluster.local - Read/Write connection

To get the password for "postgres" run:

    export POSTGRES_ADMIN_PASSWORD=$(kubectl get secret --namespace mialb21 postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

To get the password for "root" run:

    export POSTGRES_PASSWORD=$(kubectl get secret --namespace mialb21 postgresql -o jsonpath="{.data.password}" | base64 -d)

To connect to your database run the following command:

    kubectl run postgresql-client --rm --tty -i --restart='Never' --namespace mialb21 --image docker.io/bitnami/postgresql:15.1.0-debian-11-r12 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --command -- psql --host postgresql -U root -d hive -p 5432

    > NOTE: If you access the container using bash, make sure that you execute "/opt/bitnami/scripts/postgresql/entrypoint.sh /bin/bash" in order to avoid the error "psql: local user with ID 1001} does not exist"        

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace mialb21 svc/postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U root -d hive -p 5432
```

At the current point, the namespace looks like this:

```txt
NAME               READY   STATUS    RESTARTS   AGE
pod/datanode-0     1/1     Running   0          118s
pod/datanode-1     1/1     Running   0          103s
pod/datanode-2     1/1     Running   0          88s
pod/hdfs-cli       1/1     Running   0          118s
pod/namenode-0     1/1     Running   0          118s
pod/postgresql-0   1/1     Running   0          100s

NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
service/datanode        ClusterIP   10.152.183.234   <none>        9864/TCP            118s
service/namenode        ClusterIP   10.152.183.22    <none>        9870/TCP,9000/TCP   118s
service/postgresql      ClusterIP   10.152.183.169   <none>        5432/TCP            100s
service/postgresql-hl   ClusterIP   None             <none>        5432/TCP            100s

NAME                          READY   AGE
statefulset.apps/datanode     3/3     118s
statefulset.apps/namenode     1/1     118s
statefulset.apps/postgresql   1/1     100s
```

After this, we need to apply the hive metastore:

```bash
kubectl apply -f hive-metastore.yaml

# Returns:
# configmap/hive-metastore-config created
# configmap/hive-metastore-entrypoint created
# deployment.apps/hive-metastore created
# service/hive-metastore created
```

### Hive

The next step is to deploy Hive:

```bash
kubectl apply -f hive.yaml
```

Which returns:

```txt
persistentvolumeclaim/hive-warehouse-pvc created
deployment.apps/hiveserver2 created
service/hiveserver2 created
```

With the namespace looking like this:

```txt
NAME                                  READY   STATUS    RESTARTS   AGE
pod/datanode-0                        1/1     Running   0          5m13s
pod/datanode-1                        1/1     Running   0          4m58s
pod/datanode-2                        1/1     Running   0          4m43s
pod/hdfs-cli                          1/1     Running   0          5m13s
pod/hive-metastore-748656bb6b-6rvnh   1/1     Running   0          104s
pod/hiveserver2-7468b4f59b-h2stt      1/1     Running   0          17s
pod/namenode-0                        1/1     Running   0          5m13s
pod/postgresql-0                      1/1     Running   0          4m55s

NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)               AGE
service/datanode         ClusterIP   10.152.183.234   <none>        9864/TCP              5m13s
service/hive-metastore   ClusterIP   10.152.183.24    <none>        9083/TCP              104s
service/hiveserver2      ClusterIP   10.152.183.236   <none>        10000/TCP,10002/TCP   17s
service/namenode         ClusterIP   10.152.183.22    <none>        9870/TCP,9000/TCP     5m13s
service/postgresql       ClusterIP   10.152.183.169   <none>        5432/TCP              4m55s
service/postgresql-hl    ClusterIP   None             <none>        5432/TCP              4m55s

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hive-metastore   1/1     1            1           104s
deployment.apps/hiveserver2      1/1     1            1           17s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/hive-metastore-748656bb6b   1         1         1       104s
replicaset.apps/hiveserver2-7468b4f59b      1         1         1       17s

NAME                          READY   AGE
statefulset.apps/datanode     3/3     5m13s
statefulset.apps/namenode     1/1     5m13s
statefulset.apps/postgresql   1/1     4m55
```

## Exercise 2

### Upload file

First we need to uploade Alice in Wonderland to HDFS:

```bash
kubectl run hdfs-cli -it -- bash

# In the interactive shell:
wget -O alice-in-wonderland.txt https://www.gutenberg.org/files/11/11-0.txt

hdfs fds -mkdir /word-count
hdfs dfs -fs hdfs://namenode:9000 -put alice-in-wonderland.txt /word-count/alice-in-wonderland.txt
```

### Connect to hive

Next, we need to connect to Hive:

```bash
kubectl port-forward svc/hiveserver2 10002:10002 &
kubectl port-forward svc/hiveserver2 10000:10000 &
```

The rest of the exercise is then done in DBeaver.

#### Show cataloges

```sql
SHOW TABLES;
```

Which returns no tables.

#### Create database

```sql
CREATE
DATABASE IF NOT EXISTS bucket
LOCATION 'hdfs://namenode:9000/user/hive/warehouse/'
```

Which successfully creates the database.

This can be verified by running:

```sql
SHOW DATABASES;
```

Which returns:

```txt
bucket
default
```

#### Create table

```sql
CREATE TABLE bucket.text
(
    line STRING
) STORED AS TEXTFILE
LOCATION 'hdfs://namenode:9000/word-count';
```

Which successfully creates the table.

We can go into bucket and veryfy that the table is there:

```sql
USE bucket;
SHOW TABLES;
```

This returns the table "text".

#### Query table

```sql
SELECT * FROM text LIMIT 10;
```

Which returns the first 10 lines of the text file.

#### Count number of words in the text

```sql
SELECT SUM(SIZE (SPLIT(line, ' '))) AS word_count
FROM bucket.text;
```

This returns the following, with the response time of 3 seconds:

```txt
28,021
```

#### Find the 10 most used words

```sql
SELECT word, COUNT(*) AS count
FROM (
    SELECT EXPLODE(SPLIT(line, ' ')) AS word
    FROM bucket.text
    ) temp
GROUP BY word
ORDER BY count DESC
    LIMIT 10;
```

Which returns the following, with the response time of 3 seconds:

|--|---|
| word | count |
| ---- | ----- |
| the  | 1515  |
|      | 1472  |
| and  | 717   |
| to   | 706   |
| a    | 611   |
| of   | 493   |
| she  | 485   |
| said | 416   |
| it   | 347   |
| in   | 346   |

## Exercise 3

### Upload backblaze data

To upload the backblaze data, the following commands can be run:

```bash
# Open interactive container, that allows full access to apt
kubectl exec hdfs-cli -it -- bash

wget -O backblaze-data.csv https://raw.githubusercontent.com/The0mikkel/BigDataCourseExercises/refs/heads/main/lectures/05/data/2023-06-30.csv

hdfs dfs -mkdir /backblaze-data
hdfs dfs -put backblaze-data.csv /backblaze-data/2023-06-30.csv
```

### Create table for backblaze data

The table can be created by running the following commands:

```sql
CREATE
EXTERNAL TABLE IF NOT EXISTS bucket.backblaze (
  `date` STRING,
  serial_number STRING,
  model STRING,
  capacity_bytes STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:9000/backblaze-data'
TBLPROPERTIES (
  'skip.header.line.count'='1'
);
```

And we can verify that the table is created by running:

```sql
USE bucket;
SHOW TABLES;
```

Which returns:

```txt
backblaze
text
```

We can also verify that content is in the table by running:

```sql
SELECT COUNT(*) FROM bucket.backblaze;
```

Which returns:

```txt
245757
```

We can also query the table to see the first 10 rows:

```sql
SELECT * FROM bucket.backblaze LIMIT 10;
```

Which returns the first 10 rows of the table.

```txt
Date        Serial Number|Model|                Capacity Bytes
2023-06-30|PL1331LAGDJ5GH|HGST HDS5C4040ALE630|4000787030016
2023-06-30|PL2331LAGLW5UJ|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGM410J|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGM5NTJ|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGM5R4J|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGM82LJ|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGM9J9J|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGM9Y6J|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGMAPRJ|HGST HMS5C4040BLE640|4000787030016
2023-06-30|PL2331LAGMDMLJ|HGST HMS5C4040BLE640|4000787030016
```

### Questions regarding Backblaze data

#### Total count of each model

```sql
SELECT model, COUNT(*) AS count FROM bucket.backblaze GROUP BY model;
```

Which returns:

| model                                  | count |
| -------------------------------------- | ----- |
| TOSHIBA MG07ACA14TA                    | 38101 |
| ST16000NM001G                          | 27255 |
| ST12000NM0008                          | 19677 |
| ST4000DM000                            | 17899 |
| ST8000NM0055                           | 14118 |
| WDC WUH721816ALE6L4                    | 14099 |
| HGST HUH721212ALE604                   | 13203 |
| ST12000NM001G                          | 13029 |
| HGST HMS5C4040BLE640                   | 11934 |
| ST14000NM001G                          | 10790 |
| HGST HUH721212ALN604                   | 10537 |
| ST8000DM002                            | 9354  |
| WDC WUH721414ALE6L4                    | 8432  |
| TOSHIBA MG08ACA16TE                    | 5923  |
| TOSHIBA MG08ACA16TEY                   | 5289  |
| TOSHIBA MG08ACA16TA                    | 5199  |
| HGST HMS5C4040ALE640                   | 3621  |
| WDC WUH721816ALE6L0                    | 2697  |
| HGST HUH721212ALE600                   | 2606  |
| ST14000NM0138                          | 1458  |
| ST12000NM0007                          | 1214  |
| ST10000NM0086                          | 1124  |
| HGST HUH728080ALE600                   | 1115  |
| Seagate BarraCuda 120 SSD ZA250CM10003 | 1114  |
| ST6000DX000                            | 883   |
| TOSHIBA MG07ACA14TEY                   | 616   |
| CT250MX500SSD1                         | 598   |
| Seagate BarraCuda SSD ZA250CM10002     | 547   |
| DELLBOSS VD                            | 411   |
| ST500LM012 HN                          | 381   |
| ST16000NM002J                          | 309   |
| TOSHIBA MQ01ABF050M                    | 231   |
| TOSHIBA MQ01ABF050                     | 221   |
| ST500LM030                             | 205   |
| WDC WD5000LPVX                         | 186   |
| ST8000NM000A                           | 153   |
| WDC WDS250G2B0A                        | 108   |
| Seagate SSD                            | 106   |
| TOSHIBA MD04ABA400V                    | 94    |
| HGST HUH728080ALE604                   | 90    |
| MTFDDAV240TCB                          | 88    |
| Seagate IronWolf ZA250NM10002          | 80    |
| WD Blue SA510 2.5 250GB                | 65    |
| TOSHIBA HDWF180                        | 61    |
| ST14000NM0018                          | 60    |
| ST18000NM000J                          | 60    |
| WDC WD5000LPCX                         | 52    |
| HGST HUS726040ALE610                   | 38    |
| ST4000DM005                            | 34    |
| ST500LM021                             | 30    |
| ST10000NM001G                          | 28    |
| HGST HDS5C4040ALE630                   | 26    |
| ST16000NM005G                          | 26    |
| ST8000DM005                            | 25    |
| HGST HUS728T8TALE6L4                   | 20    |
| HGST HUH721010ALE600                   | 20    |
| ST4000DM004                            | 19    |
| HGST HUS726040ALN610                   | 18    |
| Seagate BarraCuda SSD ZA500CM10002     | 18    |
| WDC WD5000BPKT                         | 9     |
| ST12000NM0117                          | 8     |
| Hitachi HDS5C4040ALE630                | 6     |
| ST6000DM001                            | 4     |
| WDC WUH722222ALE6L4                    | 4     |
| TOSHIBA HDWE160                        | 4     |
| ST12000NM003G                          | 3     |
| Seagate BarraCuda 120 SSD ZA500CM10003 | 3     |
| ST12000NM000J                          | 3     |
| ST16000NM000J                          | 3     |
| WDC WD60EFRX                           | 3     |
| Seagate BarraCuda SSD ZA2000CM10002    | 3     |
| ST14000NM000J                          | 2     |
| Seagate FireCuda 120 SSD ZA500GM10001  | 2     |
| ST6000DM004                            | 1     |
| HGST HDS724040ALE640                   | 1     |
| HGST HMS5C4040BLE641                   | 1     |
| SSDSCKKB240GZR                         | 1     |
| ST1000LM024 HN                         | 1     |

#### What is the capacity of the different hard drive models

```sql
SELECT DISTINCT model, capacity_bytes FROM bucket.backblaze;
```

Which returns:

| model                                  | capacity_bytes |
| -------------------------------------- | -------------- |
| CT250MX500SSD1                         | 250059350016   |
| HGST HDS5C4040ALE630                   | 4000787030016  |
| HGST HDS724040ALE640                   | 4000787030016  |
| HGST HUH721212ALE600                   | 12000138625024 |
| HGST HUH728080ALE600                   | 8001563222016  |
| HGST HUH728080ALE604                   | 8001563222016  |
| HGST HUS726040ALE610                   | 4000787030016  |
| HGST HUS726040ALN610                   | 4000787030016  |
| Hitachi HDS5C4040ALE630                | 4000787030016  |
| SSDSCKKB240GZR                         | 240057409536   |
| ST12000NM0007                          | 12000138625024 |
| ST12000NM001G                          | 12000138625024 |
| ST14000NM000J                          | 14000519643136 |
| ST14000NM0018                          | 14000519643136 |
| ST4000DM000                            | -1             |
| ST500LM012 HN                          | 500107862016   |
| ST500LM021                             | 500107862016   |
| ST8000DM002                            | -1             |
| ST8000DM002                            | 8001563222016  |
| Seagate BarraCuda SSD ZA2000CM10002    | 2000398934016  |
| Seagate BarraCuda SSD ZA250CM10002     | 250059350016   |
| Seagate BarraCuda SSD ZA500CM10002     | 500107862016   |
| TOSHIBA HDWE160                        | 6001175126016  |
| TOSHIBA MQ01ABF050M                    | 500107862016   |
| WDC WD5000LPCX                         | 500107862016   |
| DELLBOSS VD                            | 480036847616   |
| HGST HUH721212ALE604                   | 12000138625024 |
| HGST HUH721212ALN604                   | 12000138625024 |
| ST12000NM003G                          | 12000138625024 |
| ST16000NM000J                          | 16000900661248 |
| ST16000NM005G                          | 16000900661248 |
| ST4000DM004                            | 4000787030016  |
| ST4000DM005                            | 4000787030016  |
| ST6000DM001                            | 6001175126016  |
| ST8000DM005                            | 8001563222016  |
| ST8000NM000A                           | 8001563222016  |
| Seagate BarraCuda 120 SSD ZA250CM10003 | 250059350016   |
| Seagate IronWolf ZA250NM10002          | 250059350016   |
| TOSHIBA HDWF180                        | 8001563222016  |
| TOSHIBA MG07ACA14TA                    | 14000519643136 |
| TOSHIBA MG08ACA16TE                    | 16000900661248 |
| WDC WD5000LPVX                         | 500107862016   |
| WDC WDS250G2B0A                        | 250059350016   |
| WDC WUH721816ALE6L4                    | 16000900661248 |
| HGST HMS5C4040BLE640                   | 4000787030016  |
| MTFDDAV240TCB                          | 240057409536   |
| ST1000LM024 HN                         | 1000204886016  |
| ST12000NM000J                          | 12000138625024 |
| ST12000NM0117                          | 12000138625024 |
| ST16000NM001G                          | -1             |
| ST16000NM002J                          | 16000900661248 |
| ST8000NM0055                           | -1             |
| ST8000NM0055                           | 8001563222016  |
| Seagate BarraCuda 120 SSD ZA500CM10003 | 500107862016   |
| TOSHIBA MD04ABA400V                    | 4000787030016  |
| TOSHIBA MG08ACA16TA                    | 16000900661248 |
| WD Blue SA510 2.5 250GB                | 250059350016   |
| WDC WUH721414ALE6L4                    | 14000519643136 |
| HGST HMS5C4040ALE640                   | 4000787030016  |
| HGST HMS5C4040BLE641                   | 4000787030016  |
| HGST HUH721010ALE600                   | 10000831348736 |
| HGST HUS728T8TALE6L4                   | 8001563222016  |
| ST10000NM001G                          | 10000831348736 |
| ST10000NM0086                          | 10000831348736 |
| ST12000NM0008                          | 12000138625024 |
| ST14000NM001G                          | 14000519643136 |
| ST14000NM0138                          | 14000519643136 |
| ST16000NM001G                          | 16000900661248 |
| ST18000NM000J                          | 18000207937536 |
| ST4000DM000                            | 4000787030016  |
| ST500LM030                             | 500107862016   |
| ST6000DM004                            | 6001175126016  |
| ST6000DX000                            | 6001175126016  |
| Seagate FireCuda 120 SSD ZA500GM10001  | 500107862016   |
| Seagate SSD                            | 250059350016   |
| TOSHIBA MG07ACA14TEY                   | 14000519643136 |
| TOSHIBA MG08ACA16TEY                   | 16000900661248 |
| TOSHIBA MQ01ABF050                     | 500107862016   |
| WDC WD5000BPKT                         | 500107862016   |
| WDC WD60EFRX                           | 6001175126016  |
| WDC WUH721816ALE6L0                    | 16000900661248 |
| WDC WUH722222ALE6L4                    | 22000969973760 |

#### What is the total capacity of all hard drive for each model

```sql
SELECT model, SUM(CAST(capacity_bytes AS BIGINT))/1024/1024/1024/1024 AS total_capacity_in_tb FROM bucket.backblaze GROUP BY model;
```

Which returns:

| model                                  | total_capacity_in_tb |
| -------------------------------------- | -------------------- |
| TOSHIBA MG07ACA14TA                    | 485155.21            |
| ST16000NM001G                          | 396620.22            |
| ST12000NM0008                          | 214756.01            |
| WDC WUH721816ALE6L4                    | 205179.0             |
| HGST HUH721212ALE604                   | 144098.37            |
| ST12000NM001G                          | 142199.32            |
| ST14000NM001G                          | 137393.37            |
| HGST HUH721212ALN604                   | 115001.48            |
| WDC WUH721414ALE6L4                    | 107368.02            |
| ST8000NM0055                           | 102734.76            |
| TOSHIBA MG08ACA16TE                    | 86195.85             |
| TOSHIBA MG08ACA16TEY                   | 76969.41             |
| TOSHIBA MG08ACA16TA                    | 75659.67             |
| ST8000DM002                            | 67890.67             |
| ST4000DM000                            | 65096.25             |
| HGST HMS5C4040BLE640                   | 43424.18             |
| WDC WUH721816ALE6L0                    | 39248.72             |
| HGST HUH721212ALE600                   | 28442.05             |
| ST14000NM0138                          | 18565.29             |
| ST12000NM0007                          | 13249.67             |
| HGST HMS5C4040ALE640                   | 13175.71             |
| ST10000NM0086                          | 10223.57             |
| HGST HUH728080ALE600                   | 8114.28              |
| TOSHIBA MG07ACA14TEY                   | 7843.77              |
| ST6000DX000                            | 4819.45              |
| ST16000NM002J                          | 4496.79              |
| ST8000NM000A                           | 1113.44              |
| ST18000NM000J                          | 982.27               |
| ST14000NM0018                          | 764.0                |
| HGST HUH728080ALE604                   | 654.96               |
| TOSHIBA HDWF180                        | 443.92               |
| ST16000NM005G                          | 378.37               |
| TOSHIBA MD04ABA400V                    | 342.04               |
| ST10000NM001G                          | 254.68               |
| Seagate BarraCuda 120 SSD ZA250CM10003 | 253.35               |
| ST8000DM005                            | 181.93               |
| HGST HUH721010ALE600                   | 181.91               |
| DELLBOSS VD                            | 179.44               |
| ST500LM012 HN                          | 173.3                |
| HGST HUS728T8TALE6L4                   | 145.55               |
| HGST HUS726040ALE610                   | 138.27               |
| CT250MX500SSD1                         | 136.0                |
| Seagate BarraCuda SSD ZA250CM10002     | 124.4                |
| ST4000DM005                            | 123.72               |
| TOSHIBA MQ01ABF050M                    | 105.07               |
| TOSHIBA MQ01ABF050                     | 100.52               |
| HGST HDS5C4040ALE630                   | 94.61                |
| ST500LM030                             | 93.24                |
| ST12000NM0117                          | 87.31                |
| WDC WD5000LPVX                         | 84.6                 |
| WDC WUH722222ALE6L4                    | 80.04                |
| ST4000DM004                            | 69.14                |
| HGST HUS726040ALN610                   | 65.5                 |
| ST16000NM000J                          | 43.66                |
| ST12000NM003G                          | 32.74                |
| ST12000NM000J                          | 32.74                |
| ST14000NM000J                          | 25.47                |
| WDC WDS250G2B0A                        | 24.56                |
| Seagate SSD                            | 24.11                |
| WDC WD5000LPCX                         | 23.65                |
| Hitachi HDS5C4040ALE630                | 21.83                |
| ST6000DM001                            | 21.83                |
| TOSHIBA HDWE160                        | 21.83                |
| MTFDDAV240TCB                          | 19.21                |
| Seagate IronWolf ZA250NM10002          | 18.19                |
| WDC WD60EFRX                           | 16.37                |
| WD Blue SA510 2.5 250GB                | 14.78                |
| ST500LM021                             | 13.65                |
| Seagate BarraCuda SSD ZA500CM10002     | 8.19                 |
| ST6000DM004                            | 5.46                 |
| Seagate BarraCuda SSD ZA2000CM10002    | 5.46                 |
| WDC WD5000BPKT                         | 4.09                 |
| HGST HDS724040ALE640                   | 3.64                 |
| HGST HMS5C4040BLE641                   | 3.64                 |
| Seagate BarraCuda 120 SSD ZA500CM10003 | 1.36                 |
| Seagate FireCuda 120 SSD ZA500GM10001  | 0.91                 |
| ST1000LM024 HN                         | 0.91                 |
| SSDSCKKB240GZR                         | 0.22                 |

#### What hard drive model is the most used?

```sql
SELECT model, COUNT(*) AS count FROM bucket.backblaze GROUP BY model ORDER BY count DESC LIMIT 1;
```

Which returns:

| model               | count |
| ------------------- | ----- |
| TOSHIBA MG07ACA14TA | 38101 |

#### What hard drive model has the largest total capacity?

```sql
SELECT model, SUM(CAST(capacity_bytes AS BIGINT))/1024/1024/1024/1024 AS total_capacity_in_tb FROM bucket.backblaze GROUP BY model ORDER BY total_capacity_in_tb DESC LIMIT 1;
```

Which returns:

| model               | total_capacity_in_tb |
| ------------------- | -------------------- |
| TOSHIBA MG07ACA14TA | 485155.21            |

## Exercise 4

### Deploy mongodb

```bash
kubectl apply -f mongodb.yaml
```

### Interact with MongoDB

Port forward the Mongo express service:

```bash
kubectl port-forward svc/mongo-express 8081:8081 &
```

### MongoDB and Kafka connect

First we need to re-setup the power-grid data producer.

First we setup kafka:

```bash
# In /services/kafka-cluster
helm install --values kafka-values.yaml kafka oci://registry-1.docker.io/bitnamicharts/kafka --version 30.0.4
# In /services/kafka
kubectl apply -f .
```

Then we need to setup the INGESTION topic.  
This is done in the Redpanda UI.

For this we must forward the port:

```bash
kubectl port-forward svc/redpanda 8080:8080 &
```

Then create the `INGESTION` topic in Redpanda.

To produce content to the topic, we deploy the power-grid sampler from lecture 03:

```bash
kubectl apple -f ../03/powergrid-sampler/k8s/
```

Now we need to configure kafka connect, to move the records being produced to MongoDB.  
This is done in the same manner as [Lecture 03 Exercise 06](./../03/README.md#exercise-7---kafka-connect-and-hdfs)

```bash
kubectl port-forward svc/kafka-connect 8083 &
curl -X POST \
http://127.0.0.1:8083/connectors \
-H 'Content-Type: application/json' \
-d '{
  "name": "mongodb-sink",
  "config": {
    "connection.password": "password",
    "connection.uri": "mongodb://admin:password@mongodb:27017",
    "connection.url": "mongodb://mongodb:27017",
    "connection.username": "admin",
    "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
    "database": "kafka",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "key.converter.schemas.enable": "true",
    "output.format.key": "json",
    "output.format.value": "json",
    "post.processor.chain": "com.mongodb.kafka.connect.sink.processor.DocumentIdAdder",
    "tasks.max": "4",
    "timeseries.timefield.auto.convert": "false",
    "topics": "INGESTION",
    "value.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter.schemas.enable": "true"
  }
}'
```

We can now see in Mongo Express, that the data is being stored:
![Mongo express ingestion collection](images/mongo-express-ingestion.png)

Question:  
Validate that the connector is running. Please count the number of documents inside the `INGESTION`
collection. Does it match the number of records inside your `INGESTION` topic
in [redpanda](http://127.0.0.1:8080/topics/INGESTION#messages)?

Answer:  
Yes, it closely matches, however, there may be a slight difference, due to timing.

### Query Documents in MongoBD

Question:  
Count the number of documents inside the `INGESTION` collection where the `sensor_id=6`

Answer:  
As each datapoint for the record, is stored in their own column (which does not match the style the teacher hints at), it is easy to find all records for a given sensor.  
For simplicity, we can use Mongo Express, and simply do a simple search, where we put `sensor_id` as key, and `6` as value in the search box.
