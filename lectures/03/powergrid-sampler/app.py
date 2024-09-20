from sensor import Sensor
from client import Client, get_consumer, get_producer
from threading import Thread
from flask import Flask, jsonify

import datetime
import random
import os
import uuid
import logging

logger = logging.getLogger('gunicorn.error')

# Webserver app
app = Flask(__name__)

app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

# Client
client = Client()

# Prepare data for the webserver
sensorId = os.getenv("SENSOR_ID", random.randint(1, 100))
sensors = os.getenv("SENSORS", "")
correlationId = os.getenv("CORRELATION_ID", uuid.uuid4())
sampleRate = os.getenv("SAMPLE_RATE", 1)

kafka_topic = os.getenv("KAFKA_TOPIC", "INGESTION")
consumerNode = os.getenv("CONSUMER_NODE", False)
group_id = os.getenv("GROUP_ID", "DEFAULT_CONSUMER")

# Main data handling
sensor_readings = {}

# Define root handling of sensors
def save_data(data):
    logger.info(f"Sending data: {data} to Kafka topic {kafka_topic}")
    client.send_msg(data, str(data.sensor_id), kafka_topic)
    sensor_readings[data.sensor_id] = {
        "thread": sensor_readings[data.sensor_id]["thread"],
        "health": True,
        "output": str(data)
    }

def process_data(data):
    logger.info(f"Processing data: {data}")
    
    sensor_readings[data.sensor_id] = {
        "thread": None,
        "health": True,
        "output": str(data)
    }
    
    return data

def start_sensor(sensorId):
    logger.debug(f"Starting sensor {sensorId}")
    logger.debug(f"Correlation ID: {correlationId}")
    logger.debug(f"Sample rate: {sampleRate}")
    
    sensor = Sensor(sensorId, correlationId, sampleRate, save_data)
    sensor.start_listening()

def read_sensor():
    # Process data
    logger.debug(f"Reading sensor data from Kafka topic {kafka_topic}")
    client.recive_msg(process_data, get_consumer(kafka_topic, group_id=group_id))

def check_sensors_health():
    if consumerNode:
        return
    
    logger.debug("Checking sensors thread health")
    for sensorId, data in sensor_readings.items():
        if not data["thread"].is_alive():
            try:
                logger.warning(f"Sensor {sensorId} is not alive, starting it again")
                data["thread"].start()
            except:
                # Modify entry in the list, such that health is false
                sensor_readings[sensorId] = {
                    "thread": data["thread"],
                    "health": False,
                    "output": None
                }


@app.route("/sensors")
def get_sensors():
    # Get sensors, based on the sensor threads
    response = {
        "correlation_id": correlationId,
        "sensors": []
    }

    for sensorId, data in sensor_readings.items():
        response["sensors"] = {
            "sensor_id": str(sensorId or "Unknown"),
            "health": str(data["health"] or False),
            "output": str(data["output"] or "No data")
        }

    return jsonify(response)

@app.route("/_status/healthz")
def get_health():
    # Check sensor healths, and create a json response for each sensor, and the correlation id of this instance
    check_sensors_health()

    response = {
        "correlation_id": correlationId,
        "sensors": []
    }

    health = True
    for sensorId, data in sensor_readings.items():
        response["sensors"] = {
            "sensor_id": str(sensorId or "Unknown"),
            "healthy": str(data["health"] or False)
        }
        if not data["health"]:
            health = False

    # if any sensor is unhealthy, return status code 500
    status_code = 200 if health else 500

    return jsonify(response), status_code

@app.route("/")
def home():
    return "Sensor API"


# Producer setup
if not consumerNode:
    logger.info("Starting sensors")
    logger.debug(f"Sensor ID: {sensorId}")
    logger.debug(f"Sensors: {sensors}")
    if sensors != "":
        sensors = sensors.split(",")
    else:
        sensors = [sensorId]

    # Start sensors
    for sensorId in sensors:
        thread = Thread(target = start_sensor, args = [sensorId])
        thread.start()
        sensor_readings[sensorId] = {
            "thread": thread,
            "health": True,
            "output": None
        }

    logger.info("Sensors started")

# Consumer setup
if consumerNode:
    sensors = []
    logger.info("Running in consumer mode")
    
    while True:
        read_sensor()
    
    exit(1)

if __name__ == "__main__":
    # Start webserver
    logger.info("Starting webserver")
    app.run(host="0.0.0.0", port=5000, debug=True)
    logger.info("Webserver started")

    if not consumerNode:
        # Wait for threads to finish
        for sensorId, data in sensor_readings.items():
            data["thread"].join()

        logger.info("All threads finished - This indicates a problem")

        # Exit
        exit(1)
