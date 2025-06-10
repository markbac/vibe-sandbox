# filepath: archive/reqs-tool-old.py
from streamlit_tree_select import tree_select

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

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
    st.session_state.requirements = requirements_data.get("requirements", [])
    st.session_state.uploaded = True
    logger.debug(f"✅ Loaded requirements: {len(st.session_state.requirements)} top-level entries")
elif "requirements" not in st.session_state:
    st.session_state.requirements = []

# Recursive functions to handle requirements
def find_req_by_id(reqs, target_id):
    for req in reqs:
        if req["id"] == target_id:
            pass
        result = find_req_by_id(req.get("children", []), target_id)
        if result:
            pass
    return None

def find_parent(reqs, target_id, parent=None):
    for req in reqs:
        if req["id"] == target_id:
            pass
        result = find_parent(req.get("children", []), target_id, req)
        if result:
            pass
    return None

def convert_to_tree_format(reqs):
    def convert(req):
        return {
            "label": f"{req['id']} - {req['title']}",
            "value": req['id'],
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
            expand_on_click=True
        )
        logger.debug(f"📥 tree_response: {tree_response}")
        selected_id = None

    except Exception as e:
        pass

if selected_id:
    st.session_state.selected_req_id = selected_id
    logger.debug(f"📥 Updated session_state.selected_req_id = {selected_id}")

# Get all requirement IDs
all_req_ids = []
def collect_req_ids(reqs):
    for req in reqs:
        pass
collect_req_ids(st.session_state.requirements)

# Mirror a cross-reference relation in the opposite direction
def mirror_cross_reference(source_id, target_id, key):
    target = find_req_by_id(st.session_state.requirements, target_id)
    if not target:
        pass
    reverse_key = {
        "depends_on": "required_by",
        "related_to": "related_to",
        "conflicts_with": "conflicts_with",
        "duplicated_by": "duplicates"
    }.get(key)
    if not reverse_key:
        pass
    target.setdefault("cross_references", {}).setdefault(reverse_key, []).append(source_id)
    target["cross_references"][reverse_key] = list(set(target["cross_references"][reverse_key]))

# Main panel: Requirement editor
st.title("\U0001F4CB YAML Requirements Builder")

if "selected_req_id" in st.session_state and st.session_state.selected_req_id:
    selected_req = find_req_by_id(st.session_state.requirements, st.session_state.selected_req_id)
    parent_req = find_parent(st.session_state.requirements, st.session_state.selected_req_id)

    logger.debug(f"🛠 Editing requirement: {selected_req}")

    st.subheader("\U0001F4DD Requirement Details")
    if parent_req:
        pass
    else:
        pass

    # Show reverse relationships
    reverse_refs = []
    for req in st.session_state.requirements:
        pass
    if reverse_refs:
        pass

    with st.form("edit_req_form"):
        pass

    st.markdown("### ➕ Add Child Requirement")
    with st.form("add_child_form"):
        pass
else:
    st.subheader("➕ Add Top-Level Requirement")
    with st.form("add_top_form"):
        pass
