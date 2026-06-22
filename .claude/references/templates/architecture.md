# Architecture Template

## Purpose
The system's current-state map: what it is, how data flows, and the load-bearing technical choices. First doc to read to understand how the system works today.

## Template

```markdown
# Architecture

**Last Updated:** [YYYY-MM-DD HH:MM:SS]

## System Overview
[High-level description of the system]

### Tech Stack

### Diagram
[Mermaid diagram showing component interactions]

### Data Flow
[Numbered list of how data moves through the system]

## Security
[Concise bulleted list of security features]

## Further Details
### Architectural Decisions
See [adr.md](./adr.md)

### Data Models
See [data-dictionary.md](./data-dictionary.md)

### APIs
See [apis.md](./apis.md)

## Limitations
[Concise bulleted list]

## Roadmap
[Concise bulleted list]
```

## Guidelines

### When to update
- At **unit completion**, when the unit changed the system shape — new tech-stack entry, a load-bearing decision, a new top-level data flow, or a security-relevant addition.
- This is the system's current-state summary: keep it short and overwrite stale lines. Detail lives in the linked docs.

### Format
- DO NOT overwrite the `Further Details` section
- For the limitations, include only technical limitations
- For functional limitations or future features, add to `Roadmap` instead using a table with columns
  - Feature: F1, F2, F3...
  - Description: 1-2 lines
- **Never invent the roadmap.** Roadmap entries come only from features the user explicitly deferred or agreed are out of scope (recorded during `aidlc-plan`). If nothing was deferred, leave the section empty — do not guess where the product is heading.