from sensor import Sensor
from client import Client
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
readerNode = os.getenv("READER", False)

kafka_topic = os.getenv("KAFKA_TOPIC", "INGESTION")

# Main data handling
sensor_threads = {}

# Define root handling of sensors
def save_data(data):
    logger.info(f"Sending data: {data} to Kafka topic {kafka_topic}")
    client.send_msg(data, str(data.sensor_id), kafka_topic)
    sensor_threads[data.sensor_id] = {
        "thread": sensor_threads[data.sensor_id]["thread"],
        "health": True,
        "output": str(data)
    }

def start_sensor(sensorId):
    logger.debug(f"Starting sensor {sensorId}")
    logger.debug(f"Correlation ID: {correlationId}")
    logger.debug(f"Sample rate: {sampleRate}")
        
    sensor = Sensor(sensorId, correlationId, sampleRate, save_data)
    sensor.start_listening()

def check_sensors_health():
    logger.debug("Checking sensors thread health")
    for sensorId, data in sensor_threads.items():
        if not data["thread"].is_alive():
            try:
                logger.warning(f"Sensor {sensorId} is not alive, starting it again")
                data["thread"].start()
            except:
                # Modify entry in the list, such that health is false
                sensor_threads[sensorId] = {
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
    
    for sensorId, data in sensor_threads.items():
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
    for sensorId, data in sensor_threads.items():
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


# Prepare sensors
if not readerNode:
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
        sensor_threads[sensorId] = {
            "thread": thread,
            "health": True,
            "output": None
        }
    
    logger.info("Sensors started")

if readerNode:
    sensors = []
    logger.info("Running in reader mode")

if __name__ == "__main__":
    # Start webserver
    logger.info("Starting webserver")
    app.run(host="0.0.0.0", port=5000, debug=True)
    logger.info("Webserver started")
    
    if not readerNode:
        # Wait for threads to finish
        for sensorId, data in sensor_threads.items():
            data["thread"].join()
            
        logger.info("All threads finished - This indicates a problem")
        
        # Exit
        exit(1)