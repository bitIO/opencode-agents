---
name: fip-code-review
description: >
  Review code changes in FIP/adidas AWS CDK TypeScript monorepos (npm workspaces,
  @fip/common FipConstruct/FipLambda, Biome, Jest, runtypes, commitlint). Use
  whenever reviewing a PR, a diff, a file, or pasted code from one of these repos
  (fip-agent-assets-registry, fip-mcp-registry, and similar). It combines the 4R
  framework with the FIP house rules distilled from real reviewer feedback. Use
  for "review this PR", "review this diff", "review this file", "check this
  construct", or "is this ready to merge". Produces a structured findings report
  that can be handed to sub-agents to fix in parallel.
---

# FIP Code Review

Structured code review for **adidas FIP AWS CDK TypeScript monorepos**. Builds on
the [4R framework](../4r-code-review/SKILL.md) (Risk, Readability, Reliability,
Resilience) and adds the **FIP house rules** below, distilled from real PR
reviews on `fip-agent-assets-registry` and `fip-mcp-registry`.

## When to use

- "Review this PR / diff / file" in a FIP CDK monorepo
- "Is this ready to merge?" / "what's wrong with this?"
- Reviewing CDK constructs, lambda source, configs, or workspace wiring
- Auditing a specific concern (naming, configs vs props, class properties)

## Ground rules (inherited from 4R)

- **Evidence over assertion**: every finding cites `file:line` (or function/branch).
- **Proportionality**: severity scales with blast radius (public API / auth / prod > internal tool).
- **Balanced**: report what is done well too.
- **No nitpicking**: skip cosmetics with no real impact.

## Review workflow

1. **Understand scope** — read the diff or list changed files. Identify which
   workspaces/domains are touched (constructs, lambdas, config, root wiring).
2. **Run mechanical gates locally** (no push, no fix):
   - `npm run build` — must compile
   - `npm run lint` — Biome must pass
   - `npm test` — focused on touched workspaces
   - `npx cdk synth -c region=eu-west-1 -c deploymentEnvironment=dev` — emits expected resources
3. **Apply 4R** (Risk / Readability / Reliability / Resilience) to each change.
4. **Apply the FIP house rules** below to each changed file.
5. **Emit the report** in the parallel-delegation format (§ Output).

## FIP house rules

These are the recurring review findings across the FIP CDK repos. Check each
changed file against them.

### 1. Constructs/resources assigned to the class

- Every construct and every created resource must be stored on a `public readonly`
  class property, never created as a bare statement.
  - `this.registry = new Registry(this, 'Registry', props)` — NOT `new Registry(...)`
  - `this.skillsRegistry = this.createRegistryResource(...)` — NOT `this.createRegistryResource(...)` returning void
- This applies at every level: `MainStack`, domain constructs, and inner resources.

### 2. Configs vs Props split

- **Configs** are types that come from the config JSON files. **Props** are what a
  construct needs from other constructs (cross-construct references).
- Keep them separate and compose them:
  ```ts
  export type RegistryConfig = { readonly name: string; /* ... */ };
  export type RegistryCustomResourceConfig = { readonly skills: RegistryConfig; /* ... */ };
  export type RegistryCustomResourceProps = FipConstructConfig &
    RegistryCustomResourceConfig & { readonly registryManagerLambda: IFunction };
  ```
  (`RegistryConfig` / `RegistryCustomResourceConfig` are examples — use the names
  that fit the domain under review.)
- Cross-construct references (e.g. `registryManagerLambda: IFunction`) belong in
  Props, NOT in Config.
- The top-level domain config composes the child configs:
  ```ts
  export type DomainConfig = {
    readonly <lambda>: <Lambda>Config;
    readonly <customResource>: <CustomResource>Config;
  };
  ```
  and the construct spreads them: `...<lambda>`, `...<customResource>`.

### 3. Config types live next to their construct

- "Types in CDK from configs should always be in the same cdk where the resource
  to be deployed is going to be" — each construct file owns its own config type.
- No shared `app-common` workspace / central `types.ts` for per-construct configs.
  The lambda's config lives in `lambda.ts`, the custom-resource configs in
  `custom-resource.ts`, and the composed domain config in `<business>.construct.ts`.

### 4. Naming conventions

- Workspace `cdk/index.ts` exports ONLY the main construct:
  `export * from './lib/<business>.construct';`
- File names: `<business>.construct` for the main construct; `lambda.ts`,
  `custom-resource.ts` for the pieces — the service name is usually enough.
  Use `<lambda-for-x>.lambda.ts` / `<lambda-for-y>.lambda.ts` only when a business
  logic has 2+ lambdas. Test specs mirror the source file names.

### 5. `readonly` everywhere

- Every field on every type is `readonly` (`readonly allowedAudience: Array<string>`).
- For runtypes `Record(...)`, use `.asReadonly()` so the derived `Static` type is readonly:
  ```ts
  export const RegistryResourceProperties = Record({ /* ... */ }).asReadonly();
  export type RegistryResourceProperties = Static<typeof RegistryResourceProperties>;
  ```

### 6. No duplicated validation / logic

- Hoist shared helpers to class properties instead of recreating them per method:
  ```ts
  private readonly validate = validateRuntype(this.logger)(RegistryResourceProperties);
  ```
  used in both `executeCreateEvent` and `executeUpdateEvent`, instead of a `const validate = ...` in each.

### 7. Remove the unnecessary

- Reviewer flag "not needed" has appeared for: redundant `rootDir` in tsconfig when
  the default suffices; redundant `coverageReporters` override when `jest.default-config`
  already covers it; unneeded env vars (e.g. `NODE_OPTIONS: '--enable-source-maps'`).
- Defaults are preferred; only override what must differ.

### 8. No leftover seed scaffolding

- Remove seed example workspaces / files (e.g. a shared `app-common` workspace that
  only held example types, stale `CHANGELOG` history from the seed).
- Changelog must reflect the actual project's history, not the seed's.

### 9. SDK/external libs at the root

- SDK and external libraries live in the **root** `package.json` `dependencies` so
  they're unified across the repo; lambda workspaces should not redeclare them.
- Workspace `package.json` scripts must match the repo's optimized baseline
  (sibling workspaces as reference) — don't add `--verbose`, `--runInBand`, etc.
  unless they're the norm.

### 10. FipConstruct / FipLambda conventions

- Constructs extend `FipConstruct<Props>` from `@fip/common/infra`; use
  `this.buildResourceName(name)` for every named resource; log group created via
  `this.createLogGroup(...)` before the function and passed as `logGroup:`
  (never `logRetention:`).
- Lambdas: composition root `src/index.ts` reads env vars, builds clients, captures
  them on the tracer, then `Domain` → `Handler`. Input validation with runtypes via
  the curried `validateRuntype(logger)(schema)` helper.
- Commit messages: `TICKET-123: VERB subject` (uppercase verb, ≤72 chars).

## Recurring 4R findings in FIP CDK (check these too)

These come from real reviews of the FIP lambda/construct code once the house rules
are satisfied. Calibrate severity to blast radius (prod/API path > internal tool).

- **Unchecked `JSON.parse` / casts** — e.g. `JSON.parse(props.allowedAudience) as Array<string>`
  where the runtypes schema only validates the string. A malformed payload throws an
  uncaught `SyntaxError`, and a wrong-shaped JSON silently passes the cast. Fix: validate
  the parsed shape with a runtypes `Array(StringRuntype)` (or explicit guards) before use.
- **IAM least privilege** — `PolicyStatement` with `resources: ['*']` on create/get/update/
  delete actions widens blast radius to every resource of that type in the account. Prefer
  scoping to `arn:aws:bedrock:${region}:${account}:<type>/*` (keep `*` only for actions that
  can't be scoped, and justify it).
- **Custom-resource immutability can wedge rollbacks** — throwing in the domain on an immutable
  field change (e.g. `discoveryUrl`/`registryName`) makes every UPDATE re-fail, blocking unrelated
  stack changes. Either keep the old value and ignore the delta, or surface it as a documented,
  intentional limitation.
- **Custom-resource lifecycle** — delete must tolerate `ResourceNotFoundException`/`NotFoundException`
  (treat as success); create/update must return a stable `physicalResourceId` (ARN); idempotency
  across retries matters.
- **Tracer/service defaults** — `new Tracer({ serviceName })` with an optional env var silently
  falls back to `service_undefined` in traces. Default explicitly when the wiring is imperative.
- **Bare statements instead of class properties** — see house rule #1 (recurring enough to re-check).

## Output — parallel-delegation report

Produce findings as a **flat, self-contained list** so sub-agents can pick them up
in parallel without conflicts:

```md
## Findings

### F1 (HIGH) — construct not assigned to class property
- **File**: <domain>/aws-resources/cdk/lib/<business>.construct.ts:25
- **Rule**: house rule #1 (constructs assigned to the class)
- **Issue**: `new <ChildConstruct>(...)` is a bare statement.
- **Fix**: declare `public readonly <childConstruct>: <ChildConstruct>;`
  and assign `this.<childConstruct> = new <ChildConstruct>(...)`.
- **Tests**: update `<domain>/aws-resources/test/specs/unit/<business>.construct.spec.ts` assertion if needed.

### F2 (MEDIUM) — duplicated validation setup
- **File**: <domain>/<lambda-name>/src/handler.ts:27
- **Rule**: house rule #6 (no duplicated validation / logic)
- **Issue**: `validateRuntype(...)(schema)` is recreated in both create and update.
- **Fix**: hoist it to a `private readonly validate = validateRuntype(this.logger)(Schema);` class property.
- **Tests**: none needed (behavior unchanged); verify existing handler tests still pass.
```

Use `<domain>`, `<lambda-name>`, `<business>` as placeholders matching the repo under review —
never paste names from another repo.

Rules for the report:
- Each finding is fully self-contained (file, rule, issue, concrete fix, tests to touch).
- One finding = one file (or one clearly-scoped location) so sub-agents don't collide.
- Group by severity; order HIGH → LOW.
- Add a `## Passing` section listing what's done well.
- End with a `## Suggested parallel split` — group findings by file cluster so N
  sub-agents can work on disjoint file sets concurrently.

Rules for the parallel split:
- Group findings by **file** (not by rule). Two findings touching the same file MUST go
  to the same cluster (e.g. `domain.ts` findings belong to one agent) so agents never
  edit the same file concurrently.
- Explicitly call out overlaps: if F1 is `domain.ts` and F3 is also `domain.ts`, say
  "merge F1+F3 into Agent A" rather than producing a split with colliding agents.
- Aim for clusters of roughly equal size; fewer clusters is fine if files interleave.

## Verify after fixes

- Re-run `npm run build`, `npm run lint`, `npm test` on touched workspaces.
- Confirm `npx cdk synth` still emits the expected resource count.
