# Contributing

Contributions are welcome. This project is intentionally scoped for a local-first MVP, so changes should prioritize maintainability, deterministic behavior, and evidence-based reporting.

## Local development workflow

1. Create a Python virtual environment and install backend dependencies.
2. Install Node.js dependencies for the frontend.
3. Run backend tests with Pytest.
4. Run frontend linting and type checks.
5. Verify changes against the local fixture website.

## Coding expectations

- Keep scanner logic deterministic and explainable.
- Never fabricate results.
- Treat AI outputs as advisory suggestions, not commands.
- Default to safe repository operations: review before apply.
- Prefer minimal, human-readable patches.
