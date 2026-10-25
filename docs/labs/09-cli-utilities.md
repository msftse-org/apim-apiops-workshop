# Lab 09: Native CLI output and automation

**Outcome:** discover flags and inspect machine-readable results directly.

```bash
apiops publish --help
apiops extract --help
apiops apic extract --help
apiops apic publish --help
apiops init --help

apiops publish \
  --subscription-id "$AZURE_SUBSCRIPTION_ID" \
  --resource-group "$RESOURCE_GROUP" \
  --service-name "$APIM_NAME" \
  --source apim-artifacts --overrides configuration.dev.yaml --dry-run --format json --log-level debug > .work/diagnostic-plan.json 2> .work/diagnostic-plan.log
jq '{status, exitCode, summary, plannedActions: .dryRun.actions}' .work/diagnostic-plan.json
```

JSON results go to stdout and diagnostic logs to stderr. Keep raw outputs local because they can contain resource identifiers or request details. For scripts, capture the exit code immediately.

Publish outcomes include success (0), partial failure (1), and fatal rejection (2). `init` overwrite conflicts return 1 in version 1.0.5. A successful zero-resource incremental publish is possible, so inspect counts as well as exit status.

`--cloud` supports additional Azure clouds and authentication can use other DefaultAzureCredential methods. Those are discovery topics, not validated alternatives in this public-cloud lab. For this workshop use your own `az login` session.

[Next: Verify outcomes](10-validation.md)
