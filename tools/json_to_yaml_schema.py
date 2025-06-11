#!/usr/bin/env python3
"""
Script to convert the JSON requirements schema to YAML format.
Usage:
    python tools/json_to_yaml_schema.py
"""
import json
import yaml
from pathlib import Path

json_path = Path(__file__).parent.parent / "schema" / "reqs-schema.json"
yaml_path = Path(__file__).parent.parent / "schema" / "reqs-schema.yml"

def main():
    with open(json_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(schema, f, sort_keys=False, allow_unicode=True)
    print(f"Converted {json_path} to {yaml_path}")

if __name__ == "__main__":
    main()
