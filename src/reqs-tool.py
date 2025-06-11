# filepath: src/reqs-tool.py
import json
from jsonschema.exceptions import ValidationError
from datetime import datetime
from streamlit_tree_select import tree_select
import streamlit as st
import yaml
import logging
import io
import csv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

# Load schema and validate YAML
def load_schema():
    with open("schema/reqs-schema.json", "r", encoding="utf-8") as schema_file:
        return json.load(schema_file)

def validate_requirements(data, schema):
    import jsonschema
    from jsonschema.exceptions import ValidationError
    try:
        jsonschema.validate(instance=data, schema=schema)
    except ValidationError as e:
        st.error(f"Schema validation error: {e.message}")
        return False
    return True

# Util to generate sequential requirement IDs
def generate_req_id():
    if "req_id_counter" not in st.session_state:
        st.session_state.req_id_counter = 1
    req_id = f"REQ_{st.session_state.req_id_counter:03}"
    st.session_state.req_id_counter += 1
    return req_id

# Load existing YAML
st.sidebar.header("\U0001F4C2 Upload existing YAML")
uploaded_file = st.sidebar.file_uploader("Upload requirements YAML", type=["yaml", "yml"])

if uploaded_file and not st.session_state.get("uploaded", False):
    logger.debug("\U0001F4C1 YAML file uploaded, attempting to parse")
    st.session_state.yaml_filename = uploaded_file.name
    requirements_data = yaml.safe_load(uploaded_file)
    validate_requirements(requirements_data)
    st.session_state.requirements = requirements_data.get("requirements", [])
    st.session_state.project = requirements_data.get("project", {})
    st.session_state.uploaded = True
    logger.debug(f"✅ Loaded requirements: {len(st.session_state.requirements)} top-level entries")
elif "requirements" not in st.session_state:
    st.session_state.requirements = []
    st.session_state.project = {}

# Recursive functions to handle requirements
def find_req_by_id(reqs, target_id):
    for req in reqs:
        if req.get("id") == target_id:
            return req
        result = find_req_by_id(req.get("children", []), target_id)
        if result:
            return result
    return None

def find_parent(reqs, target_id, parent=None):
    for req in reqs:
        if req.get("id") == target_id:
            return parent
        result = find_parent(req.get("children", []), target_id, req)
        if result:
            return result
    return None

def convert_to_tree_format(reqs):
    def convert(req):
        return {
            "label": f"{req.get('id', '')} - {req.get('title', '')}",
            "value": req.get('id', ''),
            "children": [convert(child) for child in req.get("children", [])]
        }
    return [convert(req) for req in reqs]

# Sidebar: Tree selection
with st.sidebar:
    st.subheader("\U0001F4CB Requirement Tree")
    tree_data = convert_to_tree_format(st.session_state.requirements)
    try:
        tree_response = tree_select(
            tree_data,
            checked=[],
            expand_on_click=True,
            multiple=False  # Explicitly disallow multiple selection
        )
        selected_id = None
        # Only allow one selection at a time
        if tree_response and tree_response.get("selected"):
            # If more than one is selected, only keep the last one
            if isinstance(tree_response["selected"], list) and len(tree_response["selected"]) > 1:
                selected_id = tree_response["selected"][-1]
            else:
                selected_id = tree_response["selected"][0]
            # Deselect any previous selection
            st.session_state.selected_req_id = selected_id
    except Exception as e:
        selected_id = None

# Get all requirement IDs
all_req_ids = []
def collect_req_ids(reqs):
    for req in reqs:
        all_req_ids.append(req.get("id"))
        collect_req_ids(req.get("children", []))

collect_req_ids(st.session_state.requirements)

# Mirror a cross-reference relation in the opposite direction
def mirror_cross_reference(source_id, target_id, key):
    target = find_req_by_id(st.session_state.requirements, target_id)
    if not target:
        return
    reverse_key = {
        "depends_on": "required_by",
        "related_to": "related_to",
        "conflicts_with": "conflicts_with",
        "duplicated_by": "duplicates"
    }.get(key)
    if not reverse_key:
        return
    target.setdefault("cross_references", {}).setdefault(reverse_key, [])
    if source_id not in target["cross_references"][reverse_key]:
        target["cross_references"][reverse_key].append(source_id)
        target["cross_references"][reverse_key] = list(set(target["cross_references"][reverse_key]))

# Add child requirement
def add_child_requirement(parent_req):
    with st.form(f"add_child_form_{parent_req['id']}"):
        pass

# Dynamically generate Streamlit fields for a requirement based on the schema
def render_requirement_fields(req, schema, prefix=""):
    fields = {}
    req_schema = schema["$defs"]["requirement"]["properties"]
    for field, props in req_schema.items():
        key = f"{prefix}{field}"
        value = req.get(field, None)
        field_type = props.get("type", "string")
        enum = props.get("enum")
        desc = props.get("description", "")
        if enum:
            fields[field] = st.selectbox(f"{field} ({desc})", enum, index=enum.index(value) if value in enum else 0, key=key)
        elif field_type == "boolean":
            fields[field] = st.checkbox(f"{field} ({desc})", value=bool(value), key=key)
        elif field_type == "array":
            items_type = props.get("items", {}).get("type")
            if items_type == "string":
                fields[field] = st.text_area(f"{field} (comma-separated) ({desc})", value=", ".join(value or []), key=key).split(", ") if value is not None else []
            elif items_type == "object":
                # For arrays of objects (e.g., comments, external_references)
                arr = value or []
                st.markdown(f"**{field}** ({desc})")
                arr_fields = []
                for i, item in enumerate(arr):
                    st.markdown(f"*Entry {i+1}*")
                    item_fields = {}
                    for subfield, subprops in props["items"].get("properties", {}).items():
                        subkey = f"{key}_{i}_{subfield}"
                        item_fields[subfield] = st.text_input(f"{subfield}", item.get(subfield, ""), key=subkey)
                    arr_fields.append(item_fields)
                fields[field] = arr_fields
            else:
                fields[field] = value or []
        elif field_type == "object":
            # For custom/metadata/status/cross_references/traceability
            st.markdown(f"**{field}** ({desc})")
            obj = value or {}
            obj_fields = {}
            for subfield, subprops in props.get("properties", {}).items():
                subkey = f"{key}_{subfield}"
                subval = obj.get(subfield, "")
                if subprops.get("type") == "boolean":
                    obj_fields[subfield] = st.checkbox(f"{subfield}", value=bool(subval), key=subkey)
                elif subprops.get("type") == "array":
                    obj_fields[subfield] = st.text_area(f"{subfield} (comma-separated)", value=", ".join(subval or []), key=subkey).split(", ") if subval is not None else []
                else:
                    obj_fields[subfield] = st.text_input(f"{subfield}", subval, key=subkey)
            fields[field] = obj_fields
        else:
            fields[field] = st.text_input(f"{field} ({desc})", value or "", key=key)
    return fields

schema = load_schema()

# Main panel
st.title("\U0001F4CB YAML Requirements Builder")

if st.session_state.project.get("summary"):
    st.info(f"**Project:** {st.session_state.project.get('name', '')}\n\n**Summary:** {st.session_state.project['summary']}")

if "selected_req_id" in st.session_state and st.session_state.selected_req_id:
    selected_req = find_req_by_id(st.session_state.requirements, st.session_state.selected_req_id)
    parent_req = find_parent(st.session_state.requirements, st.session_state.selected_req_id)

    logger.debug(f"🛠 Editing requirement: {selected_req}")

    st.subheader("📝 Requirement Details")
    with st.form("edit_req_form"):
        updated_fields = render_requirement_fields(selected_req, schema)
        submitted = st.form_submit_button("Save Changes")
        if submitted:
            for k, v in updated_fields.items():
                selected_req[k] = v
            st.success("Requirement updated.")

    st.subheader("➕ Add Child Requirement")
    with st.form("add_child_form"):
        child_fields = render_requirement_fields({}, schema, prefix="child_")
        add_child = st.form_submit_button("Add Child")
        if add_child:
            child_req = {k: v for k, v in child_fields.items() if v}
            selected_req.setdefault("children", []).append(child_req)
            st.success("Child requirement added.")

else:
    st.subheader("➕ Add Top-Level Requirement")
    with st.form("new_req_form"):
        new_fields = render_requirement_fields({}, schema, prefix="new_")
        add_new = st.form_submit_button("Add Requirement")
        if add_new:
            new_req = {k: v for k, v in new_fields.items() if v}
            st.session_state.requirements.append(new_req)
            st.success("Top-level requirement added.")

# --- Add Download/Export YAML Button and Project Metadata Editing ---

# Project metadata editor
st.sidebar.markdown("---")
st.sidebar.header("\U0001F4D6 Project Metadata")
if "project" not in st.session_state:
    st.session_state.project = {}
project = st.session_state.project
schema_project = schema["properties"].get("project", {}).get("properties", {})
with st.sidebar.form("project_metadata_form"):
    for field, props in schema_project.items():
        desc = props.get("description", "")
        value = project.get(field, "")
        if props.get("type") == "array":
            project[field] = st.text_area(f"{field} (comma-separated) ({desc})", value=", ".join(value or []), key=f"proj_{field}").split(", ") if value is not None else []
        else:
            project[field] = st.text_input(f"{field} ({desc})", value or "", key=f"proj_{field}")
    save_proj = st.form_submit_button("Save Project Metadata")
    if save_proj:
        st.session_state.project = project
        st.success("Project metadata updated.")

# --- Download/Export YAML ---
if st.session_state.requirements:
    st.markdown("---")
    st.header("\U0001F4BE Export Requirements YAML/CSV")
    export_data = {
        "project": st.session_state.project,
        "requirements": st.session_state.requirements
    }
    yaml_str = yaml.dump(export_data, sort_keys=False, allow_unicode=True)
    st.download_button(
        label="Download requirements.yaml",
        data=yaml_str,
        file_name="requirements.yaml",
        mime="text/yaml"
    )

    # --- Export to CSV ---
    def flatten_req(req, parent_id=None):
        flat = {
            'id': req.get('id', ''),
            'title': req.get('title', ''),
            'description': req.get('description', ''),
            'parent_id': parent_id or '',
            'tags': ", ".join(req.get('tags', [])),
            'type': req.get('type', ''),
            'category': req.get('category', ''),
            'priority': req.get('priority', ''),
            'state': req.get('state', ''),
            'status_implemented': req.get('status', {}).get('implemented', ''),
            'status_verified': req.get('status', {}).get('verified', ''),
            'status_removed': req.get('status', {}).get('removed', ''),
            'cross_references': str(req.get('cross_references', {})),
            'external_references': str(req.get('external_references', [])),
            'rationale': req.get('rationale', ''),
            'verification': req.get('verification', ''),
            'release': req.get('release', ''),
            'risk': req.get('risk', ''),
            'domain': req.get('domain', ''),
            'metadata': str(req.get('metadata', {})),
            'custom': str(req.get('custom', {})),
        }
        rows = [flat]
        for child in req.get('children', []):
            rows.extend(flatten_req(child, parent_id=flat['id']))
        return rows

    # Flatten all requirements
    csv_rows = []
    for req in st.session_state.requirements:
        csv_rows.extend(flatten_req(req))

    # Prepare CSV
    if csv_rows:
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)
        st.download_button(
            label="Download requirements.csv",
            data=csv_buffer.getvalue(),
            file_name="requirements.csv",
            mime="text/csv"
        )
