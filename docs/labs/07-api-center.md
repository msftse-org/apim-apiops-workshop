# Lab 07: API Center backup and replay

**Outcome:** distinguish the API catalog from the gateway, then export and replay catalog artifacts.

```bash
python3 scripts/workshop.py apic
```

The runner:

1. Previews and publishes the sample API catalog in `apic-artifacts/`.
2. Extracts the catalog and definitions to `.work/apic-backup/`.
3. Asserts specification files exist.
4. Previews and replays the extracted backup into the same API Center instance.
5. Extracts only the `default` workspace with `--no-specifications` to `.work/apic-metadata/`.
6. Asserts this metadata-only backup contains no specification files.
7. Publishes that metadata with `--no-specifications`.

Open the sample API in API Center and compare its metadata to the files. Extra sample APIs or catalog analyzer resources may be present, so total counts can differ by instance.

This validates same-instance backup/replay. It does not prove cross-region recovery, recovery to a fresh instance, or complete backup of every Azure service setting. APIC dry-run checks local plans; it does not exercise every Azure acceptance check.

[Next: CI/CD and Copilot](08-cicd.md)
