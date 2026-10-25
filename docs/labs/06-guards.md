# Lab 06: Secrets, rejection and one explicit deletion

**Outcome:** see secret redaction, a blocked publish, commit-scoped deletion and stale local-file removal.

The fixture value is the public synthetic string `WORKSHOP-NOT-A-CREDENTIAL`. It is not a real credential. Create a disposable repository with exactly one named value:

```bash
DELETE_LAB=$(mktemp -d "$WORKSHOP_ROOT/.work/delete.XXXXXX")
cp -R examples/disposable/. "$DELETE_LAB/"
cp examples/configuration.disposable.yaml "$DELETE_LAB/configuration.yaml"
cp examples/filter.temporary.yaml "$DELETE_LAB/filter.yaml"
cd "$DELETE_LAB"
git init -b lab-delete
git config user.name "Workshop Participant"
git config user.email "workshop@example.invalid"
git add .
git commit -m "Add disposable synthetic named value"
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source artifacts --overrides configuration.yaml

apiops extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --output extracted --filter filter.yaml
jq '.properties.value' extracted/namedValues/dev-workshop-temporary/namedValueInformation.json
```

Expected extracted value: `*** REDACTED ***`. Publishing it without a replacement must fail. The following block checks the expected exit code:

```bash
if apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source extracted --dry-run; then
  echo "Unexpected success: stop and inspect the CLI version"; exit 1
else
  result=$?
  test "$result" -eq 2
  echo "Expected redaction rejection (exit 2)"
fi

if apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source artifacts --filter filter.yaml --delete-unmatched --dry-run; then
  echo "Unexpected success: incompatible options were accepted"; exit 1
else
  result=$?
  test "$result" -eq 2
  echo "Expected filter/delete rejection (exit 2)"
fi
```

Delete only the fixture artifact and pin that removal commit. Review the entire dry-run plan before executing it:

```bash
git rm artifacts/namedValues/workshop-temporary/namedValueInformation.json
git commit -m "Remove disposable named value"
DELETE_COMMIT=$(git rev-parse HEAD)
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source artifacts --overrides configuration.yaml --commit-id "$DELETE_COMMIT" --delete-unmatched --dry-run --format json > delete-plan.json
jq '.dryRun.actions' delete-plan.json
jq -e '.dryRun.actions | length == 1 and .[0].operation == "DELETE" and .[0].type == "NamedValue" and .[0].name == "workshop-temporary"' delete-plan.json
apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source artifacts --overrides configuration.yaml --commit-id "$DELETE_COMMIT" --delete-unmatched

apiops extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --output extracted --filter filter.yaml --remove-stale
test ! -f extracted/namedValues/dev-workshop-temporary/namedValueInformation.json
cd "$WORKSHOP_ROOT"
```

Full `--delete-unmatched` can remove remote resources absent from the local source. This lab uses a pinned commit so only its removed fixture is targeted. Do not run a full unmatched cleanup against the fixture directory.

For actual secrets, the CLI supports Key Vault references and pipeline token substitution. Those need customer-owned secret stores and permissions; this lab does not provision them. If interrupted after fixture creation, finish the scoped removal block or delete that exact temporary value in your sandbox.

[Next: API Center](07-api-center.md)
