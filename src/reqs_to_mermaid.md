# reqs_to_mermaid.py

A Python script to convert hierarchical requirements in YAML format to a Mermaid `requirementDiagram` for easy visualization.

## Features
- Reads requirements from a YAML file (see `data/reqs.yml`)
- Outputs a Mermaid diagram showing requirements and their relationships
- Supports nested requirements and cross-references (traces, satisfies, refines, derives)

## Usage

1. **Install dependencies** (from the project root):
   ```pwsh
   pip install -r requirements.txt
   ```

2. **Run the script:**
   ```pwsh
   python src/reqs_to_mermaid.py data/reqs.yml docs/reqs.mmd
   ```
   - The first argument is the input YAML file
   - The second argument is the output Mermaid file

3. **View the diagram**
   - Paste the output `.mmd` file into a Mermaid live editor (e.g., https://mermaid.live)
   - Or embed in Markdown using triple-backtick mermaid blocks

## Example
```pwsh
python src/reqs_to_mermaid.py data/reqs.yml docs/reqs.mmd
```

## See Also
- [docs/reqs.md](../docs/reqs.md) — Example Mermaid diagrams
- [data/reqs.yml](../data/reqs.yml) — Example requirements file

# reqs_to_mermaid.py — YAML to Mermaid Converter

## Overview

`reqs_to_mermaid.py` is a command-line Python script that converts a hierarchical requirements YAML file into a Mermaid `requirementDiagram` for easy visualization and documentation.

## Features

- Reads requirements from a YAML file (see `data/reqs.yml`)
- Outputs a Mermaid diagram file (see `docs/reqs.mmd`)
- Supports nested requirements and relationships (contains, traces, satisfies, etc.)
- Warns about unsupported or unknown relationship types

## Usage

```pwsh
python src/reqs_to_mermaid.py data/reqs.yml docs/reqs.mmd
```

- The first argument is the input YAML file
- The second argument is the output Mermaid file

## Example Output

```mermaid
requirementDiagram
requirement "REQ_001" {
  id: REQ_001
  text: "Temperature Control"
}
"REQ_001" -contains-> "REQ_008"
...
```

## Dependencies

- pyyaml

## Tips

- Use the generated `.mmd` file in Markdown docs or with Mermaid live editors
- The script expects the YAML to follow the schema in `schema/reqs-schema.json`
- See the main README for more on requirements structure and schema
