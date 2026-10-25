# Lab 02: First deployment

**Outcome:** two working API routes from one set of canonical artifacts.

1. Open `apim-artifacts/apis/demo-orders/specification.json`. Find `/status` and `/echo`.
2. Open `operations/get-status/policy.xml`. This operation returns a synthetic response.
3. Open the API policy and `policyFragments/demo-headers/policyFragmentInformation.json`. The fragment supplies environment and release headers.
4. Preview, publish, then repeat for QA:

```bash
python3 scripts/workshop.py preview --env dev
python3 scripts/workshop.py publish --env dev
python3 scripts/workshop.py preview --env qa
python3 scripts/workshop.py publish --env qa
python3 scripts/workshop.py status
```

Expected: `/dev/orders/status` returns HTTP 200 with `X-Demo-Environment: dev` and `X-Demo-Release: v1`. `/qa/orders/status` returns HTTP 200 with `qa` and `v2`. The status helper retries while gateway changes propagate.

The wrapper executes this CLI pattern with your configured Azure identifiers:

```text
apiops publish --source apim-artifacts --overrides configuration.dev.yaml
  --subscription-id <id> --resource-group <rg> --service-name <apim> --format json
```

Dry-run adds `--dry-run`. Inspect `.work/logs/dev-preview.stdout.txt`: `dryRun.actions` describes the plan. A successful preview does not guarantee Azure will accept every property at publish time.

For the backend example, call `https://<your-apim>.azure-api.net/dev/orders/echo`. The policy routes to `httpbin.org/get`; the live suite checks its response and headers. This depends on an external public service. The `/status` exercise works without that backend.

[Next: Release and rollback](03-release.md)
