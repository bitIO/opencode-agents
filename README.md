# OpenCode Agents Team

An opinionated AI software-delivery team for [OpenCode](https://opencode.ai/).

The goal of this project is not to create a collection of coding agents.

The goal is to create an **AI engineering organization** that can take a software request from a human client, understand it, challenge it when necessary, plan the work, delegate implementation to specialists, verify the result, and maintain traceability between requirements, tasks, code changes, and commits.

The human remains the **product authority**.

The AI team is responsible for the **engineering process**.

---

## Vision

The desired interaction is simple:

> **Human:** "I need authentication for our applications."

The human should not need to know:

* which files need changing
* which package should own the functionality
* which database migrations are required
* whether the request conflicts with existing architecture
* which specialist should implement each part
* which tests are required
* which security concerns need reviewing
* how to split the work into commits

The engineering team should figure that out.

The human should instead be asked questions when a decision genuinely requires human judgment.

The target workflow is:

```text
                         HUMAN / CLIENT
                               │
                               │ request
                               ▼
                       ┌────────────────┐
                       │   TEAM LEAD    │
                       │  Orchestrator  │
                       └───────┬────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          Requirements     Technical       Repository
            Analysis       Analysis        Analysis
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                       Feasibility Gate
                               │
                         human decision
                         when required
                               │
                               ▼
                         Engineering Plan
                               │
                         dependency graph
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
        Specialist A      Specialist B      Specialist C
             │                 │                 │
          verify             verify             verify
             │                 │                 │
          commit             commit             commit
             └─────────────────┼─────────────────┘
                               ▼
                       System-level Review
                               │
                               ▼
                           Acceptance
                               │
                               ▼
                              DONE
```

---

## Core Principle

### The team lead is an orchestrator, not an omniscient engineer.

The team lead should not become a giant prompt containing every engineering discipline.

It should know:

1. **what needs to be understood**
2. **which specialist can provide that understanding**
3. **when a decision requires the human**
4. **how to turn the resulting understanding into executable work**
5. **how to coordinate that work**
6. **how to verify that the final result satisfies the original request**

The team lead does not need to personally know everything.

It needs to know **who to ask**.

---

## The Engineering Lifecycle

The team is organized around five stages.

### 1. Intake

A request can originate from either:

#### Existing issue

* The human provides an existing GitHub issue.
* The team determines whether the issue is sufficiently clear to proceed.

#### Conversational request

The human describes a feature vaguely.

For example:

> "We need authentication shared by all our applications."

The team must first turn this into a sufficiently precise engineering request.

The human is the authority on **what should be built**.

The engineering team is responsible for determining **how to build it**.

---

### 2. Understand

Before implementation begins, the team must understand two different things.

#### Product understanding

Questions include:

* What outcome does the human actually want?
* Who needs the feature?
* What behavior should change?
* What is explicitly out of scope?
* Which decisions require human approval?
* Is the proposed feature actually needed now?

This is the responsibility of the requirements/product capability.

#### Technical understanding

Questions include:

* How does the repository currently solve this problem?
* Where does the relevant functionality live?
* What package boundaries exist?
* What architectural constraints exist?
* Which dependencies are involved?
* Which external APIs/frameworks are involved?
* What existing behavior could be affected?
* What migrations or compatibility concerns exist?
* Does the proposed solution fit the repository?

This is **not the same thing as product refinement**.

A technically precise issue can still describe a bad architecture.

---

### 3. Feasibility Gate

This is the most important distinction in this project.

A request being detailed does **not** mean it is ready for implementation.

The team must distinguish:

> **"We know what the issue says."**

from:

> **"We have evidence that the issue can and should be implemented this way."**

The feasibility stage challenges the proposed solution before task decomposition.

It should identify:

* contradictions with the existing codebase
* architectural conflicts
* unnecessary abstractions
* speculative requirements
* missing dependencies
* migration risks
* security risks
* integration constraints
* external-library limitations
* unclear ownership
* hidden coupling
* missing acceptance criteria
* implementation assumptions that have not been verified

The output is not code.

The output is an **engineering assessment**.

---

### 4. Plan

Only after the request passes the feasibility gate should the team lead decompose it.

The plan should be a dependency graph rather than merely a list of tasks.

For example:

```text
Task A: database schema
        │
        ├──────────────┐
        ▼              ▼
Task B: repository   Task C: auth core
        │              │
        └──────┬───────┘
               ▼
        Task D: provider adapter
               │
               ▼
        Task E: host integration
               │
        ┌──────┴───────┐
        ▼              ▼
     Task F          Task G
    frontend        integration
               │
               ▼
          system review
```

Each task must have:

* one clear responsibility
* a defined expected outcome
* explicit files/packages when known
* known dependencies
* acceptance conditions
* an assigned specialist
* a verification strategy

---

### 5. Execute

Implementation is delegated to specialist agents.

The team should prefer existing specialists over creating new agents.

Typical specialists include:

| Agent           | Responsibility                    |
| --------------- | --------------------------------- |
| `dev-node`      | Node.js / TypeScript / backend    |
| `dev-react`     | React / frontend                  |
| `devops-docker` | Docker / containerization         |
| `github`        | GitHub / branches / commits / PRs |
| `qa-testing`    | Tests and test strategy           |
| `qa-security`   | Security and threat modeling      |
| `qa-data`       | Database/data integrity           |
| `qa-perf`       | Performance                       |
| `qa-a11y`       | Accessibility                     |
| `review`        | Code/system review                |
| `product-owner` | Requirements refinement           |

Specialists should remain narrow.

A specialist should not become an alternative team lead.

---

## Atomic Work and Traceability

Every meaningful implementation task should correspond to an atomic commit.

The desired relationship is:

```text
Requirement
    │
    ├── Task A
    │      └── Commit A
    │
    ├── Task B
    │      └── Commit B
    │
    └── Task C
           └── Commit C
```

The team should always be able to answer:

> Why does this commit exist?

and:

> Which requirement/task does this code change satisfy?

A commit should represent one coherent engineering change.

Do not use commits as arbitrary checkpoints.

Use them as **traceability boundaries**.

---

## Verification

Implementation and verification are separate responsibilities.

The agent that writes the change should not automatically be the only agent deciding whether the change is correct.

Verification should operate at multiple levels.

### Local verification

Does the implementation:

* compile?
* lint?
* pass relevant tests?
* conform to existing patterns?

### Domain verification

Does the change preserve:

* data integrity?
* security?
* performance?
* accessibility?

when those concerns apply?

### System verification

Does the complete feature satisfy:

* the original acceptance criteria?
* the architectural decisions?
* the intended user behavior?
* the boundaries defined during planning?

A feature can pass local tests and still fail system-level verification.

---

## Human Authority

The AI team should be autonomous about **engineering execution** but not autonomous about **product decisions**.

The team should interrupt the human when a decision affects things such as:

* product behavior
* scope
* irreversible migrations
* significant architectural trade-offs
* security posture
* externally visible API contracts
* expensive infrastructure
* ambiguous business rules
* intentionally deferred requirements

The team should **not** interrupt the human for ordinary engineering decisions that are already constrained by the request, repository conventions, or established team rules.

The objective is:

> **Ask humans about decisions, not implementation details.**

---

## Architecture Principles

### Prefer evidence over speculation

Agents should inspect the repository before proposing changes.

They should inspect relevant external documentation when library behavior matters.

Do not design against imagined APIs.

Do not assume that a framework behaves a certain way because the agent remembers it.

---

### Existing architecture wins by default

Before introducing a new abstraction, ask:

> Does the repository already have a mechanism for this?

Before adding a new package:

> Is the package boundary actually required?

Before adding an interface:

> Is there a real variation point?

Before introducing configuration:

> Is this value genuinely variable?

Before adding a provider abstraction:

> Is provider substitution a real requirement?

---

### YAGNI applies to architecture too

The team should distinguish between:

```text
real requirement
```

and:

```text
possible future requirement
```

A seam should exist because there is a meaningful boundary today or because the current requirement explicitly requires substitutability.

Do not build hypothetical infrastructure merely because it might be useful later.

---

## Example: Authentication

An authentication issue might contain an apparently sophisticated architecture:

```text
AuthProvider
AuthApp
RoleRepository
Better Auth adapter
Strapi adapter
shared client
```

The engineering team must not assume that this is correct merely because the specification is detailed.

Before implementation, the technical analysis should ask:

* Does the repository already have an authentication boundary?
* How are users currently represented?
* Where are roles currently stored?
* Can the proposed migration preserve existing data?
* Does the selected provider actually support the required flows?
* Does the proposed provider contract expose the necessary semantics?
* Is the fetch-based host abstraction compatible with the existing server?
* Does the proposed bearer behavior work with the intended clients?
* Does `/me` provide a stable contract?
* Are session and token semantics understood?
* Does the package boundary actually enforce the intended dependency direction?
* Are the proposed abstractions necessary?
* What security assumptions are being made?
* What happens to existing authenticated users during migration?

Only after these questions are sufficiently answered should the team create implementation tasks.

---

## Agent Roles

The team is intentionally divided into different classes of responsibility.

### Orchestrator

#### `team-lead`

Owns the workflow.

It:

* receives requests
* determines what needs to be understood
* delegates analysis
* coordinates specialists
* creates the execution plan
* tracks progress
* delegates implementation
* delegates verification
* coordinates commits
* performs final acceptance

It does not implement code.

---

### Requirements

#### `product-owner`

Owns product clarity.

It answers:

> What should we build?

It does not answer:

> Is this architecture technically correct?

---

### Technical investigation

A dedicated technical-analysis capability is expected to become a first-class part of the team.

Its responsibility is:

> **What does the repository and its technical environment tell us about this request?**

It should combine:

* repository exploration
* architecture analysis
* dependency analysis
* existing-pattern discovery
* external API/library research
* feasibility analysis
* identification of contradictions and risks

This role should produce evidence and recommendations, not implementation.

---

### Implementation specialists

Implementation specialists answer:

> How do we implement the approved plan?

They should not independently redefine the product or architecture unless they discover a blocking contradiction.

If they discover one, they report it back to the team lead.

---

### Quality specialists

Quality agents answer focused questions:

> Is this safe/correct/tested/performant/accessibile/data-safe?

They should not silently expand scope.

---

## Skills

Agents should load specialized skills when the problem requires them.

Available skills may include:

* TypeScript
* architecture
* Drizzle
* Drizzle migrations
* PostgreSQL
* Turborepo
* React
* Playwright
* Docker
* Render
* code review
* external documentation research

Skills are **capabilities**, not necessarily agents.

A skill should be attached to the agent that needs the knowledge.

Avoid creating a new agent merely because a new skill exists.

---

## The Team's Core Invariants

These rules should survive changes to individual agents.

### 1. No implementation before sufficient understanding

Do not turn an unclear request into code.

### 2. No decomposition before feasibility

Do not turn an unvalidated architecture into 20 implementation tasks.

### 3. No specialist should become the orchestrator

Specialists provide expertise to the team lead.

### 4. No silent architectural changes

If implementation reveals that the plan is wrong, stop and escalate.

### 5. Every meaningful task has traceability

Task → code → commit.

### 6. Verification is independent

Implementation and verification should be separate responsibilities whenever practical.

### 7. Humans own product decisions

Agents recommend. Humans decide when the decision changes product intent or carries significant irreversible consequences.

### 8. Prefer existing repository patterns

Do not introduce abstractions without evidence.

### 9. External APIs must be verified

Use authoritative documentation rather than model memory.

### 10. The smallest correct system wins

Do not optimize for the number of agents, tasks, abstractions, or commits.

Optimize for delivering the requested behavior safely.

---

## What This Project Is Not

This project is not intended to create:

* autonomous agents that freely modify production systems
* dozens of overlapping specialist personas
* an AI hierarchy where every agent reviews every other agent
* a replacement for human product ownership
* an architecture committee that blocks ordinary development
* maximum test coverage regardless of value
* maximum abstraction
* maximum parallelism

The goal is **controlled autonomy**.

---

## Initial Team

The initial team may contain:

```text
team-lead
│
├── product-owner
├── technical-analysis        ← emerging capability
│
├── dev-node
├── dev-react
├── devops-docker
├── github
├── ...                       ← more specialists may be added as needed
│
├── qa-testing
├── qa-security
├── qa-data
├── qa-perf
├── qa-a11y
└── review
```

The exact team should evolve based on real failure modes.

Do not add agents simply because a discipline exists.

---

## Design Goal

The ultimate goal is that a human can interact with the system like this:

```text
Human:

"I need shared authentication across the admin,
recorder and teams applications. Better Auth seems
like a good option."

Team Lead:

1. Understands the request.
2. Refines missing product requirements.
3. Investigates the existing repository.
4. Researches relevant external APIs.
5. Challenges the proposed architecture.
6. Reports important trade-offs.
7. Gets human decisions where required.
8. Creates an engineering plan.
9. Delegates atomic implementation tasks.
10. Verifies each task.
11. Commits each atomic change.
12. Performs system-level verification.
13. Reports what changed and why.
```

The human should be able to remain at the level of:

> **"What should the software do?"**

while the AI team handles:

> **"How do we safely get there?"**

---

## Evolution Strategy

This project should evolve from observed failures.

When an implementation goes wrong, ask:

> Which stage of the lifecycle should have prevented this?

Examples:

| Failure                                | Likely missing capability       |
| -------------------------------------- | ------------------------------- |
| Requirements misunderstood             | Product/requirements            |
| Existing code ignored                  | Repository investigation        |
| Bad architecture implemented perfectly | Feasibility/architecture        |
| Library API hallucinated               | External documentation research |
| Migration loses data                   | Data verification               |
| Auth vulnerability                     | Security review                 |
| Tests don't cover behavior             | Testing strategy                |
| Tasks depend on each other incorrectly | Planning/dependency analysis    |
| Agent changes unrelated files          | Task boundary enforcement       |
| Code works but violates architecture   | System/code review              |
| Impossible requirement discovered late | Earlier feasibility gate        |
| Too many unnecessary abstractions      | Architecture/YAGNI review       |

The answer to a failure should not automatically be:

> "Create another agent."

First ask:

> **Which responsibility was missing, and which existing role should own it?**

Only create a new agent when the responsibility is sufficiently distinct and recurring.

---

## Success Criteria

This project is successful when:

1. A vague feature request can become an executable engineering plan without the human decomposing it.
2. Existing GitHub issues can be challenged before implementation.
3. Architectural assumptions are validated before large amounts of code are written.
4. Specialists work within clearly defined boundaries.
5. Every meaningful implementation task is traceable to a commit.
6. Verification catches defects independently of implementation.
7. The team can stop and ask the human when a real product decision is required.
8. The number of agents remains small enough to understand.
9. The system becomes more reliable through observed feedback rather than prompt complexity.
10. The human spends more time making product decisions and less time managing implementation mechanics.

---

## Current Direction

The immediate priority is **not adding more coding agents**.

The next design problem is to establish the technical-analysis / feasibility capability that sits between:

```text
requirements
     ↓
technical understanding
     ↓
feasibility
     ↓
planning
     ↓
implementation
```

The existing `team-lead`, `product-owner`, `dev-*`, `qa-*`, and `review` agents provide a strong foundation.

The next iteration should determine whether the technical-analysis capability should be:

1. a new dedicated agent,
2. an expanded `explore` capability,
3. a reusable architecture/research skill invoked by `team-lead`,
4. or a small combination of these.

The decision should be based on the responsibilities and failure modes of the system—not on the desire to have more agents.

---

## Guiding Principle

> **Build an engineering organization, not an agent zoo.**
