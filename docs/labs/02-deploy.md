# Lab 02: Preview and deploy dev and QA

**Outcome:** one canonical artifact set, two API namespaces and observable headers.

Open `apim-artifacts/apis/demo-orders/specification.json` and the operation policies. `/status` returns synthetic JSON. `/echo` calls the public httpbin backend. The policy fragment adds environment/release headers.

From the repository root:

```bash
unset COMMIT_ID
mkdir -p .work
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --dry-run --format json > .work/dev-preview.json
jq '.dryRun.actions' .work/dev-preview.json
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml

apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.qa.yaml --dry-run
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.qa.yaml
```

Call both routes:

```bash
for environment in dev qa; do
  expected_release=v1
  [[ "$environment" == qa ]] && expected_release=v2
  for attempt in {1..36}; do
    if curl --fail-with-body --max-time 30 -sS \
      -D ".work/$environment.headers" -o ".work/$environment.body" \
      "https://$APIM_NAME.azure-api.net/$environment/orders/status" &&
      grep -qi "x-demo-release: $expected_release" ".work/$environment.headers"; then break; fi
    sleep 5
  done
  grep -qi "x-demo-environment: $environment" ".work/$environment.headers"
  grep -qi "x-demo-release: $expected_release" ".work/$environment.headers"
  jq -e '.status == "ok" and .synthetic == true' ".work/$environment.body"
done
curl --fail-with-body --retry 4 --retry-delay 5 --max-time 30 -sS \
  -D .work/echo.headers -o .work/echo.body \
  "https://$APIM_NAME.azure-api.net/dev/orders/echo"
jq -e '.url | endswith("/get")' .work/echo.body
grep -qi 'x-demo-environment: dev' .work/echo.headers
grep -qi 'x-demo-release: v1' .work/echo.headers
```

Expected: HTTP 200, dev release v1 and QA release v2 in `X-Demo-Environment` / `X-Demo-Release`. The status body contains `"synthetic": true`. The echo body shows an upstream URL ending `/get`. Gateway changes can take a short time to propagate; retry the call if you briefly see the old value.

A dry-run is a plan, not proof Azure will accept every property. The external echo service may be unavailable; `/status` does not depend on it.

[Next: Release and rollback](03-release.md)
