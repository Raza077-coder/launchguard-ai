# Security

LaunchGuard AI treats website scanning as a controlled, high-risk workflow. The MVP includes built-in protections against SSRF and unsafe browser automation.

## Threats addressed

- Localhost and loopback targets
- Private, reserved, and link-local IP ranges
- Cloud metadata endpoints
- Malicious redirect chains
- Invalid or unexpected URL schemes
- Excessive crawl depth and page counts
- Arbitrary code execution in scans
- Unsafe repository path operations

## Runtime protections

- Validation of destination IPs and redirect targets before each request.
- Blocking of private IP ranges and localhost.
- Strict timeout budgets and page limits.
- Browser automation in a controlled environment with limited concurrency.
- Path validation and repository guardrails for patch generation.
- Sanitization of output before sending to the frontend.

## Security requirements for deployment

- Run scans in an isolated process or container.
- Use a dedicated browser user profile and restricted network policy.
- Do not expose internal exception messages or credentials in API responses.
- Require user authorization before any repository write or patch approval action.
