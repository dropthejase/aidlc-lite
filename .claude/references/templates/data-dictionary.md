# Data Dictionary Template

## Purpose
The current data model — entities, fields, constraints, and relationships. The reference for what data exists, what is valid, and where PII lives.

## Template

```markdown
# Data Dictionary

**Last Updated:** [YYYY-MM-DD HH:MM:SS]

## Overview
[1-2 lines: datastore(s) in use — Postgres, DynamoDB, Redis — and modelling style]

## Entity Relationships
[Mermaid erDiagram showing entities and cardinality]

## [Entity Name]
**Store:** [table/collection name]  •  **Key:** [PK / partition+sort]

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | uuid | PK | Unique identifier |
| email | string | unique, not null | Login + contact |
| status | enum | active\|suspended | Account state |
| created_at | timestamp | not null | Row creation |

**Indexes:** [secondary indexes and why]
**Notes:** [PII flags, retention, derived/computed fields]
```

## Guidelines

### When to update
- At **unit completion**, when an entity, field, constraint, index, or relationship was added or changed.

### Format
- One `##` block per entity; the Constraints column carries uniqueness, nullability, FKs, enums, ranges.
- Flag PII in Notes — this is what the security review reads for data classification.
- Cardinality lives in the ER diagram; do not restate it per field.
- List short enum values in Constraints; for long sets, point to where they are defined.
