# Solution

This document contains the solutions to the exercises in the lecture.

- [Solution](#solution)
  - [Exercise 1](#exercise-1)
    - [Validation](#validation)
  - [Exercise 2](#exercise-2)
    - [Service validation](#service-validation)
      - [Kafka Schema registry](#kafka-schema-registry)
      - [Kafka Connect](#kafka-connect)
      - [Kafka KSQL](#kafka-ksql)
  - [Exercise 3](#exercise-3)
  - [Exercise 4](#exercise-4)
    - [Task 1 - Properties of topic](#task-1---properties-of-topic)
    - [Task 2 - Create topic](#task-2---create-topic)
    - [Task 3 - What will sensor id key do](#task-3---what-will-sensor-id-key-do)
    - [Task 4 - Recreate powergrid sampler to post to Kafka](#task-4---recreate-powergrid-sampler-to-post-to-kafka)
  - [Exercise 5](#exercise-5)
  - [Exercise 6](#exercise-6)
  - [Exercise 7](#exercise-7)

## Exercise 1

First, we need to deploy the cluster.  
For this we follow the helm install command from the documentation:

```bash
helm install --values kafka-values.yaml kafka oci://registry-1.docker.io/bitnamicharts/kafka --version 30.0.4
```

Then we can check the status of the pods:

```bash
kubectl get all
```

The output then looks like this:

```txt
NAME                     READY   STATUS    RESTARTS   AGE
pod/kafka-controller-0   1/1     Running   0          78s
pod/kafka-controller-1   1/1     Running   0          78s
pod/kafka-controller-2   1/1     Running   0          78s

NAME                                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
service/kafka                       ClusterIP   10.152.183.158   <none>        9092/TCP                     78s
service/kafka-controller-headless   ClusterIP   None             <none>        9094/TCP,9092/TCP,9093/TCP   78s

NAME                                READY   AGE
statefulset.apps/kafka-controller   3/3     78s
```

### Validation

Now we need to validate that the Kafka cluster was deployed correctly.  
To do this, the first task is to create a topic, then produce a message and finally consume the message.

To do this, we use a client pod to interact with the Kafka cluster.

```bash
kubectl run kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.8.0-debian-12-r3  --command -- sleep infinity
```

The output then looks like this:

```txt
pod/kafka-client created
```

From here, we use a shell in the client pod to interact with the Kafka cluster.

```bash
kubectl exec --tty -i kafka-client -- bash
```

We are using two terminals from here, both connected through the above command.  
In the first terminal, we use a console producer, and in the second terminal, we use a console consumer.

In the first terminal, we create a topic:

```bash
kafka-console-producer.sh --bootstrap-server kafka:9092 --topic test
```

In the second terminal, we consume the message:

```bash
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic test --from-beginning
```

Now we can write a message in the first terminal and see it appear in the second terminal.

```txt
> Hello, World!
```

The output in the second terminal then looks like this:

```txt
Hello, World!
```

The following screenshot shows the two consoles side by side:
![Screenshots of terminals connected as producer and consumer in Kafka](solution-images/kafka-test-two-consoles.png)

We then delete the kafka client pod:

```bash
kubectl delete pod kafka-client
```

## Exercise 2

This execise is about Kafka Connect, Kafka Schema Registry, and Kafka KSQL.

The first task is about familiarizing with the three deployment files for the beforementioned services.

- [kafka-schema-registry.yaml](./kafka-schema-registry.yaml)
- [kafka-connect.yaml](./kafka-connect.yaml)
- [kafka-ksqldb.yaml](./kafka-ksqldb.yaml)

In them, we see config maps, services, deployments as well as storage claims (for Kafka Connect).

The second task is to deploy the services.  
This can be done by running the following commands (*As noted in the instructions*):

```bash
kubectl apply --filename=kafka-schema-registry.yaml,kafka-connect.yaml,kafka-ksqldb.yaml
```

After the deployment, we can check the status of the pods:

```bash
kubectl get all
```

The output then looks like this:

```txt
NAME                                        READY   STATUS    RESTARTS   AGE
pod/kafka-connect-5c76db745f-hrdwl          1/1     Running   0          59s
pod/kafka-controller-0                      1/1     Running   0          22m
pod/kafka-controller-1                      1/1     Running   0          22m
pod/kafka-controller-2                      1/1     Running   0          22m
pod/kafka-ksqldb-cli-b74fb48c4-fzr7j        1/1     Running   0          59s
pod/kafka-ksqldb-server-56b6c66847-6sfrm    1/1     Running   0          59s
pod/kafka-schema-registry-794b485bb-946q9   1/1     Running   0          59s

NAME                                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
service/kafka                       ClusterIP   10.152.183.158   <none>        9092/TCP                     22m
service/kafka-connect               NodePort    10.152.183.250   <none>        8083:30374/TCP               59s
service/kafka-controller-headless   ClusterIP   None             <none>        9094/TCP,9092/TCP,9093/TCP   22m
service/kafka-ksqldb-server         NodePort    10.152.183.212   <none>        8088:31879/TCP               59s
service/kafka-schema-registry       ClusterIP   10.152.183.56    <none>        8081/TCP                     59s

NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kafka-connect           1/1     1            1           59s
deployment.apps/kafka-ksqldb-cli        1/1     1            1           59s
deployment.apps/kafka-ksqldb-server     1/1     1            1           59s
deployment.apps/kafka-schema-registry   1/1     1            1           59s

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/kafka-connect-5c76db745f          1         1         1       59s
replicaset.apps/kafka-ksqldb-cli-b74fb48c4        1         1         1       59s
replicaset.apps/kafka-ksqldb-server-56b6c66847    1         1         1       59s
replicaset.apps/kafka-schema-registry-794b485bb   1         1         1       59s

NAME                                READY   AGE
statefulset.apps/kafka-controller   3/3     22m
```

Then the instructions says to change some values in the config map for the redpanda deployment in [redpanda.yaml](./redpanda.yaml).

*This was already done (not by me), so we can skip this step.*

### Service validation

Now we can interact with the services.

#### Kafka Schema registry

To test the schema registry, we can follow the instructions in the exercise.

```bash
kubectl port-forward svc/kafka-schema-registry 8081:8081
```

Then we can open the browser and go to [http://localhost:8081](http://localhost:8081).  
Returned is:

```json
{}
```

#### Kafka Connect

The same can be done for the Kafka Connect service.

```bash
kubectl port-forward svc/kafka-connect 8083:8083
```

Then we can open the browser and go to [http://localhost:8083](http://localhost:8083).
Returned is:

```json
{"version":"7.3.1-ce","commit":"a453cbd27246f7bb","kafka_cluster_id":"OijWyl0mcQDmVsdNmz5dRN"}
```

#### Kafka KSQL

The KsqlDB service is a bit different, as we can use the KsqlDB CLI to interact with it.

```bash
kubectl exec --stdin --tty deployment/kafka-ksqldb-cli -- ksql http://kafka-ksqldb-server:8088
```

The output is then:

```txt
                  ===========================================
                  =       _              _ ____  ____       =
                  =      | | _____  __ _| |  _ \| __ )      =
                  =      | |/ / __|/ _` | | | | |  _ \      =
                  =      |   <\__ \ (_| | | |_| | |_) |     =
                  =      |_|\_\___/\__, |_|____/|____/      =
                  =                   |_|                   =
                  =        The Database purpose-built       =
                  =        for stream processing apps       =
                  ===========================================

Copyright 2017-2022 Confluent Inc.

CLI v7.3.1, Server v7.3.1 located at http://kafka-ksqldb-server:8088
Server Status: RUNNING

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql> exit
Exiting ksqlDB.
```

These services respond in line with the expectations, and the deployment is successful.

## Exercise 3

This exercise focuses on the Redpanda deployment.

To deploy, we can use the provided [redpanda.yaml](./redpanda.yaml) file.

```bash
kubectl apply -f redpanda.yaml
```

After the deployment, we can check the status of the pods:

```bash
kubectl get all
```

The output then looks like this:

```txt
NAME                                        READY   STATUS    RESTARTS   AGE
pod/kafka-connect-5c76db745f-hrdwl          1/1     Running   0          30m
pod/kafka-controller-0                      1/1     Running   0          52m
pod/kafka-controller-1                      1/1     Running   0          52m
pod/kafka-controller-2                      1/1     Running   0          52m
pod/kafka-ksqldb-cli-b74fb48c4-fzr7j        1/1     Running   0          30m
pod/kafka-ksqldb-server-56b6c66847-6sfrm    1/1     Running   0          30m
pod/kafka-schema-registry-794b485bb-946q9   1/1     Running   0          30m
pod/redpanda-7b8b757c5d-kkgpb               1/1     Running   0          5s

NAME                                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
service/kafka                       ClusterIP   10.152.183.158   <none>        9092/TCP                     52m
service/kafka-connect               NodePort    10.152.183.250   <none>        8083:30374/TCP               30m
service/kafka-controller-headless   ClusterIP   None             <none>        9094/TCP,9092/TCP,9093/TCP   52m
service/kafka-ksqldb-server         NodePort    10.152.183.212   <none>        8088:31879/TCP               30m
service/kafka-schema-registry       ClusterIP   10.152.183.56    <none>        8081/TCP                     30m
service/redpanda                    ClusterIP   10.152.183.225   <none>        8080/TCP                     5s

NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kafka-connect           1/1     1            1           30m
deployment.apps/kafka-ksqldb-cli        1/1     1            1           30m
deployment.apps/kafka-ksqldb-server     1/1     1            1           30m
deployment.apps/kafka-schema-registry   1/1     1            1           30m
deployment.apps/redpanda                1/1     1            1           5s

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/kafka-connect-5c76db745f          1         1         1       30m
replicaset.apps/kafka-ksqldb-cli-b74fb48c4        1         1         1       30m
replicaset.apps/kafka-ksqldb-server-56b6c66847    1         1         1       30m
replicaset.apps/kafka-schema-registry-794b485bb   1         1         1       30m
replicaset.apps/redpanda-7b8b757c5d               1         1         1       5s

NAME                                READY   AGE
statefulset.apps/kafka-controller   3/3     52m
```

We can now try to access the Redpanda service by port forwarding:

```bash
kubectl port-forward svc/redpanda 8080:8080
```

Then we can open the browser and go to [http://localhost:8080](http://localhost:8080).

![Redpanda in browser](solution-images/redpanda-access.png)

We can then see the overview of the Kafka cluster, including the topics, brokers, and partitions.  
Especially can we see the internal Kafka items and the "test" topic we created earlier.

## Exercise 4

This exercise an extension on lecture 2 exercise 10, where we created a power sampler in python for hdfs. This time we will use the same sampler but for Kafka, where Kafka Connect will push it to hdfs.

### Task 1 - Properties of topic

- How many partitions will you have for the `INGESTION` topic?
  - For the powergrid sampler, we want up to 3 consumers (fictive number, but this is the real constraint).  
  This means we need at least 3 partitions, to allow for parallel consumption.  
  We can increase this to 6 partitions, to allow for more consumers in the future.
- Which replication factor will you use for the `INGESTION` topic?
  - Since the cluster is small, we can use a replication factor of 3, mathcing the number of brokers and reaching HA minimum.
- Which min in-sync replicas will you use for the `INGESTION` topic?
  - For reliability and HA, we should at least have 2 in-sync replicas.  
    This allows for the loss of one broker without data loss and with continued operation.
- What would be an appropriate retention time for the `INGESTION` topic?
  - For a powergrid reader, which uses kafka connect to push to hdfs, we can use a retention time of 1 day. This allows for small downtime and still allows for the data to be read by the consumer.  
  - If we see, that we may use the messages for longer, this can be increased to 7 days or longer.
- What would be an appropriate retention size for the `INGESTION` topic?
  - Currently there is no guide to, how many datapoints fits in a given size, but we can use a size of 1GB. This allows for a good amount of data to be stored, while still being able to be read by the consumer, without the need for a large amount of storage.  
  - If we see, that 1 GB is too small over time, we can increase the size to 10 GB.

### Task 2 - Create topic

Create `INGESTION` topic with the properties from the previous task.  
This is done in the redpanda web interface.

![Ingest creation in redpanda](solution-images/ingestion-topic-creation.png)

### Task 3 - What will sensor id key do

Question: Which property will be possible if you add a key, which defines the sensor id, to each record?

Answer:

It will be possible for one consumer to receive all data for the single sensor, and only that consumer, as all sensor data will be in the same partition.

### Task 4 - Recreate powergrid sampler to post to Kafka

The powergrid sampler is recreated to post to Kafka.

This is done in the [powergrid-sampler](./powergrid-sampler) directory.

The sampler is then deployed to the cluster.

```bash
kubectl apply -f powergrid-sampler/k8s/
```

The result, is that the sensor data is posted to the Kafka topic.

![Redpanda ingestion view](solution-images/redpanda-ingestion-topic.png)

## Exercise 5

The source code for the powergrid sampler can be found in the [powergrid-sampler](./powergrid-sampler) directory, which has been updated to receive the Kafka topic as an environment variable.

Primary update is the following, which handles the Kafka producer:

```python
def start_sensor(sensorId):
    logger.debug(f"Starting sensor {sensorId}")
    logger.debug(f"Correlation ID: {correlationId}")
    logger.debug(f"Sample rate: {sampleRate}")
    
    sensor = Sensor(sensorId, correlationId, sampleRate, save_data)
    sensor.start_listening()

def read_sensor():
    # Process data
    logger.debug(f"Reading sensor data from Kafka topic {kafka_topic}")
    client.receive_msg(process_data, get_consumer(kafka_topic, group_id=group_id))
```

To get the output, we can use the following command:

```bash
# Reader 1
kubectl logs deployments/reader-1

# Reader 2
kubectl logs deployments/reader-2
```

Questions:  
*Start another consumer but with a different group id in your interactive container. What happens when you run the program?*

Answer:  
When starting another consumer in a different group id, the consumer will get the same messages as the first consumer, as both groups get all messages

Questions:
*Two consumers with the same group id are started. What happens when you runs it?*

Answer:  
When starting two consumers in the same group, they will not receive the same messages, but listen on different partitions, and thus get different messages.

Questions:
*Open [localhost:8080/topics/INGESTION](http://127.0.0.1:8080/topics/INGESTION#consumers). You should now see a table similar to the one below. What does the Lag column mean?*

Answer:
The two groups are seen in the Redpanda web interface, and the lag is the difference between the last message and the current message.

![Redpanda consumer view](solution-images/redpanda-ingestion-consumers.png)

Questions and answers:

- How can we get two consumers to receive identical records?
  - To receive the same records, consumers needs to be in two different groups
- How can we get two consumers to receive unique records?
  - To receive unique records, consumers needs to be in the same group
- What defines the maximum number of active parallel consumers within one consumer group?
  - The number of partitions in the topic defines the maximum number of active parallel consumers within one consumer group. If more consumers are started, they will be idle.

## Exercise 6

This exercise is about creating ksqlDB, with 6 seperate streams based on the sensor id.

Step 1:  
Interactive shell

```bash
kubectl exec --stdin --tty deployment/kafka-ksqldb-cli -- ksql http://kafka-ksqldb-server:8088

                  ===========================================
                  =       _              _ ____  ____       =
                  =      | | _____  __ _| |  _ \| __ )      =
                  =      | |/ / __|/ _` | | | | |  _ \      =
                  =      |   <\__ \ (_| | | |_| | |_) |     =
                  =      |_|\_\___/\__, |_|____/|____/      =
                  =                   |_|                   =
                  =        The Database purpose-built       =
                  =        for stream processing apps       =
                  ===========================================

Copyright 2017-2022 Confluent Inc.

CLI v7.3.1, Server v7.3.1 located at http://kafka-ksqldb-server:8088
Server Status: RUNNING

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql> 
```

Step 2:  
Create a stream over the existing `INGESTION` topic with the following name `STREAM_INGESTION`

SQL for ingestion:

```sql
CREATE STREAM STREAM_INGESTION (
  sensor_id STRING,
  correlation_id STRING,
  modality DOUBLE,
  unit STRING,
  schema_version INTEGER,
  created_at DOUBLE 
) WITH (KAFKA_TOPIC = 'INGESTION', VALUE_FORMAT = 'JSON');
```

Running the SQL:

```bash
ksql> CREATE STREAM STREAM_INGESTION (
>  sensor_id STRING,
>  correlation_id STRING,
>  modality DOUBLE,
>  unit STRING,
>  schema_version INTEGER,
>  created_at DOUBLE
>) WITH (KAFKA_TOPIC = 'INGESTION', VALUE_FORMAT = 'JSON');

 Message
----------------
 Stream created
----------------
```

Step 3:  
Create dedicated channels for each sesnor.  
There are 6 sensors, so there will be created one for each sensor.

The following SQL will be used, with `sensor_id` replaced with the id.

```sql
CREATE STREAM SENSOR_ID_<sensor_id> AS
SELECT
    *
FROM
    STREAM_INGESTION
WHERE
    sensor_id = '<sensor_id>';
```

CREATE STREAM SENSOR_ID_1 AS SELECT * FROM STREAM_INGESTION WHERE sensor_id = '1';

The following is it executed:

```bash
ksql> CREATE STREAM SENSOR_ID_1 AS SELECT * FROM STREAM_INGESTION WHERE sensor_id = '1';

 Message
-------------------------------------------
 Created query with ID CSAS_SENSOR_ID_1_31
-------------------------------------------

ksql> CREATE STREAM SENSOR_ID_2 AS SELECT * FROM STREAM_INGESTION WHERE sensor_id = '2';

 Message
-------------------------------------------
 Created query with ID CSAS_SENSOR_ID_3_33
-------------------------------------------

ksql> CREATE STREAM SENSOR_ID_3 AS SELECT * FROM STREAM_INGESTION WHERE sensor_id = '3';

 Message
-------------------------------------------
 Created query with ID CSAS_SENSOR_ID_3_35
-------------------------------------------

ksql> CREATE STREAM SENSOR_ID_4 AS SELECT * FROM STREAM_INGESTION WHERE sensor_id = '4';

 Message
-------------------------------------------
 Created query with ID CSAS_SENSOR_ID_4_37
-------------------------------------------

ksql> CREATE STREAM SENSOR_ID_5 AS SELECT * FROM STREAM_INGESTION WHERE sensor_id = '5';

 Message
-------------------------------------------
 Created query with ID CSAS_SENSOR_ID_5_39
-------------------------------------------

ksql> CREATE STREAM SENSOR_ID_6 AS SELECT * FROM STREAM_INGESTION WHERE sensor_id = '6';

 Message
-------------------------------------------
 Created query with ID CSAS_SENSOR_ID_6_41
-------------------------------------------
```

Step 4:  
Validate the strems using CLI.

The following SQL can be used:

```sql
SELECT * FROM SENSOR_ID_<sensor_id> EMIT CHANGES;
```

This executed is: 

```bash
ksql> SELECT * FROM SENSOR_ID_1 EMIT CHANGES;
+---------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+       
|SENSOR_ID                              |CORRELATION_ID                         |MODALITY                               |UNIT                                   |SCHEMA_VERSION                         |CREATED_AT                             |       
+---------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+---------------------------------------+       
|1                                      |703a81f1-3ef1-4965-bdc2-2d200b7fb4e7   |-189.2306757625213                     |MW                                     |1                                      |1726861986.969642                      |       
|1                                      |703a81f1-3ef1-4965-bdc2-2d200b7fb4e7   |-312.5373231482345                     |MW                                     |1                                      |1726861988.0925968                     |       
|1                                      |703a81f1-3ef1-4965-bdc2-2d200b7fb4e7   |507.15718794015265                     |MW                                     |1                                      |1726861989.215825                      |
```

## Exercise 7

Step 1:  
Ensure HDFS is running

This can be done by running the service in [serviecs/hdfs](../../services/hdfs/):

```bash
kubectl apply -f ../../services/hdfs/
```

Step 2:  
Setup HDFS 2 sink connector.

This is done using API, since UI does not have all features:

```bash
kubectl port-forward svc/kafka-connect 8083 & 
curl -X POST \
http://127.0.0.1:8083/connectors \
-H 'Content-Type: application/json' \
-d '{
    "name": "hdfs-sink",
    "config": {
        "connector.class": "io.confluent.connect.hdfs.HdfsSinkConnector",
        "tasks.max": "3",
        "topics": "INGESTION",
        "hdfs.url": "hdfs://namenode:9000",
        "flush.size": "3",
        "format.class": "io.confluent.connect.hdfs.json.JsonFormat",
        "key.converter.schemas.enable":"false",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "key.converter.schema.registry.url": "http://kafka-schema-registry:8081", 
        "value.converter.schemas.enable":"false",
        "value.converter.schema.registry.url": "http://kafka-schema-registry:8081", 
        "value.converter": "org.apache.kafka.connect.json.JsonConverter"
    }
}'
```

Result:

```json
{
   "name":"hdfs-sink",
   "config":{
      "connector.class":"io.confluent.connect.hdfs.HdfsSinkConnector",
      "tasks.max":"3",
      "topics":"INGESTION",
      "hdfs.url":"hdfs://namenode:9000",
      "flush.size":"3",
      "format.class":"io.confluent.connect.hdfs.json.JsonFormat",
      "key.converter.schemas.enable":"false",
      "key.converter":"org.apache.kafka.connect.storage.StringConverter",
      "key.converter.schema.registry.url":"http://kafka-schema-registry:8081",
      "value.converter.schemas.enable":"false",
      "value.converter.schema.registry.url":"http://kafka-schema-registry:8081",
      "value.converter":"org.apache.kafka.connect.json.JsonConverter",
      "name":"hdfs-sink"
   },
   "tasks":[
      
   ],
   "type":"sink"
}
```

Step 3:  
Validate the HDFS 2 Sink Connector is working as expected.

For this, we can run the following commands:  

```bash
kubectl exec hdfs-cli -it -- hdfs dfs -ls /topics/
```

Which gives:

```bash
Defaulted container "hadoop" out of: hadoop, init-config (init)
Found 2 items
drwxr-xr-x   - root supergroup          0 2024-09-20 20:25 /topics/+tmp
drwxr-xr-x   - root supergroup          0 2024-09-20 20:27 /topics/INGESTION
```

and

```bash
kubectl exec hdfs-cli -it -- hdfs dfs -ls 
/topics/INGESTION
Defaulted container "hadoop" out of: hadoop, init-config (init)
Found 6 items
drwxr-xr-x   - root supergroup          0 2024-09-20 20:44 /topics/INGESTION/partition=0
drwxr-xr-x   - root supergroup          0 2024-09-20 20:44 /topics/INGESTION/partition=1
drwxr-xr-x   - root supergroup          0 2024-09-20 20:44 /topics/INGESTION/partition=2
drwxr-xr-x   - root supergroup          0 2024-09-20 20:44 /topics/INGESTION/partition=3
drwxr-xr-x   - root supergroup          0 2024-09-20 20:44 /topics/INGESTION/partition=4
drwxr-xr-x   - root supergroup          0 2024-09-20 20:44 /topics/INGESTION/partition=5
```

We can also check logs by doing:

```bash
kubectl exec hdfs-cli -it -- hdfs dfs -ls /logs/
```

Which gives:

```bash
Defaulted container "hadoop" out of: hadoop, init-config (init)
Found 1 items
drwxr-xr-x   - root supergroup          0 2024-09-20 20:27 /logs/INGESTION
```

Question:  
How does HDFS 2 Sink Connector keep up with the six fictive data sources?

Answer:  
When running on a sample rate of 1HZ with 6 sensors, it can keep up, but increasing the sample rate, it takes some time, before the sink catches up.  
But it can catch up, even at 10HZ.