# Security Policy

## Supported Versions

Security fixes are provided on the latest commit in the default branch.

## Reporting a Vulnerability

Please do not open public issues for potential security vulnerabilities.

Send a report with the following details:

- Affected file/module
- Reproduction steps
- Potential impact
- Suggested remediation (optional)

Use a private communication channel where possible (for example, private email associated with the maintainer profile).

## Dependency Safety

- Keep dependencies updated in `requirements.txt`.
- Review model and tokenizer artifacts from trusted sources only.
- Verify downloaded checkpoint files using checksums when available.

## Model Safety Note

This project can generate synthetic media. Use generated content responsibly and in accordance with platform and local policy requirements.
