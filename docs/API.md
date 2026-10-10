# LaunchGuard AI API documentation

## Health

- `GET /api/health` – returns server status and app mode

## Projects

- `GET /api/projects` – list projects
- `POST /api/projects` – create a project
- `GET /api/projects/{project_id}` – fetch project details
- `DELETE /api/projects/{project_id}` – delete a project

## Scans

- `POST /api/scans` – create a scan job
- `GET /api/scans` – list scans
- `GET /api/scans/{scan_id}` – fetch scan state
- `POST /api/scans/{scan_id}/cancel` – cancel a scan
- `GET /api/scans/{scan_id}/events` – list scan event logs
- `GET /api/scans/{scan_id}/findings` – list findings
- `GET /api/findings/{finding_id}` – get detail for a finding
- `PATCH /api/findings/{finding_id}` – update finding status
- `GET /api/scans/{scan_id}/report` – generate report JSON

## Repairs

- `POST /api/repair-plans`
- `POST /api/repair-proposals`
- `GET /api/repair-proposals/{proposal_id}`
- `POST /api/repair-proposals/{proposal_id}/approve`
- `POST /api/repair-proposals/{proposal_id}/reject`
- `POST /api/verification-runs`
