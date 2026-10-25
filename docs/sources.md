# Official sources and version

Customer exercises use the published npm package `@azure-tools/apiops-cli@1.0.5`. The original assessment also inspected source commit `129fb326e6878c2bedd45e8ae4ccb8526de688a4`. Validation records identify the actual installed package and its integrity metadata.

- [Official repository](https://github.com/Azure/apiops-cli)
- [Getting started](https://github.com/Azure/apiops-cli/blob/main/docs/getting-started.md)
- [Publish reference](https://github.com/Azure/apiops-cli/blob/main/docs/commands/publish.md)
- [Incremental publish](https://github.com/Azure/apiops-cli/blob/main/docs/guides/incremental-publish.md)
- [Environment overrides](https://github.com/Azure/apiops-cli/blob/main/docs/guides/environment-overrides.md)
- [Filtering resources](https://github.com/Azure/apiops-cli/blob/main/docs/guides/filtering-resources.md)
- [Copilot prompt files](https://github.com/Azure/apiops-cli/blob/main/docs/guides/prompt-files.md)
- [Microsoft Learn](https://learn.microsoft.com/en-us/azure/api-management/how-to-manage-apiops-cli)

Specific implementation behavior takes precedence over older inconsistent prose: incremental mode uses the selected commit versus its parent, unresolved redaction markers reject publishing, and init overwrite conflicts return exit 1. The labs assert these outcomes.
