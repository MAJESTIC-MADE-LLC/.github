# Existing dependency alert review

The four existing App-Template alerts concern jose and [GHSA-vm9r-h74p-hg97](https://github.com/advisories/GHSA-vm9r-h74p-hg97). They reference hosting/control_app, hosting/coordinator, hosting/reference_app and majestic_hosting lockfiles. Current source resolves jose0.3.5+2; the advisory identifies0.3.5+1 or later as patched. Read-only inspection confirmed the resolved configured-key-only fix, and the maintained workspace grant verifier additionally rejects token-selected header keys and verifies against its configured trusted key.

These alerts do not establish a current blocker for the resolved patched graph. Continued matching around the build suffix is an inference, not a confirmed provider diagnosis. No alert was dismissed and no general security-audit claim is made. [Pinned verifier source](https://github.com/MAJESTIC-MADE-LLC/App-Template/blob/5e72d2e60f9c77ab713a671b05fdedd11e7ceb0a/packages/majestic_hosting/lib/src/workspace_grant.dart).
