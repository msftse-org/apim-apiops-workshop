# Official sources

The tested CLI source is pinned to commit `129fb326e6878c2bedd45e8ae4ccb8526de688a4` (package version 1.0.5).

- [Official repository](https://github.com/Azure/apiops-cli)
- [Pinned getting started](https://github.com/Azure/apiops-cli/blob/129fb326e6878c2bedd45e8ae4ccb8526de688a4/docs/getting-started.md)
- [Publish reference](https://github.com/Azure/apiops-cli/blob/129fb326e6878c2bedd45e8ae4ccb8526de688a4/docs/commands/publish.md)
- [Incremental publishing](https://github.com/Azure/apiops-cli/blob/129fb326e6878c2bedd45e8ae4ccb8526de688a4/docs/guides/incremental-publish.md)
- [Environment overrides](https://github.com/Azure/apiops-cli/blob/129fb326e6878c2bedd45e8ae4ccb8526de688a4/docs/guides/environment-overrides.md)
- [Filtering guide](https://github.com/Azure/apiops-cli/blob/129fb326e6878c2bedd45e8ae4ccb8526de688a4/docs/guides/filtering-resources.md)
- [Copilot prompt files](https://github.com/Azure/apiops-cli/blob/129fb326e6878c2bedd45e8ae4ccb8526de688a4/docs/guides/prompt-files.md)
- [Microsoft Learn overview](https://learn.microsoft.com/en-us/azure/api-management/how-to-manage-apiops-cli)

Two documentation inconsistencies matter for this pin: the implementation/specific incremental guide uses the selected commit versus its parent; and the secret-redaction guard rejects unresolved placeholders even though some older override prose says they are skipped. The exercises assert the behavior observed in the pinned implementation.
