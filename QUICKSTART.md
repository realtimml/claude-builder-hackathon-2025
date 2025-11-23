# 🚀 Quick Start Guide

Get the Hackathon Presentation Generator running in 5 minutes!

## Prerequisites Check

Make sure you have:
- ✅ Python 3.9+ installed: `python --version`
- ✅ Node.js 18+ installed: `node --version`
- ✅ Git installed: `git --version`

## Step 1: Get API Keys (5-10 minutes)

### Claude API Key (Required)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Click "Get API Keys"
4. Create a new key and copy it

### GitHub Token (Recommended)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`
4. Generate and copy the token

### Canva API (Required)
1. Go to https://www.canva.dev/
2. Create a developer account
3. Create a new app
4. Copy Client ID and Client Secret
5. Set redirect URI to: `http://localhost:8000/api/canva/callback`

## Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate
# OR on Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
CLAUDE_API_KEY=your_anthropic_key_here
GITHUB_TOKEN=your_github_token_here
CANVA_CLIENT_ID=your_canva_client_id_here
CANVA_CLIENT_SECRET=your_canva_secret_here
PORT=8000
FRONTEND_URL=http://localhost:5173
EOF

# Edit .env with your actual API keys
nano .env  # or use your preferred editor
```

## Step 3: Frontend Setup (1 minute)

```bash
# Open a new terminal
cd front_end

# Install dependencies
npm install
```

## Step 4: Start the Application (30 seconds)

### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # if not already active
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend:
```bash
cd front_end
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

## Step 5: Test It Out! (1 minute)

1. Open http://localhost:5173 in your browser
2. Enter a test GitHub URL: `https://github.com/anthropics/anthropic-sdk-python`
3. Enter a test Devpost URL (or use a real hackathon project)
4. Click "Generate Presentation ✨"

## Testing the Health Endpoint

Before generating a presentation, check if all services are configured:

```bash
curl http://localhost:8000/api/health
```

You should see:
```json
{
  "status": "healthy",
  "services": {
    "github": true,
    "claude": true,
    "canva": true
  }
}
```

If any service shows `false`, double-check your API keys in `.env`

## Common Issues

### "Module not found" error
```bash
# Make sure virtual environment is activated
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### "Connection refused" error
- Make sure backend is running on port 8000
- Check if another process is using the port: `lsof -i :8000`

### "CORS error" in browser
- Verify `FRONTEND_URL=http://localhost:5173` in backend `.env`
- Restart the backend server after changing `.env`

### "Invalid API key" errors
- Double-check your API keys have no extra spaces
- Make sure you've saved the `.env` file
- Restart the backend server after updating `.env`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [backend/README.md](backend/README.md) for API details
- Customize the presentation structure in `backend/services/claude_service.py`
- Modify the UI styling in `front_end/src/App.css`

## Need Help?

- Check the main README for troubleshooting
- Open an issue on GitHub
- Review the API documentation at http://localhost:8000/docs

Happy hacking! 🎉

