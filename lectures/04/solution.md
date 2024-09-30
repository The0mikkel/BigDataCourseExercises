# Solution

- [Solution](#solution)
  - [Prerequisits](#prerequisits)
  - [Exercise 1](#exercise-1)
  - [Exercise 2](#exercise-2)
    - [Task 1](#task-1)
    - [Task 2](#task-2)

## Prerequisits

In order to prepare for the exercises, both HDFS and Kafka must be running.

These can be installed from the `services` directory:

```bash
# HDFS
kubectl apply -f ../../services/hdfs/.

# Kafka
helm install --values ../../services/kafka/kafka-values.yaml kafka oci://registry-1.docker.io/bitnamicharts/kafka --version 30.0.4
kubectl apply -f ../../services/kafka/.
```

*Run the above from this directory.*

To access Redpanda, the following can be used:

```bash
kubectl port-forward svc/redpanda 8080:8080
```

## Exercise 1

Deploy spark by using helm:

```bash
helm install --values spark-values.yaml spark oci://registry-1.docker.io/bitnamicharts/spark --version 9.2.10
kubectl port-forward svc/spark-master-svc 8081:80
```

## Exercise 2

### Task 1

First task is to run the `pi-estimation.py` locally.

To do this, we need spark:

```bash
pip install pyspark
```

And then we can run the program:

```bash
$ python3 pi-estimation.py
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/09/23 19:43:51 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Pi is roughly 3.138804
```

We can increase the number of partitions by adding an argument:

```bash
$ python3 pi-estimation.py 10
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/09/23 19:46:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
# [Stage 0:==================================>                       (6 + 1) / 10]
Pi is roughly 3.143432

$ python3 pi-estimation.py 100
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/09/23 19:48:53 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Pi is roughly 3.142264
```

By increasing the partitions, we get a more accurate number, closer to 3.14159.  
It also takes significantly longer to run the script, when increasing the partitions.

### Task 2

Now the Python script is moved into the cluster, to run.

```bash
# Forward spark web interface
kubectl port-forward svc/spark-master-svc 8081:80

# Create interactive container
kubectl run spark-interactive --image python:bookworm -it -- bash
 
# In the interactive container
apt update && apt install nano default-jre # Install nano for copying files and java for spark
pip install pyspark

# Copy files over, needed for exercise (pi-estimation.py & src/utils.py)
# Remember to change LOCAL to K8S for spark context in pi-estimation.py

# Now we can run the same examples
spark-submit pi-estimation.py 10

# However, the process fails:
24/09/29 20:06:33 INFO StandaloneAppClient$ClientEndpoint: Executor updated: app-20240929200614-0004/8 is now RUNNING
Traceback (most recent call last):
  File "/pi-estimation.py", line 24, in <module>
    count = sc.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/pyspark/python/lib/pyspark.zip/pyspark/rdd.py", line 1924, in reduce
  File "/usr/local/lib/python3.12/site-packages/pyspark/python/lib/pyspark.zip/pyspark/rdd.py", line 1833, in collect
  File "/usr/local/lib/python3.12/site-packages/pyspark/python/lib/py4j-0.10.9.7-src.zip/py4j/java_gateway.py", line 1322, in __call__
  File "/usr/local/lib/python3.12/site-packages/pyspark/python/lib/pyspark.zip/pyspark/errors/exceptions/captured.py", line 179, in deco        
  File "/usr/local/lib/python3.12/site-packages/pyspark/python/lib/py4j-0.10.9.7-src.zip/py4j/protocol.py", line 326, in get_return_value       
py4j.protocol.Py4JJavaError: An error occurred while calling z:org.apache.spark.api.python.PythonRDD.collectAndServe.
: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 4 times, most recent failure: Lost task 0.3 in stage 0.0 (TID 6) (10.1.155.83 executor 6): ExecutorLostFailure (executor 6 exited caused by one of the running tasks) Reason: Command exited with code 50
Driver stacktrace:
        at org.apache.spark.scheduler.DAGScheduler.failJobAndIndependentStages(DAGScheduler.scala:2856)
        at org.apache.spark.scheduler.DAGScheduler.$anonfun$abortStage$2(DAGScheduler.scala:2792)
        at org.apache.spark.scheduler.DAGScheduler.$anonfun$abortStage$2$adapted(DAGScheduler.scala:2791)
        at scala.collection.mutable.ResizableArray.foreach(ResizableArray.scala:62)
        at scala.collection.mutable.ResizableArray.foreach$(ResizableArray.scala:55)
        at scala.collection.mutable.ArrayBuffer.foreach(ArrayBuffer.scala:49)
        at org.apache.spark.scheduler.DAGScheduler.abortStage(DAGScheduler.scala:2791)
        at org.apache.spark.scheduler.DAGScheduler.$anonfun$handleTaskSetFailed$1(DAGScheduler.scala:1247)
        at org.apache.spark.scheduler.DAGScheduler.$anonfun$handleTaskSetFailed$1$adapted(DAGScheduler.scala:1247)
        at scala.Option.foreach(Option.scala:407)
        at org.apache.spark.scheduler.DAGScheduler.handleTaskSetFailed(DAGScheduler.scala:1247)
        at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.doOnReceive(DAGScheduler.scala:3060)
        at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2994)
        at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2983)
        at org.apache.spark.util.EventLoop$$anon$1.run(EventLoop.scala:49)
        at org.apache.spark.scheduler.DAGScheduler.runJob(DAGScheduler.scala:989)
        at org.apache.spark.SparkContext.runJob(SparkContext.scala:2393)
        at org.apache.spark.SparkContext.runJob(SparkContext.scala:2414)
        at org.apache.spark.SparkContext.runJob(SparkContext.scala:2433)
        at org.apache.spark.SparkContext.runJob(SparkContext.scala:2458)
        at org.apache.spark.rdd.RDD.$anonfun$collect$1(RDD.scala:1049)
        at org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:151)
        at org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:112)
        at org.apache.spark.rdd.RDD.withScope(RDD.scala:410)
        at org.apache.spark.rdd.RDD.collect(RDD.scala:1048)
        at org.apache.spark.api.python.PythonRDD$.collectAndServe(PythonRDD.scala:195)
        at org.apache.spark.api.python.PythonRDD.collectAndServe(PythonRDD.scala)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:569)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:840)
```

Due to failure, the spark job on cluster could not be completed.  
Therefore, the exercise cannot be completed.

Further debugging has not been done, due to time constraints.
