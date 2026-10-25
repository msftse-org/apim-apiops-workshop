# Lab 08: CI/CD scaffolding and Copilot prompts

**Outcome:** generate both supported pipeline formats without overwriting this workshop repository.

```bash
python3 scripts/workshop.py scaffold
```

For each of `github-actions` and `azure-devops`, the runner creates a fresh `.work/scaffold-<platform>-<timestamp>/` directory and runs:

```text
apiops init --ci <platform> --environments dev,qa --non-interactive
```

It asserts configuration and Copilot prompt files exist, repeats init to test overwrite protection, and then tests explicit `--force` regeneration.

Inspect the generated files:

1. The extraction workflow: how does it capture configuration and create a proposed Git change?
2. The publishing workflow: where are environment overrides selected?
3. The identity setup guide: which app, federation settings and Azure roles are required?
4. `.github/prompts/`: filter configuration, override configuration and platform identity prompts.
5. Configuration schema references: how can VS Code provide completion and validation?

To try Copilot, open the generated folder in VS Code with your own GitHub Copilot access. Select a generated prompt and ask it to prepare a filter or explain the identity setup. Review its output before running Azure commands. Interactive Copilot sessions require a licensed account and were not automated in the validation run.

The generated Azure DevOps pipelines are samples in this lab. They are not claimed as executed hosted pipelines. The next lab provides an executable GitHub Actions path for this workshop.

[Next: Hosted workflow](09-hosted-workflow.md)
