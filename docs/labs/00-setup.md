# Lab 00: Install the CLI and sign in

**Outcome:** use the real `apiops` executable against your own Azure account.

Install Node.js 22+, npm, Azure CLI, Git, jq and curl. Use Bash or WSL. Follow the README clone and environment setup first, then inspect the native CLI:

```bash
apiops --version
apiops --help
apiops extract --help
apiops publish --help
apiops init --help
apiops apic --help
az account show --query '{tenant:tenantId,subscription:id,name:name}' -o table
```

Expected CLI version: `1.0.5`. Confirm the tenant and subscription are yours before making changes. If different, run `az login --tenant "$TENANT_ID"` and `az account set --subscription "$AZURE_SUBSCRIPTION_ID"` again.

If global npm installation is unavailable, `npx --yes @azure-tools/apiops-cli@1.0.5 <command>` invokes the same CLI. Replace the word `apiops` with that command prefix consistently.

Privileges: resource creation usually requires Contributor on the dedicated group, plus permission to create the group if it does not exist. Managing existing APIM configuration requires APIM write permissions; API Center needs its own write permissions. Ask your administrator for suitable lab access. No tenant-wide administrator role or GitHub identity is required for these local exercises.

Keep `.env` private. `apiops` uses DefaultAzureCredential, including your Azure CLI sign-in. Do not set service-principal secret variables unless deliberately using that authentication method. `unset COMMIT_ID` before full publishes if your shell inherited it from CI.

[Next: Resources](01-resources.md)
