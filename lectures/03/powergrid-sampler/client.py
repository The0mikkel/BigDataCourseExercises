import json

from data_model import PackageObj, generate_sample
from kafka import KafkaConsumer, KafkaProducer

# Format <pod name>.<service name>:<port>
KAFKA_BOOTSTRAP: list[str] = ["kafka:9092"]

DEFAULT_TOPIC: str = "INGESTION"
DEFAULT_ENCODING: str = "utf-8"
DEFAULT_CONSUMER: str = "DEFAULT_CONSUMER"

def get_producer() -> KafkaProducer:
    return KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)

def get_consumer(topic: str, group_id: str = None) -> KafkaConsumer:
    if group_id is None:
        group_id = DEFAULT_CONSUMER
    return KafkaConsumer(topic, bootstrap_servers=KAFKA_BOOTSTRAP, group_id=group_id)


class Client:
    def send_msg(value, key: str, topic: str, producer: KafkaProducer) -> None:
        if not producer:
            producer = get_producer()
            
        if not topic:
            topic = DEFAULT_TOPIC
        
        producer.send(
            topic=topic,
            key=key.encode(DEFAULT_ENCODING),
            value=json.dumps(value).encode(DEFAULT_ENCODING),
        )
