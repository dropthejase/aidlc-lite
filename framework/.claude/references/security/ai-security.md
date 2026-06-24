# AI Security

Applies when the application involves LLMs, autonomous agents, or MCP tool integrations. Read alongside `security-baseline.md`.

## OWASP Top 10 for LLM Applications (2025)

For every LLM-powered feature, verify defenses against each category:

1. **LLM01 — Prompt Injection**: Treat all user input as potentially adversarial. Never interpolate user input directly into system prompts. Validate and sanitize before passing to the model. Use separate trusted and untrusted input channels.

2. **LLM02 — Sensitive Information Disclosure**: Audit training data and RAG corpora for PII, credentials, and confidential content. Apply output filtering. Do not include secrets in system prompts. Test for memorisation of training data.

3. **LLM03 — Supply Chain**: Vet third-party models, datasets, plugins, and fine-tuning pipelines. Pin model versions. Verify integrity of model artifacts. Treat external model providers as third-party vendors.

4. **LLM04 — Data and Model Poisoning**: Validate and audit training and fine-tuning datasets. Monitor model behaviour for unexpected drift. Restrict who can contribute to training pipelines.

5. **LLM05 — Improper Output Handling**: Never pass raw LLM output directly to interpreters (SQL, shell, HTML). Treat LLM output as untrusted. Sanitize before rendering or executing. Apply output schemas where possible.

6. **LLM06 — Excessive Agency**: Grant the minimum tool permissions needed. Require human approval for irreversible actions (delete, send, publish). Log all tool calls. Apply rate limits on agentic actions.

7. **LLM07 — System Prompt Leakage**: Do not store secrets in system prompts. Assume system prompts can be extracted. Test for prompt disclosure via adversarial inputs.

8. **LLM08 — Vector and Embedding Weaknesses**: Validate data before indexing into vector stores. Apply access controls at retrieval time — retrieved context inherits the permissions of the requester. Monitor for poisoned embeddings.

9. **LLM09 — Misinformation**: Do not present LLM output as authoritative without grounding or citation. Apply fact-checking layers for high-stakes domains. Communicate uncertainty to users.

10. **LLM10 — Unbounded Consumption**: Apply token limits per request and per user. Implement request rate limiting. Set cost budgets and alert thresholds. Gracefully degrade under load rather than failing silently.

## OWASP Top 10 for Agentic Applications (2026)

Applies when the system uses autonomous agents that plan, decide, and act across multiple steps or tools:

1. **ASI01 — Agent Goal Hijack**: Validate agent instructions at each step, not just at initialisation. Detect and reject goal drift. Confirm intent before executing high-impact actions.

2. **ASI02 — Tool Misuse & Exploitation**: Define strict tool schemas. Validate tool inputs and outputs. Apply least-privilege at the tool level. Log all tool invocations with inputs, outputs, and caller identity.

3. **ASI03 — Identity & Privilege Abuse**: Do not allow agents to inherit ambient credentials. Issue scoped, short-lived tokens per task. Never grant agents persistent admin access.

4. **ASI04 — Agentic Supply Chain Vulnerabilities**: Vet and pin third-party plugins, tool registries, and agent frameworks. Treat external tool providers as untrusted until verified.

5. **ASI05 — Unexpected Code Execution (RCE)**: Sandbox code execution environments. Restrict what languages and system calls agents can invoke. Review and approve code generation before execution in production.

6. **ASI06 — Memory & Context Poisoning**: Validate context retrieved from memory stores before acting on it. Treat persisted memory as untrusted input. Apply TTL and integrity checks to stored context.

7. **ASI07 — Insecure Inter-Agent Communication**: Authenticate all agent-to-agent communication. Encrypt payloads in transit. Do not allow an agent to instruct another agent to bypass safety controls.

8. **ASI08 — Cascading Failures**: Design agents to fail safely and independently. Apply circuit breakers between agent stages. Define explicit rollback and compensation actions for multi-step workflows.

9. **ASI09 — Human-Agent Trust Exploitation**: Make agent identity clear to users at all times. Do not allow agents to impersonate humans. Require explicit user consent before agents act on their behalf.

10. **ASI10 — Rogue Agents**: Monitor agent behaviour continuously. Implement kill switches. Alert on actions outside expected behaviour envelopes. Do not allow agents to disable their own monitoring.

## OWASP MCP Top 10 (2025)

Applies when the system uses Model Context Protocol servers or clients:

1. **MCP01 — Token Mismanagement & Secret Exposure**: Never store credentials in model context, system prompts, or protocol logs. Use short-lived, scoped tokens. Enforce secret scanning in CI.

2. **MCP02 — Privilege Escalation via Scope Creep**: Define the minimum required scope at registration. Automate expiry of unused permissions. Audit granted scopes quarterly.

3. **MCP03 — Tool Poisoning**: Treat MCP tool descriptions as untrusted input. Validate tool outputs before acting. Alert on unexpected changes to registered tool definitions.

4. **MCP04 — Supply Chain Attacks & Dependency Tampering**: Pin MCP server versions. Verify integrity of server packages. Do not auto-update MCP dependencies without review.

5. **MCP05 — Command Injection & Execution**: Validate and sanitize all inputs before passing to MCP tools. Never allow raw user input to reach shell or database tools.

6. **MCP06 — Prompt Injection via Contextual Payloads**: Treat context injected by MCP servers as untrusted. Isolate server-provided context from trusted system instructions.

7. **MCP07 — Insufficient Authentication & Authorization**: Require authentication for every MCP server. Enforce per-tool authorization. Do not expose MCP servers publicly without access controls.

8. **MCP08 — Lack of Audit and Telemetry**: Log every tool call: server, tool name, inputs, outputs, caller, timestamp. Ship logs to tamper-resistant storage. Alert on anomalous patterns.

9. **MCP09 — Shadow MCP Servers**: Maintain an inventory of all registered MCP servers. Block unregistered servers. Alert on unexpected server registration.

10. **MCP10 — Context Injection & Over-Sharing**: Limit the context surface exposed to each MCP server. Do not share cross-server context without explicit permission. Treat each server's tool descriptions as potentially adversarial.

## AI Security Checklist

For code review and design review, verify:
- [ ] User input is never interpolated directly into system prompts
- [ ] LLM output is treated as untrusted before rendering or executing
- [ ] Tool permissions follow least privilege — minimum scope per task
- [ ] All tool calls are logged with inputs, outputs, and caller identity
- [ ] Irreversible agent actions require human approval
- [ ] No secrets or credentials in system prompts or model context
- [ ] Agent tokens are short-lived and task-scoped, not ambient
- [ ] Agent-to-agent communication is authenticated and encrypted
- [ ] MCP servers are inventoried, pinned, and access-controlled
- [ ] Token/cost budgets and rate limits are enforced per user
- [ ] Kill switch exists for autonomous agent workflows
- [ ] Agent behaviour is monitored and alerts exist for anomalies
