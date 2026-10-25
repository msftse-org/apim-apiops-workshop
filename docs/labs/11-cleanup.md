# Lab 11: Clean up your resources

**Outcome:** remove the resources from your own dedicated workshop group when finished.

Review the account and every resource first:

```bash
az account show --query '{tenant:tenantId,subscription:id,name:name}' -o table
az resource list --subscription "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" --query '[].{name:name,type:type}' -o table
```

If this group contains only your workshop resources, run the native delete command and answer its confirmation prompt:

```bash
az group delete --subscription "$AZURE_SUBSCRIPTION_ID" --name "$RESOURCE_GROUP"
```

This deletes the **entire group**, not just its API configuration. Do not run it against a shared or production group. The reference environment stays deployed for demonstrations, so final validation intentionally does not execute whole-group deletion. Lab 06 already removes its disposable named value.

No GitHub deployment identity is created by the customer path. If you separately configured customer-owned pipelines, remove their federation, role assignments and variables when retiring those pipelines.

[Return to workshop](../../README.md)
