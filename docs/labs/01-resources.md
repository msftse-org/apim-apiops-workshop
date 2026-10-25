# Lab 01: Create or select your Azure resources

**Outcome:** APIM Consumption and API Center Free in your own dedicated resource group.

Skip the creation block if your administrator has already provisioned these resources. Set `.env` to those exact names instead. APIM names must be globally unique.

```bash
az group create --subscription "$AZURE_SUBSCRIPTION_ID" \
  --name "$RESOURCE_GROUP" --location "$LOCATION" --tags purpose=apim-apiops-workshop

az apim create --subscription "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" --name "$APIM_NAME" --location "$LOCATION" \
  --sku-name Consumption --sku-capacity 0 \
  --publisher-name "APIM Workshop" --publisher-email "$PUBLISHER_EMAIL"

az rest --method put \
  --url "https://management.azure.com/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.ApiCenter/services/$APIC_NAME?api-version=2024-03-01" \
  --body "$(jq -n --arg location "$LOCATION" '{location:$location,sku:{name:"Free"},properties:{}}')"
```

Verify the resources:

```bash
az apim show --subscription "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" --name "$APIM_NAME" \
  --query '{state:provisioningState,sku:sku.name,gateway:gatewayUrl}' -o table

az resource list --subscription "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" --query '[].{name:name,type:type}' -o table
```

Wait for APIM provisioning to report `Succeeded`. Creation may take several minutes. Regional SKU availability, naming, quota and subscription policy may affect provisioning. Use an allowed region if West Europe is unavailable.

Consumption is metered. A Free API Center does not make the entire Azure lab free. The author validated publishing against existing resources; fresh creation was performed in the original sandbox setup. Your tenant's provisioning policy is not assumed to match it.

[Next: Deploy](02-deploy.md)
