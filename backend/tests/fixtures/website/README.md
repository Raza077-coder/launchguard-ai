# Fixture Website

This directory contains a deterministic local website for testing LaunchGuard AI's scanner.

## Pages

- `index.html` — A valid page with correct metadata and structure.
- `missing-title.html` — Missing `<title>` tag (SEO issue).
- `missing-meta.html` — Missing meta description (SEO issue).
- `missing-alt.html` — Images without alt text (accessibility issue).
- `broken-links.html` — Contains links to non-existent pages (link validation issue).
- `mobile.html` — Unresponsive layout for mobile viewport testing.

## Running the Fixture Locally

To serve this directory locally:

```bash
python -m http.server 8888 --directory backend/tests/fixtures/website
```

Then scan:

```
http://localhost:8888
```

## Expected Findings

When LaunchGuard scans `http://localhost:8888`, it should detect:

1. **missing-title.html**: Missing or empty `<title>` tag → medium severity SEO finding
2. **missing-meta.html**: Missing meta description → low severity SEO finding
3. **missing-alt.html**: Multiple images missing alt text → medium severity accessibility finding
4. **broken-links.html**: Broken internal links returning 404 → medium severity broken-link finding
5. **mobile.html**: Layout overflow on mobile viewport → low/medium severity responsive issue

All findings should be persisted to SQLite with accurate timestamps and evidence.
