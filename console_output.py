from .base import OutputStrategy
import json

class ConsoleOutput(OutputStrategy):
    def write(self, data):
        for row in data:
            print(json.dumps(row, indent=2, ensure_ascii=False))
            print('-' * 40)
