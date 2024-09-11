import random
import time
import threading

from data import SensorData

# Mocking values
VALID_RANGE = (-600, 600)

# class Sensor:
class Sensor:
    def __init__(self, id, correlation_id, sample_rate, callback=None):
        self.id = id
        self.correlation_id = correlation_id
        self.sample_rate = sample_rate
        self.callback = callback
        self.listen = False

    def __str__(self):
        return f"Sensor {self.id} with sample rate {self.sample_rate}"

    def __repr__(self):
        return f"Sensor({self.id}, {self.sample_rate})"

    def __eq__(self, other):
        return self.id == other.id and self.sample_rate == other.sample_rate

    '''
    Get reading of sensor in -+600 MW in double type
    '''
    def pull_reading(self):
        # Generate random value within valid range
        return random.uniform(*VALID_RANGE)

    '''
    Register callback to call for each reading of sample rate
    '''
    def register_callback(self, callback):
        self.callback = callback
        print(f"Callback {callback} registered")

    '''
    Start listening for readings
    '''
    def start_listening(self):
        if not self.callback:
            raise ValueError("Callback not registered")
        
        self.listen = True
        print("Listening started")
        while self.listen:
            reading = self.pull_reading()
            self.callback(SensorData(self.id, self.correlation_id, reading, "MW", "real_time"))
            
            # Ensure sample rate, which is of how many samples per second (Hz)
            time.sleep(1 / self.sample_rate)

    '''
    Stop listening for readings
    '''
    def stop_listening(self):
        self.listen = False
        print("Listening stopped")

if __name__ == "__main__":
    # Create a sensor
    sensor = Sensor(1, 10)
    print(sensor)
    
    # Pull a reading
    print(sensor.pull_reading())
    
    # Pull 10 readings
    for _ in range(10):
        print(sensor.pull_reading())
        
    print("Registering callback")
    sensor.register_callback(print)
    
    threading.Thread(target=sensor.start_listening).start()
    
    print("Listening for 5 seconds")
    time.sleep(5)
    sensor.stop_listening()
    print("Done")
    