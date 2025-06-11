# reqs_tool.py — Streamlit Requirements Editor

## Overview

`reqs_tool.py` is an interactive Streamlit web app for creating, editing, and visualizing hierarchical requirements in YAML format. It supports project-level metadata, schema validation, and advanced features like cross-references, traceability, and exporting requirements.

## Features

- **Tree View:** Browse and expand/collapse a hierarchical requirements tree in the sidebar.
- **Single-Select Editing:** Select a requirement to view and edit all its fields, including nested/complex types, using a UI auto-generated from the schema.
- **Add Child Requirements:** Add child requirements to any selected requirement.
- **Add Top-Level Requirements:** Deselect all to add a new top-level requirement.
- **Project Metadata:** Edit project-level metadata in the sidebar.
- **Schema Validation:** All requirements are validated against the JSON schema.
- **Export:** Download the current requirements and project metadata as a YAML file.

## How to Use

1. **Start the App:**

   ```pwsh
   streamlit run src/reqs-tool.py
   ```
   Or use the batch file:
   ```pwsh
   ./tools/reqs.bat
   ```

2. **Upload Requirements YAML:**

   - Use the sidebar to upload an existing requirements YAML file, or start from scratch.

3. **Browse and Edit:**

   - Use the sidebar tree to select a requirement for editing.
   - Edit all fields, including arrays and objects, in the main panel.
   - Add child requirements to any selected requirement.
   - Deselect all to add a new top-level requirement.

4. **Edit Project Metadata:**

   - Use the sidebar form to edit project-level fields (name, version, summary, etc).

5. **Export:**

   - Use the export section to download the current requirements and metadata as a YAML file.

## Notes

- Only one requirement can be selected at a time for editing.
- The UI is dynamically generated from the schema, so it adapts to schema changes.
- All changes are in-memory until you export/download the YAML.
- See the main README and schema files for more details on requirements structure.
