# Third-Party Notices

AIDLC-Lite incorporates and adapts material from the projects below. Each retains its original license; those licenses are reproduced here. This file satisfies the notice requirements of the MIT and Apache 2.0 licenses.

---

## AWS AI-DLC (v2)

https://github.com/awslabs/aidlc-workflows/tree/v2

Several reference guides under `.claude/references/` are used directly or adapted from the AWS AI-DLC v2 knowledge base (e.g. `requirements-guide.md`, `product-guide.md`, `ddd-patterns.md`, `functional-design-guide.md`, `architecture-patterns.md`, `ux-guide.md`, `interaction-design-patterns.md`, `market-research-methods.md`, `code-generation*.md`, `testing-guide.md`). Some are verbatim; some are modified.

Licensed under the MIT No Attribution license (MIT-0). Attribution is not legally required by MIT-0; it is given here by choice.

```
MIT No Attribution

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

---

## Anthropic — Planner-Generator-Evaluator / long-running agents

https://github.com/anthropics/cwc-long-running-agents
https://www.anthropic.com/engineering/harness-design-long-running-apps

The generator ⇄ evaluator harness and the inversion-of-control loop (the loop and all exits living in the driver script, not the agents) are adapted from Anthropic's long-running-agents work. No files are reproduced verbatim; the loop in `.claude/scripts/generate_evaluate.py` is an original implementation of the pattern.

Licensed under the Apache License, Version 2.0. The full license text is available at https://www.apache.org/licenses/LICENSE-2.0 and in the source repository. Per the Apache 2.0 terms, note that AIDLC-Lite's implementation is a modified, independent adaptation and not the original work.
