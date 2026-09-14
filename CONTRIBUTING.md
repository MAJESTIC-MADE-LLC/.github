# Contributing

Thank you for helping improve a Majestic Made project. Repository-specific guidance and templates
take precedence over this organization default.

## Before opening an issue

- Use the repository's bug form and include only the minimum reproducible, non-sensitive details.
- Do not post vulnerabilities, credentials, personal records, child data, health information, or
  private documents in an issue. Follow the private process in [SECURITY.md](SECURITY.md).
- Use [SUPPORT.md](SUPPORT.md) for account, billing, data, or general support questions.

## Changes

1. Start from the current `dev` branch and keep the change focused.
2. Follow the repository's setup, test, formatting, and static-analysis instructions.
3. Add or update tests for changed behavior.
4. Document changes to data collection, storage, retention, deletion, authentication, cloud use,
   third-party services, or recurring cost.
5. Open the pull request against `dev`. The `main` branch is release-only and is updated by
   maintainers after the applicable release checks and approvals pass.

Never commit secrets, production data, or generated files that may contain user data. New remote
services and dependencies should have a clear product need, privacy impact, maintenance owner, and
cost justification.
