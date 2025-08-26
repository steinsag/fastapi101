import os


def kafka_config_producer() -> dict[str, str]:
    return {
        "bootstrap.servers": os.environ["KAFKA_ENDPOINT"],
        "sasl.username": os.environ["KAFKA_USERNAME"],
        "sasl.password": os.environ["KAFKA_PASSWORD"],
        "security.protocol": os.environ["KAFKA_SECURITY_PROTOCOL"],
        "sasl.mechanisms": "PLAIN",
        "acks": "all",
    }
