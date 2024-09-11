from sensor import Sensor
from client import Client
from data import SensorData
from threading import Thread
from flask import Flask, jsonify

import datetime
import random
import os
import uuid

# Webserver app
app = Flask(__name__)

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
    print(f"Saving data: {data} to HDFS ({path})")
    client.append(path, data)
    sensor_threads[data.sensor_id] = (sensor_threads[data.sensor_id][0], sensor_threads[data.sensor_id][1], data.modality)
        
def start_sensor(sensorId):
    print(f"Starting sensor {sensorId}")
    print(f"Correlation ID: {correlationId}")
    print(f"Sample rate: {sampleRate}")
        
    sensor = Sensor(sensorId, correlationId, sampleRate, save_data)
    sensor.start_listening()

def check_sensors_health():
    print("Checking sensors thread health")
    for sensorId, (thread, health) in sensor_threads.items():
        if not thread.is_alive():
            try:
                print(f"Sensor {sensorId} is not alive, starting it again")
                thread.start()
            except:
                # Modify entry in the list, such that health is false
                sensor_threads[sensorId] = (thread, False)
                

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
def get_sensors():
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


if __name__ == "__main__":
    # Prepare sensors
    if sensors != "":
        sensors = sensors.split(",")
    else:
        sensors = [sensorId]
    
    # Start sensors
    for sensorId in sensors:
        thread = Thread(target = start_sensor, args = [sensorId])
        thread.start()
        sensor_threads[sensorId] = (thread, True, 0)

    # Start webserver
    app.run()
