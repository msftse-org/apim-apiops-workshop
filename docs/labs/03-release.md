# Lab 03: Change a release and roll it back

**Outcome:** dev v1 → v2 → v1, with QA remaining v2. All deployment steps use native `apiops publish`.

Make a separate local Git repository for the exercise, so your workshop checkout remains unchanged:

```bash
RELEASE_LAB=$(mktemp -d "$WORKSHOP_ROOT/.work/release.XXXXXX")
cp -R apim-artifacts configuration.dev.yaml "$RELEASE_LAB/"
cd "$RELEASE_LAB"
git init -b lab-release
git config user.name "Workshop Participant"
git config user.email "workshop@example.invalid"
git add .
git commit -m "Baseline v1"

jq '.properties.value = "v2"' \
  apim-artifacts/namedValues/demo-release/namedValueInformation.json > release.tmp
mv release.tmp apim-artifacts/namedValues/demo-release/namedValueInformation.json
git add apim-artifacts/namedValues/demo-release/namedValueInformation.json
git commit -m "Release v2"
CHANGE_COMMIT=$(git rev-parse HEAD)
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --commit-id "$CHANGE_COMMIT" --dry-run --format json > change-preview.json
jq '.summary' change-preview.json
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --commit-id "$CHANGE_COMMIT"
# Wait for the gateway to serve the requested release.
for attempt in {1..24}; do
  if curl --fail-with-body --max-time 30 -sS -D response.headers -o response.body \
    "https://$APIM_NAME.azure-api.net/dev/orders/status" &&
    grep -qi "x-demo-release: v2" response.headers; then break; fi
  sleep 5
done
grep -qi "x-demo-release: v2" response.headers
cat response.headers response.body
curl --fail-with-body -i "https://$APIM_NAME.azure-api.net/qa/orders/status"
```

Expect one PUT in the plan, dev v2 and QA v2. Now revert the selected commit:

```bash
git revert --no-edit "$CHANGE_COMMIT"
ROLLBACK_COMMIT=$(git rev-parse HEAD)
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --commit-id "$ROLLBACK_COMMIT"
# Wait for the gateway to serve the requested release.
for attempt in {1..24}; do
  if curl --fail-with-body --max-time 30 -sS -D response.headers -o response.body \
    "https://$APIM_NAME.azure-api.net/dev/orders/status" &&
    grep -qi "x-demo-release: v1" response.headers; then break; fi
  sleep 5
done
grep -qi "x-demo-release: v1" response.headers
cat response.headers response.body
cd "$WORKSHOP_ROOT"
```

Expected dev release: v1. `--commit-id` compares the selected commit with its parent, not an arbitrary range up to HEAD. Do not assume it detects every missed deployment. Use full publish for a baseline or drift recovery.

Keep `RELEASE_LAB` in this shell for Lab 04. If the v2 publish succeeds but a later step fails, execute the rollback block before leaving the lab.

[Next: Overrides](04-overrides.md)
