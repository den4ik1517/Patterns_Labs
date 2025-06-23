from .base import OutputStrategy
import json

class RedisOutput(OutputStrategy):
    def write(self, data):
        for row in data:
            key = row.get("Service Number ID", "unknown")
            value = json.dumps(row, indent=2, ensure_ascii=False)
            print(f"[Redis] Stored key: {key}")
            print(value)
            print('-' * 40)
