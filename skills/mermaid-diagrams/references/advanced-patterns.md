# Advanced Patterns

## README Architecture Map

Use this for complex systems where GitHub compatibility matters. It avoids experimental diagram types but still shows ownership, async paths, storage, and failure handling.

```mermaid
flowchart LR
  user["User"]
  cli["CLI / Browser"]

  subgraph edge["Edge"]
    proxy["Reverse proxy"]
    auth{"Session valid?"}
  end

  subgraph app["Application"]
    api["API routes"]
    jobs["Job dispatcher"]
    audit["Audit log writer"]
  end

  subgraph workers["Workers"]
    queue[["Queue"]]
    worker["Worker pool"]
    retry["Retry policy"]
  end

  subgraph data["Data"]
    db[("Primary DB")]
    blob[("Blob storage")]
  end

  user --> cli
  cli --> proxy
  proxy --> auth
  auth -->|yes| api
  auth -->|no| denied["401 / 403"]
  api --> db
  api --> jobs
  api --> audit
  jobs --> queue
  queue --> worker
  worker --> db
  worker --> blob
  worker -->|transient failure| retry
  retry --> queue

  classDef boundary fill:#f8fafc,stroke:#64748b,color:#0f172a
  classDef decision fill:#fff7ed,stroke:#c2410c,color:#7c2d12
  classDef store fill:#eef2ff,stroke:#4338ca,color:#312e81
  classDef failure fill:#fef2f2,stroke:#b91c1c,color:#7f1d1d
  class auth decision
  class db,blob store
  class denied failure
```

## Trust Boundary Flow

Make trust boundaries explicit and label edges by protocol or credential.

```mermaid
flowchart TB
  browser["Browser"]

  subgraph public["Public network"]
    cdn["CDN"]
  end

  subgraph private["Private application network"]
    gateway["API gateway"]
    service["Service"]
    vault["Secrets vault"]
  end

  subgraph storage["Storage boundary"]
    db[("Database")]
  end

  browser -->|HTTPS| cdn
  cdn -->|signed origin request| gateway
  gateway -->|JWT claims| service
  service -->|short-lived token| vault
  service -->|parameterized SQL| db
```

## Deep Sequence With Failures

Use `box`, `alt`, `par`, `critical`, and `break` to keep complex workflows readable.

```mermaid
sequenceDiagram
  autonumber
  actor User
  box Client
    participant UI
  end
  box Platform
    participant API
    participant Queue
    participant Worker
  end
  participant DB as Database

  User->>UI: Submit import
  UI->>API: POST /imports
  API->>DB: Create import row
  API->>Queue: Enqueue import job
  API-->>UI: 202 Accepted

  par Background processing
    Queue->>Worker: Deliver job
    Worker->>DB: Lock import row
    critical Validate and persist
      Worker->>Worker: Parse file
      Worker->>DB: Write normalized records
    option Invalid input
      Worker->>DB: Mark failed with reason
    end
  and User polling
    UI->>API: GET /imports/:id
    API->>DB: Read status
    API-->>UI: Status payload
  end

  alt import complete
    UI-->>User: Show imported records
  else import failed
    UI-->>User: Show actionable error
  end
```

## ERD With Intentional Attributes

Show only attributes that explain identity, cardinality, or reader-facing meaning.

```mermaid
erDiagram
  USER ||--o{ PROJECT : owns
  PROJECT ||--o{ IMPORT_JOB : contains
  IMPORT_JOB ||--o{ IMPORT_ROW : produces
  USER ||--o{ AUDIT_EVENT : triggers
  PROJECT ||--o{ AUDIT_EVENT : scopes

  USER {
    uuid id PK
    string email UK
    datetime created_at
  }

  PROJECT {
    uuid id PK
    uuid owner_id FK
    string slug UK
  }

  IMPORT_JOB {
    uuid id PK
    uuid project_id FK
    string status
    string failure_reason
  }

  IMPORT_ROW {
    uuid id PK
    uuid import_job_id FK
    string external_key
    json normalized_payload
  }
```

## State Machine Contract

Use state diagrams when invalid transitions are a bug.

```mermaid
stateDiagram-v2
  direction LR
  [*] --> Draft
  Draft --> Queued: submit
  Queued --> Running: worker locks job
  Running --> Succeeded: all rows persisted
  Running --> Failed: validation or runtime error
  Running --> CancelRequested: user cancels
  CancelRequested --> Canceled: worker acknowledges
  Failed --> Queued: retry allowed
  Succeeded --> [*]
  Canceled --> [*]

  note right of Failed
    Store a stable failure_reason
    before exposing status.
  end note
```

## Release Story With GitGraph

Use `gitGraph` to explain release strategy, rollback, or hotfix flow.

```mermaid
gitGraph
  commit id: "v1.2.0"
  branch feature
  checkout feature
  commit id: "add import"
  commit id: "tests"
  checkout main
  merge feature tag: "v1.3.0"
  branch hotfix
  checkout hotfix
  commit id: "patch auth" type: HIGHLIGHT
  checkout main
  merge hotfix tag: "v1.3.1"
```

## Migration Timeline

Use timelines for planning and postmortems, but verify GitHub support first.

```mermaid
timeline
  title Storage Migration
  section Preparation
    Week 1 : Add dual-write metrics
           : Backfill dry-run
    Week 2 : Fix drift
           : Freeze schema changes
  section Cutover
    Week 3 : Enable new reads
           : Monitor latency and error budget
  section Cleanup
    Week 4 : Remove old write path
           : Archive migration dashboard
```
