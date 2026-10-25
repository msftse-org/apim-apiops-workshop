# Lab 07: API Center metadata and specifications

**Outcome:** operate the API catalog separately from the APIM gateway.

Preview and seed the catalog:

```bash
apiops apic publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIC_NAME" \
  --source apic-artifacts --dry-run
apiops apic publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIC_NAME" \
  --source apic-artifacts
```

Back up its resources and definitions, then preview and replay that backup:

```bash
apiops apic extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIC_NAME" \
  --output .work/apic-backup
find .work/apic-backup -name 'specification.*'
apiops apic publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIC_NAME" \
  --source .work/apic-backup --dry-run
apiops apic publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIC_NAME" \
  --source .work/apic-backup
```

Now select only the default API Center workspace and skip specifications:

```bash
apiops apic extract \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIC_NAME" \
  --output .work/apic-metadata --workspace default --no-specifications
find .work/apic-metadata -name 'specification.*'
apiops apic publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIC_NAME" \
  --source .work/apic-metadata --no-specifications
```

Expected: the first backup contains specification files; the metadata-only directory does not. API Center workspaces are separate from APIM workspaces. Additional sample/analyzer resources may exist, so counts can differ.

This validates same-instance replay. It is not a disaster recovery test to a fresh region or service. APIC dry-run inspects the local plan and does not prove all Azure-side validation will succeed.

[Next: Pipeline generation](08-cicd.md)
