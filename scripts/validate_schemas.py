import json
import glob
from jsonschema import validate

# Load the schemas from data_contracts.md (this is a simplified representation)
# In a real scenario, you would parse the markdown or have separate schema files.
schemas = {
    "TestCase": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "input": {"type": "string"},
            "expected": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["id", "input", "expected"]
    }
}

def validate_jsonl(file_path, schema):
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            try:
                instance = json.loads(line)
                validate(instance=instance, schema=schema)
            except Exception as e:
                print(f"Validation failed for {file_path} at line {i+1}: {e}")
                exit(1)
    print(f"Validation passed for {file_path}")

if __name__ == "__main__":
    for file_path in glob.glob("suites/**/*.jsonl", recursive=True):
        # This is a simplification. You would need a way to map file to schema.
        if "examples.jsonl" in file_path:
            validate_jsonl(file_path, schemas["TestCase"])