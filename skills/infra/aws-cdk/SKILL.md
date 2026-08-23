---
name: aws-cdk
description: >-
  AWS CDK patterns for TypeScript: app/stack/construct structure, L2/L3
  construct choice, IAM least privilege, stateful-resource safety,
  environment/account wiring, testing with fine-grained assertions, and
  synth/diff/deploy workflow. Use when writing or reviewing CDK code,
  cdk.json, stacks, constructs, or any IaC written in the AWS CDK.
---

# AWS CDK

Infrastructure-as-code in TypeScript. Prefer the highest-level construct that
does the job, grant least privilege by default, and treat stateful resources
as radioactive.

## Project structure

```text
bin/app.ts            # app entry: new MyApp({ env: { account, region } })
lib/
  my-stack.ts         # Stack classes — thin composition of constructs
constructs/           # reusable L3 constructs (shared within the repo)
test/my-stack.test.ts # assertions against synthesized templates
cdk.json              # app: "npx ts-node bin/app.ts", context settings
```

- Stacks stay thin: business wiring lives in constructs, not inline in the
  Stack class.
- One stack per deployment unit / lifecycle. Don't put stateful data stores
  in the same stack as ephemeral compute unless the lifecycle truly matches.
- In monorepos, share constructs via an internal package (e.g.
  `packages/common`); apps import them rather than copy-pasting.

## Constructs

- **L3 (pattern) > L2 > L1** — reach for `aws-cdk-lib/aws-*` L2s; drop to L1
  (`CfnXxx`) only for features missing from L2; extract an L3 once a
  construct is reused or exceeds ~50 lines of wiring.
- Props are plain interfaces extending nothing; required props first, no
  defaults hidden deep inside the construct.
- Never hardcode ARNs/partition assumptions — use
  `stack.formatArn()` / token-based references so it works across partitions
  (including GovCloud/China if ever needed).

## IAM least privilege

- Use `grantRead` / `grantWrite` / `grantInvoke` style methods instead of
  hand-written policies with `"*"` actions or resources.
- If you must write a policy statement, scope both actions and resource ARNs;
  never `"Resource": "*"`.
- Roles are assumed by specific services (`grants.lambda.grantInvoke(queue)`)
  — avoid broad `AssumeRole` trust.

## Stateful resources (databases, buckets, queues, DynamoDB)

- Default to `removalPolicy: RETAIN` and `delete: false`-style protection on
  production data stores. `DESTROY` only for throwaway/dev stacks.
- Renaming or changing certain properties (DynamoDB key schema, RDS engine
  version, bucket names) forces replacement — flag this in review; the diff
  must call it out explicitly.
- Enable PITR/backups, encryption (usually default), and versioning on
  buckets holding anything valuable.

## Environments and accounts

- Always pass explicit `env: { account, region }` — never rely on the CLI's
  ambient credentials for synthesis decisions.
- Cross-account/region values come from context lookups (SSM parameters,
  `ssm.StringParameter.valueForStringParameter`) or config files, not
  hardcoded IDs sprinkled through stacks.
- Tag everything (`Tags.of(scope).add(...)`) for cost allocation; use Aspects
  for org-wide mandatory tags.

## Workflow

- `cdk synth` must succeed before anything else; read the synthesized
  template when logic is nontrivial.
- Review `cdk diff` like a production change — every new IAM statement,
  replacement, or deletion gets a conscious decision.
- Deploys go through CI where possible; local deploys target dev accounts
  only.
- Bootstrap each account/region once (`cdk bootstrap`); don't fight unbound
  ("The environment ... has not been bootstrapped") errors by hacking around
  assets.

## Testing

- Fine-grained assertions with
  `Template.fromStack(stack).hasResourceProperties("AWS::X::Y", {...})` are
  the default test style.
- Snapshot tests only for small stable templates — they churn otherwise.
- Test the things that hurt: IAM scoping, encryption/removal policies,
  event-source mappings, environment variables wiring.

## Secrets and config

- No secrets in source, context, or synthesized templates. Use Secrets
  Manager / SSM SecureString and grant access; pass secret *names*, never
  values, through props.

## Before finishing

- [ ] `cdk synth` (or the package's build + test command) passes
- [ ] `cdk diff` reviewed; replacements/deletions called out in the summary
- [ ] No wildcard IAM statements introduced
- [ ] Stateful resources have explicit removal policy + protection reasoning
- [ ] New constructs follow naming/structure conventions of the repo
