<!-- filepath: schema/reqs-schema.md -->

# Requirements Schema Overview

This schema defines a flexible, hierarchical structure for managing requirements in YAML or JSON format. It is designed to support:

- Complex, nested requirements (parent/child relationships)
- Project-level metadata
- Implementation and validation tracking
- Traceability and cross-references between requirements
- Rich metadata for each requirement (tags, status, rationale, etc.)

## Top-Level Structure

- **requirements** (array, required):
  - The main list of requirements. Each entry is a requirement object, which may itself have nested `children`.
- **project** (object, optional):
  - Metadata about the project, such as code, summary, and external references.

## Requirement Object Fields

- **id** (string, required):
  - Unique identifier for the requirement (e.g., `REQ_001`, `REQ_MYPROJECT_000001`).
- **title** (string, required):
  - Short, human-readable title for the requirement.
- **description** (string, required):
  - Detailed description, supports Markdown.
- **tags** (array of strings, optional):
  - For filtering, searching, or classifying requirements.
- **status** (object, optional):
  - Flags for tracking implementation and validation (e.g., `implemented`, `verified`).
- **cross_references** (object, optional):
  - Links to other requirements (e.g., `depends_on`, `related_to`, `conflicts_with`).
- **children** (array, optional):
  - Nested child requirements, each with the same structure as a top-level requirement.
- **external_references** (array, optional):
  - Document IDs, URLs, ticket numbers, or other references.
- **acceptance_criteria** (array, optional):
  - List of criteria for requirement acceptance.
- **linked_features** (array, optional):
  - Associated feature or epic IDs from project management tools.
- **deprecated_reason** (string, optional):
  - Reason for deprecation if the requirement is no longer valid.
- **domain** (string, optional):
  - Domain or subsystem classification.
- **metadata** (object, optional):
  - Arbitrary key-value metadata (e.g., release, team).
- **rationale** (string, optional):
  - Reasoning or justification for the requirement.
- **verification** (string, optional):
  - How the requirement will be verified (e.g., Test, Review).
- **priority** (string, optional):
  - Priority level (e.g., High, Medium, Low).
- **traceability** (object, optional):
  - Traceability information for audits or compliance.
- **risk** (string, optional):
  - Risk assessment or notes.
- **release** (string, optional):
  - Release version or milestone.
- **state** (string, optional):
  - Current state (e.g., approved, draft, deprecated).

## Key Features

- **Hierarchical**: Requirements can be nested to any depth using `children`.
- **Traceable**: Cross-references and traceability fields support compliance and impact analysis.
- **Extensible**: The schema allows for additional metadata and fields as needed.
- **Validation**: The schema can be used with tools like `jsonschema` to validate requirements files before use.

For full details, see the JSON and YAML schema files in the `schema/` directory.
