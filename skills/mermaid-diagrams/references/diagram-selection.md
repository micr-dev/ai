# Diagram Selection

## Decision Table

| Need | Use | Why |
| --- | --- | --- |
| Explain modules, services, data flow, trust boundaries | `flowchart` | Most flexible and most GitHub-safe |
| Explain request/response, retries, queues, async work | `sequenceDiagram` | Preserves time ordering and actor responsibility |
| Explain database/domain entities | `erDiagram` | Shows cardinality and attributes compactly |
| Explain protocol states, lifecycle, job runner, auth session | `stateDiagram-v2` | Captures allowed transitions and terminal states |
| Explain branches, releases, rollback, promotion | `gitGraph` | Maps version-control history as documentation |
| Explain roadmap, migration phases, incident chronology | `timeline` | Reader scans time periods quickly |
| Explain C4 context/container/component | `C4Context`, `C4Container`, `C4Component` | Familiar architecture model, but experimental in Mermaid |
| Explain cloud/resource topology | `architecture-beta` | Purpose-built but requires recent Mermaid support |
| Explain prioritization | `quadrantChart` | Compact tradeoff matrix |
| Explain concept hierarchy | `mindmap` | Useful for taxonomy, not system behavior |

## Split Rules

Split one large diagram into multiple diagrams when:

- A reader needs two different answers, for example "what exists" and "what happens at runtime".
- The diagram has more than one dominant reading direction.
- There are more than roughly 25 to 35 nodes.
- Edge crossings are the main thing the reader sees.
- A subgraph has grown enough to deserve its own local view.

Good README sequence:

1. Context diagram: what systems exist and who owns them.
2. Runtime sequence: what happens during the key workflow.
3. Data or state diagram: what invariants the workflow changes.

## Choosing Between Similar Types

Use `flowchart` instead of C4 when:

- GitHub README compatibility matters more than C4 notation purity.
- You need colors, custom node shapes, or non-C4 relationships.
- The architecture is small enough that C4 boundaries would add ceremony.

Use C4 instead of `flowchart` when:

- The audience already uses C4 vocabulary.
- The goal is architecture review, not implementation details.
- You can accept experimental renderer risk or have verified GitHub support.

Use `stateDiagram-v2` instead of `flowchart` when:

- The allowed transitions are the main contract.
- Invalid transitions matter.
- Start, terminal, fork, join, or composite states clarify behavior.

Use `sequenceDiagram` instead of `flowchart` when:

- Time order and ownership matter.
- Retries, failures, parallel work, or critical sections are the important parts.
- The same components exchange several messages.
