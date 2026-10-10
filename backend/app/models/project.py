from __future__ import annotations

from app.database import init_db
from app.main import app

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn

    init_db()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
