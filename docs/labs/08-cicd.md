# Lab 08: Generate CI/CD and Copilot files

**Outcome:** see what `apiops init` creates for both supported platforms. No deployment pipeline is connected to Azure by this lab.

```bash
GITHUB_LAB=$(mktemp -d "$WORKSHOP_ROOT/.work/github.XXXXXX")
cd "$GITHUB_LAB"
apiops init --ci github-actions --environments dev,qa --non-interactive
find . -maxdepth 4 -type f

# Existing generated files require an explicit overwrite decision.
if apiops init --ci github-actions --environments dev,qa --non-interactive; then
  echo "Unexpected overwrite without --force"; exit 1
else
  result=$?
  test "$result" -eq 1
  echo "Expected overwrite conflict (exit 1)"
fi
apiops init --ci github-actions --environments dev,qa --non-interactive --force

AZDO_LAB=$(mktemp -d "$WORKSHOP_ROOT/.work/azure-devops.XXXXXX")
cd "$AZDO_LAB"
apiops init --ci azure-devops --environments dev,qa --non-interactive
find . -maxdepth 4 -type f
if apiops init --ci azure-devops --environments dev,qa --non-interactive; then
  echo "Unexpected overwrite without --force"; exit 1
else
  result=$?
  test "$result" -eq 1
  echo "Expected overwrite conflict (exit 1)"
fi
apiops init --ci azure-devops --environments dev,qa --non-interactive --force
cd "$WORKSHOP_ROOT"
```

Inspect the extraction/publish workflows, configuration files and identity setup guide. The generated files use workload identity federation patterns. A customer who wants to deploy through their own CI system must configure their own repository, identities, permissions and approval gates separately.

Open `.github/prompts/` in either generated directory. The prompts help GitHub Copilot prepare filters, overrides and platform identity setup. Interactive Copilot requires your own licensed VS Code account and is not part of the automated execution evidence.

These generated files remain under ignored `.work/`. The public workshop repository has only offline validation CI, with no Azure variables or deployment trust.

[Next: CLI utilities](09-cli-utilities.md)
