# reqs_tool.py — Streamlit Requirements Editor

## Overview

`reqs_tool.py` is an interactive Streamlit web app for creating, editing, and visualizing hierarchical requirements stored in YAML format. It supports project-level metadata, validation against a schema, and advanced features like cross-references and traceability.

## Features

- Upload, view, and edit requirements YAML files
- Hierarchical (parent/child) requirements tree
- Add, edit, and delete requirements interactively
- Cross-reference and traceability support
- Project metadata display
- Schema validation (using `schema/reqs-schema.json`)
- Export and download updated YAML

## Usage

1. **Start the app:**

   ```pwsh
   streamlit run src/reqs_tool.py
   ```
   Or use the batch file:
   ```pwsh
   ./tools/reqs.bat
   ```

2. **Upload a requirements YAML file** (or start from scratch)

3. **Browse and edit** the requirements tree in the sidebar

4. **Edit details** for any selected requirement

5. **Add child or top-level requirements** as needed

6. **Download/export** the updated YAML file

## File Structure

- Requirements YAML files: `data/`
- Schema: `schema/reqs-schema.json`
- Example docs: `docs/`

## Dependencies

- streamlit
- pyyaml
- jsonschema
- streamlit-tree-select

## Tips

- Use the schema for validation to ensure your requirements files are well-formed.
- All changes are in-memory until you export/download the YAML.
- See the main README for more on the schema and project structure.
