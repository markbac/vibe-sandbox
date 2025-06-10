# filepath: src/reqs_to_mermaid.py
#!/usr/bin/env python3

import argparse
import yaml
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_mermaid(requirements):
    lines = ["requirementDiagram"]
    id_map = {}

    def add_block(req):
        rid = req["id"]
        text = req.get("title", req.get("text", "")).replace('"', "'")
        id_map[rid] = f'"{rid}"'
        lines.append(f'requirement "{rid}" {{')
        lines.append(f'  id: {rid}')
        lines.append(f'  text: "{text}"')
        lines.append("}")

        for child in req.get("children", []):
            add_block(child)
            lines.append(f'{id_map[rid]} -contains-> {id_map[child["id"]]}')

            for rel_type, targets in child.get("cross_references", {}).items():
                rel_map = {
                    "traces": "traces",
                    "satisfies": "satisfies",
                    "refines": "refines",
                    "derives": "derives"
                }
                if rel_type not in rel_map:
                    logging.warning(f"Unsupported relationship type: {rel_type}")
                    continue
                for target in targets:
                    lines.append(f'{id_map[child["id"]]} -{rel_map[rel_type]}-> "{target}"')

    for top_req in requirements.get("requirements", []):
        add_block(top_req)

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Convert YAML requirements to Mermaid requirementDiagram format.")
    parser.add_argument("input_yaml", type=Path, help="Path to the YAML input file")
    parser.add_argument("output_mmd", type=Path, help="Path to the output .mmd Mermaid file")
    args = parser.parse_args()

    if not args.input_yaml.exists():
        logging.error(f"Input file does not exist: {args.input_yaml}")
        return

    with open(args.input_yaml, "r", encoding="utf-8") as f:
        requirements = yaml.safe_load(f)

    logging.info(f"Loaded requirements from {args.input_yaml}")
    mermaid_output = generate_mermaid(requirements)

    with open(args.output_mmd, "w", encoding="utf-8") as f:
        f.write(mermaid_output)

    logging.info(f"Mermaid diagram written to {args.output_mmd}")

if __name__ == "__main__":
    main()
