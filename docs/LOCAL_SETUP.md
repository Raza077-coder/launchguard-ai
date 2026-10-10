# Local setup

## Requirements

- Python 3.11+
- Node.js 18+
- Git
- Playwright Chromium

## Windows PowerShell

```powershell
# Clone
cd C:\workspace
git clone https://github.com/Raza077-coder/launchguard-ai.git
cd launchguard-ai

# Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
cd backend
pip install -r requirements.txt
python -m playwright install chromium

# Frontend
cd ..\frontend
npm install

# Run backend
cd ..\backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run frontend in a second terminal
cd ..\frontend
npm run dev
```

## Optional Ollama

Set environment variables:

```powershell
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "llama3.1"
```

If the local model is unavailable, the app should fall back to deterministic results without breaking the scan.
