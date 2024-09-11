from sensor import Sensor
from client import Client
from data import SensorData
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

# HDFS client
client = Client()

# Prepare data for the webserver
sensorId = os.getenv("SENSOR_ID", random.randint(1, 100))
sensors = os.getenv("SENSORS", "")
correlationId = os.getenv("CORRELATION_ID", uuid.uuid4())
sampleRate = os.getenv("SAMPLE_RATE", 1)

# Main data handling
sensor_threads = {}

# Define root handling of sensors
def save_data(data):
    # Convert float to date
    date = datetime.datetime.fromtimestamp(data.created_at).strftime('%Y-%m-%d')
    path = f"/powergrid/elecricity_lines/wattage_offset/{data.sensor_id}/{data.temporal_aspect}/{date}/{data.correlation_id}.parquet"
    logger.info(f"Saving data: {data} to HDFS ({path})")
    client.append(path, data)
    sensor_threads[data.sensor_id] = (sensor_threads[data.sensor_id][0], sensor_threads[data.sensor_id][1], data.modality)
        
def start_sensor(sensorId):
    logger.debug(f"Starting sensor {sensorId}")
    logger.debug(f"Correlation ID: {correlationId}")
    logger.debug(f"Sample rate: {sampleRate}")
        
    sensor = Sensor(sensorId, correlationId, sampleRate, save_data)
    sensor.start_listening()

def check_sensors_health():
    logger.debug("Checking sensors thread health")
    for sensorId, (thread, health, output) in sensor_threads.items():
        if not thread.is_alive():
            try:
                logger.warning(f"Sensor {sensorId} is not alive, starting it again")
                thread.start()
            except:
                # Modify entry in the list, such that health is false
                sensor_threads[sensorId] = (thread, False, output)
                

@app.route("/sensors")
def get_sensors():
    # Get sensors, based on the sensor threads
    response = {
        "correlation_id": correlationId,
        "sensors": []
    }
    
    for sensorId, (thread, health, output) in sensor_threads.items():
        response["sensors"].append({
            "sensor_id": sensorId,
            "healthy": health,
            "reading": output
        })
    
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
    for sensorId, (thread, health, current_output) in sensor_threads.items():
        response["sensors"].append({
            "sensor_id": sensorId,
            "healthy": health
        })
        if not health:
            health = False
        
    # if any sensor is unhealthy, return status code 500
    status_code = 200 if health else 500
    
    return jsonify(response), status_code

@app.route("/")
def home():
    return "Sensor API"

logger.info("Starting sensors")

# Prepare sensors
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
    sensor_threads[sensorId] = (thread, True, 0)
    
logger.info("Sensors started")

if __name__ == "__main__":
    # Start webserver
    logger.info("Starting webserver")
    app.run(host="0.0.0.0", port=5000, debug=True)
    logger.info("Webserver started")
