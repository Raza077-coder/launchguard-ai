from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
FIXTURE_DIR = BACKEND_DIR / "tests" / "fixtures" / "website"
