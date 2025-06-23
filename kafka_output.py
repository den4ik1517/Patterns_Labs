from .base import OutputStrategy
import json

class KafkaOutput(OutputStrategy):
    def write(self, data):
        for row in data:
            message = json.dumps(row, indent=2, ensure_ascii=False)
            print("[Kafka] Sent:")
            print(message)
            print('-' * 40)
