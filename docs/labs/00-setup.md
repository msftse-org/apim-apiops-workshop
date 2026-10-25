# Lab 00: Setup

**Outcome:** run the same CLI version used to validate the workshop.

1. Install Node.js 22 or later, npm, Git, Python 3.10 or later and Azure CLI. Use Bash on macOS/Linux or WSL on Windows.
2. Clone this repository, enter its root and run `bash scripts/install.sh`.
3. Run `bash scripts/apiops.sh --version`. Expected: `1.0.5`.
4. Copy `config.example.json` to `config.local.json`. Enter your subscription ID, dedicated resource group, region, globally unique APIM/API Center names, and publisher email.
5. Run `az login`. Select an account that can access your sandbox subscription.
6. Run `python3 scripts/resources.py plan` and inspect the target names before provisioning.
7. After Lab 01, run `python3 scripts/workshop.py doctor`. Every reported step should have `passed: true`.

`config.local.json`, `.work/`, `vendor/` and npm cache are Git-ignored. Never commit credentials or local raw logs. The workshop uses Azure CLI through DefaultAzureCredential. For new resource creation you need resource creation rights in the chosen subscription/group. For existing services, use APIM write permissions and API Center write permissions scoped to the lab resources. Hosted federation is covered separately in Lab 09.

The installer fetches the exact upstream commit and builds locally. It does not install an unpinned global CLI. `APIOPS_CLI` can point to an already-built entry point when testing another version, but results must identify that version.

[Next: Resources](01-resources.md)
