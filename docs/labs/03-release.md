# Lab 03: Release and rollback

**Outcome:** observe dev v1, dev v2 and dev v1 again, while QA remains v2.

Run the repeatable version first:

```bash
python3 scripts/workshop.py cycle
```

The runner creates `.work/release-<timestamp>/` with its own Git history. It commits a v1 baseline, changes only `namedValues/demo-release/namedValueInformation.json`, commits v2, previews one PUT, deploys it, tests dev and QA, then reverts that commit and deploys the revert. It attempts rollback even if the v2 verification fails.

For the manual exercise, create your own local branch and commit only the named value change:

```bash
git switch -c lab-release
python3 scripts/set-release.py v2
git add apim-artifacts/namedValues/demo-release/namedValueInformation.json
git commit -m "Lab: release v2"
python3 scripts/workshop.py incremental --env dev --commit HEAD
# Call /dev/orders/status: expect v2.
git revert --no-edit HEAD
python3 scripts/workshop.py incremental --env dev --commit HEAD
python3 scripts/workshop.py status
```

Expected final state: dev v1, QA v2. Exercise commits remain local unless you explicitly push them.

`--commit-id` compares one selected commit to its parent. It is not a deployment history database and does not automatically deploy every missed commit. Use a full publish for baseline/drift recovery or override-only changes. Missing Git history can result in zero selected resources, so inspect the JSON summary.

[Next: Overrides](04-overrides.md)
