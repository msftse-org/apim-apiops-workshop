# Lab 05: Extraction, filters and dependency expansion

**Outcome:** inspect full configuration, select resources, and compare dependency expansion.

```bash
apiops extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --output .work/extract-dependencies --filter filter.dev-strict.yaml --format json > .work/extract-dependencies.json

apiops extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --output .work/extract-exact --filter filter.dev-strict.yaml --no-transitive --format json > .work/extract-exact.json
jq '.summary.totalExtracted' .work/extract-dependencies.json .work/extract-exact.json

apiops extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --output .work/extract-full
```

Dependency expansion includes the backend, fragment and named values referenced by the API. The exact extraction contains fewer resources. Compare the directories.

An omitted filter type means “include all” for that type. Our filters explicitly list all 17 keys and use `[]` for unrelated types. Extract filters match deployed names (`dev-demo-orders`); publish filters match canonical artifact names (`demo-orders`).

Preview and publish the filtered canonical subset:

```bash
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --filter filter.orders-strict.yaml --dry-run
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --filter filter.orders-strict.yaml
```

The tag is explicitly included so the API association can resolve. `--no-transitive` can also be used with publish, but required dependencies must already exist.

Try wildcard selection and exclusion:

```bash
apiops extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --output .work/extract-patterns --filter examples/filter.patterns.yaml
find .work/extract-patterns -name namedValueInformation.json
```

Expected: `dev-demo-environment` is present and `dev-demo-release` is absent. The filter selects `dev-*` and excludes `!dev-demo-release`. Exclusions are quoted to avoid YAML ambiguity.

[Next: Secrets and deletion](06-guards.md)
