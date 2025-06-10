# vibe-sandbox

This repository is a Python sandbox for requirements management and visualization, including a Streamlit-based requirements editor and tools for working with hierarchical YAML requirements.

## Project Structure

- `src/` — Python source code and tools
  - `reqs_tool.py` — Streamlit app for editing and visualizing requirements
  - `reqs_to_mermaid.py` — Convert YAML requirements to Mermaid diagrams
  - `reqs_tool.md` — Detailed usage and documentation for the Streamlit tool
  - `reqs_to_mermaid.md` — Detailed usage and documentation for the Mermaid export script
- `data/` — Example and working requirements YAML files
- `schema/` — JSON/YAML schema for requirements validation
- `docs/` — Documentation and example diagrams
- `tools/` — Utility scripts (e.g., Windows batch launcher)
- `archive/` — Old/legacy versions of tools

## Setup Instructions

1. **Create and activate a virtual environment:**
   
   ```pwsh
   ./setup.ps1
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   
   ```pwsh
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   
   ```pwsh
   streamlit run src/reqs-tool.py
   ```
   Or use the batch file:
   ```pwsh
   ./tools/reqs.bat
   ```

4. **Convert requirements YAML to Mermaid diagram:**
   
   ```pwsh
   python src/reqs_to_mermaid.py data/reqs.yml docs/reqs.mmd
   ```

## Dependencies
- streamlit
- pyyaml
- jsonschema
- streamlit-tree-select

## Notes
- Place your requirements YAML files in `data/`.
- Place schema files in `schema/`.
- Old versions of scripts are in `archive/` for reference.

## Project Schema

The requirements YAML files are validated against a schema defined in `schema/reqs_schema.json` (JSON) and `schema/reqs_schema.yml` (YAML).

### Schema Highlights

- **requirements**: Top-level array of requirement objects
- **project**: Optional project metadata (code, summary, references)
- **requirement**: Each requirement has an `id`, `title`, `description`, and may include:
  - `tags`: List of tags for filtering/classification
  - `status`: Implementation/validation flags
  - `cross_references`: Dependency and traceability links
  - `children`: Nested requirements
  - `external_references`: Document IDs, URLs, tickets
  - `acceptance_criteria`, `linked_features`, `rationale`, `verification`, `priority`, etc.

See the schema files for full details and required/optional fields.

---

For more, see the example files in `docs/` and `data/`.

# Changelog

## [Unreleased]

### Changed

- `reqs-tool.py` → `reqs_tool.py`
- `reqs-tool-old.py` → `reqs_tool_old.py`
- `reqs-tool-old1.py` → `reqs_tool_old1.py`
- `reqs_to_mermaid.py` (already snake_case)
- Update all references in README and docs to use snake_case.
