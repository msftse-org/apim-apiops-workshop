# Lab 01: Resources

**Outcome:** an APIM Consumption gateway and a separate API Center Free catalog in a dedicated resource group.

```bash
python3 scripts/resources.py plan
python3 scripts/resources.py provision
python3 scripts/resources.py list
python3 scripts/workshop.py doctor
```

The provision command first checks for existing resources. It creates missing resources and reuses existing ones. APIM requires a publisher email when it is first created. The script does not upgrade or downgrade an existing APIM SKU. Wait for APIM provisioning to finish before publishing. Resource creation can take several minutes and can fail due to regional SKU availability, quota, naming or subscription policy.

In Azure portal, confirm the APIM SKU and API Center SKU. Consumption is metered and other Azure usage may incur charges. A Free API Center does not make the entire lab free.

The reference sandbox was already deployed when the public workshop was validated. The idempotent reuse path was checked again. Fresh resource creation was exercised during the original lab, not recreated for every validation run.

[Next: First deployment](02-deploy.md)
