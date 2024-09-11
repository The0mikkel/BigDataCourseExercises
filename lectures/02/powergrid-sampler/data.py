import time

class SensorData:
    def __init__(self, sensor_id, correlation_id, modality, unit, temporal_aspect, schema_version=1, created_at=None):
        self.sensor_id = sensor_id
        self.correlation_id = correlation_id
        self.modality = modality
        self.unit = unit
        self.temporal_aspect = temporal_aspect
        self.schema_version = schema_version or 1
        self.created_at = created_at or time.time()
        
    def __str__(self):
        return f"SensorData {self.sensor_id} with correlation id {self.correlation_id} and modality {self.modality} {self.unit}"
    
    def getSensorId(self):
        # Return as string
        return str(self.sensor_id)
    
    def getCorrelationId(self):
        # Return as string
        return str(self.correlation_id)
    
    def getModality(self):
        # Return as double
        return float(self.modality)

    def getUnit(self):
        # Return as string
        return str(self.unit)

    def getTemporalAspect(self):
        # Return as string
        return str(self.temporal_aspect)
    
    def getSchemaVersion(self):
        # Return as integer
        return int(self.schema_version)
    
    def getCreatedAt(self):
        # Return as double
        return float(self.created_at)
    
    def toObject(self):
        return {
            "sensor_id": self.getSensorId(),
            "correlation_id": self.getCorrelationId(),
            "modality": self.getModality(),
            "unit": self.getUnit(),
            "temporal_aspect": self.getTemporalAspect(),
            "schema_version": self.getSchemaVersion(),
            "created_at": self.getCreatedAt()
        }
    