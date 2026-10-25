# Lab 00: Install the CLI and sign in

**Outcome:** use the real `apiops` executable against your own Azure account.

Install Node.js 22+, npm, Azure CLI, Git, jq and curl. Use Bash or WSL. Follow the README clone and environment setup first, then inspect the native CLI:

```bash
for tool in node npm az git jq curl apiops; do
  command -v "$tool" >/dev/null || { echo "Missing prerequisite: $tool"; exit 1; }
done
node -e 'if (+process.versions.node.split(".")[0] < 22) process.exit(1)'
test "$(apiops --version)" = "1.0.5"
for name in TENANT_ID AZURE_SUBSCRIPTION_ID RESOURCE_GROUP APIM_NAME APIC_NAME LOCATION PUBLISHER_EMAIL; do
  value="${!name:-}"
  if [[ -z "$value" || "$value" == *YOUR-* || "$value" == "YOU@EXAMPLE.COM" ]]; then
    echo "Edit .env: $name is missing or still a placeholder"; exit 1
  fi
done
test "$(az cloud show --query name -o tsv)" = AzureCloud
test "$(az account show --query id -o tsv)" = "$AZURE_SUBSCRIPTION_ID"
test "$(az account show --query tenantId -o tsv)" = "$TENANT_ID"
curl --help all | grep -q -- --fail-with-body
apiops --version
apiops --help
apiops extract --help
apiops publish --help
apiops init --help
apiops apic --help
az account show --query '{tenant:tenantId,subscription:id,name:name}' -o table
```

Expected CLI version: `1.0.5`. Confirm the tenant and subscription are yours before making changes. If different, run `az login --tenant "$TENANT_ID"` and `az account set --subscription "$AZURE_SUBSCRIPTION_ID"` again.

If global npm installation fails with a filesystem permission error, open Bash at your checkout root and install the same native CLI into an ignored folder. All subsequent `apiops` commands remain unchanged:

```bash
export WORKSHOP_ROOT="$PWD"
mkdir -p "$WORKSHOP_ROOT/.work/tools"
npm install --global --prefix "$WORKSHOP_ROOT/.work/tools" @azure-tools/apiops-cli@1.0.5
export PATH="$WORKSHOP_ROOT/.work/tools/bin:$PATH"
apiops --version
```

Run the prerequisite block again after installing. Registry or proxy errors require network configuration; changing the installation folder does not fix them.

Privileges: resource creation usually requires Contributor on the dedicated group, plus permission to create the group if it does not exist. Managing existing APIM configuration requires APIM write permissions; API Center needs its own write permissions. Ask your administrator for suitable lab access. No tenant-wide administrator role or GitHub identity is required for these local exercises.

### Public npm and corporate networks

The customer installation uses the standard npm command from the README. npm defaults to **`https://registry.npmjs.org/`**, unless your organization has configured another registry. This repository does not contain a `.npmrc` or require the author's corporate network.

Check your current configuration with `npm config get registry`. On an unrestricted network, `npm view @azure-tools/apiops-cli@1.0.5 version --registry=https://registry.npmjs.org/` checks the pinned public package. If your VPN or organization requires an approved mirror, use that existing configuration for installation; the same `apiops` commands follow. For a one-command override, npm accepts `--registry` with your organization's approved URL. Do not replace a managed global configuration just to follow this workshop.

A failed connection from a corporate machine is not evidence that the public package is missing. Validation records distinguish public-registry checks on GitHub-hosted runners from the author's local installation through its configured mirror. See [npm's registry documentation](https://docs.npmjs.com/cli/v11/using-npm/registry/).

### Session and network requirements

Keep the same Bash session and run labs in order. Start from the repository root. PowerShell and zsh do not support all these Bash expressions. The sample gateway URLs target **Azure public cloud**.

You need network access to GitHub, your npm registry, Azure sign-in and management endpoints, your APIM gateway and `httpbin.org`. A corporate proxy, TLS inspection, blocked registry or unavailable echo backend can stop a lab. Global npm permission errors can be avoided with a user-managed Node installation or the local-prefix installation above. Do not paste credentials into troubleshooting logs.

If your session closes, open Bash at the repository root and run:

```bash
set -euo pipefail
export WORKSHOP_ROOT="$PWD"
source .env
export PATH="$WORKSHOP_ROOT/.work/tools/bin:$PATH"
unset COMMIT_ID
mkdir -p .work
az account set --subscription "$AZURE_SUBSCRIPTION_ID"
```

Then rerun Labs 02–10 in order. This recreates `RELEASE_LAB`, `DELETE_LAB`, `GITHUB_LAB`, `AZDO_LAB` and their evidence files before final verification. Do not append Lab 04's override twice in the same disposable repository: restart Lab 03 first. The temporary directories are intentionally disposable, while resource cleanup remains explicit.

Keep `.env` private. `apiops` uses DefaultAzureCredential. The supplied `.env.example` sets `AZURE_TOKEN_CREDENTIALS=AzureCliCredential` so these local labs use your Azure CLI sign-in. Leave this setting in place for the workshop. `unset COMMIT_ID` before full publishes if your shell inherited it from CI.

[Next: Resources](01-resources.md)
