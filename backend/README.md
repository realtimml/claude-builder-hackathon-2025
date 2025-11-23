# Backend - Hackathon Presentation Generator

FastAPI backend for the Hackathon Presentation Generator.

## Overview

This backend service orchestrates the entire presentation generation process:
1. Fetches repository data from GitHub API
2. Scrapes Devpost submission details
3. Uses Claude AI to analyze and structure content
4. Creates presentation in Canva using their Connect API

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **PyGithub**: Official GitHub API wrapper
- **BeautifulSoup4**: HTML parsing for Devpost scraping
- **Anthropic SDK**: Claude AI integration
- **httpx**: Async HTTP client for Canva API

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
CLAUDE_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
CANVA_CLIENT_ID=...
CANVA_CLIENT_SECRET=...
PORT=8000
FRONTEND_URL=http://localhost:5173
```

## Running the Server

### Development Mode

```bash
python main.py
```

Or with Uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Services

### GitHub Service (`services/github_service.py`)

Handles all GitHub API interactions:
- Repository metadata extraction
- README content fetching
- Language and dependency analysis
- Contributor information
- Repository structure analysis

**Key Methods:**
- `fetch_repo_data(github_url)`: Main method to get all repository data

### Devpost Service (`services/devpost_service.py`)

Web scraping for Devpost submissions:
- Project title and tagline
- Structured sections (inspiration, challenges, learnings, etc.)
- Team member information
- Tech stack tags
- Project images

**Key Methods:**
- `scrape_devpost(devpost_url)`: Main scraping method

### Claude Service (`services/claude_service.py`)

AI-powered content generation:
- Analyzes combined GitHub and Devpost data
- Structures content into presentation slides
- Generates compelling narratives for judges
- Creates speaker notes

**Key Methods:**
- `generate_presentation_content(github_data, devpost_data)`: Generates structured presentation

### Canva Service (`services/canva_service.py`)

Canva API integration:
- OAuth authentication
- Design creation
- Slide population
- Export and sharing

**Key Methods:**
- `create_presentation(presentation_data)`: Creates and populates Canva presentation

## API Endpoints

### Health Check

```http
GET /api/health
```

**Response:**
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

### Generate Presentation

```http
POST /api/generate-presentation
Content-Type: application/json

{
  "github_url": "https://github.com/username/repo",
  "devpost_url": "https://devpost.com/software/project-name"
}
```

**Response:**
```json
{
  "success": true,
  "canva_url": "https://www.canva.com/design/...",
  "message": "Presentation generated successfully!",
  "presentation_data": {
    "presentation_title": "Amazing Hackathon Project",
    "team_members": ["Alice", "Bob", "Charlie"],
    "slides": [
      {
        "slide_number": 1,
        "title": "Project Title",
        "content": ["Bullet point 1", "Bullet point 2"],
        "speaker_notes": "Introduction notes..."
      }
    ]
  }
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid URLs)
- `500`: Server error (API failures, parsing errors)

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limits

Be aware of rate limits for external APIs:
- **GitHub API**: 60 requests/hour (unauthenticated), 5000/hour (with token)
- **Claude API**: Depends on your plan
- **Canva API**: Check your developer dashboard

## Development

### Adding New Services

1. Create a new file in `services/` directory
2. Implement the service class
3. Import and initialize in `main.py`
4. Use in the endpoint handlers

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLAUDE_API_KEY` | Anthropic API key | Yes |
| `GITHUB_TOKEN` | GitHub personal access token | Recommended |
| `CANVA_CLIENT_ID` | Canva app client ID | Yes |
| `CANVA_CLIENT_SECRET` | Canva app client secret | Yes |
| `CANVA_REDIRECT_URI` | OAuth redirect URI | No |
| `PORT` | Server port | No (default: 8000) |
| `FRONTEND_URL` | Frontend URL for CORS | No (default: localhost:5173) |

## Deployment

### Docker (Coming Soon)

```bash
docker build -t presentation-generator-backend .
docker run -p 8000:8000 --env-file .env presentation-generator-backend
```

### Cloud Platforms

The FastAPI app can be deployed to:
- **Heroku**: Use Procfile with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **AWS Lambda**: Use Mangum adapter
- **Google Cloud Run**: Containerize with Docker
- **Railway/Render**: Direct Python deployment

## Troubleshooting

### Import Errors

Make sure virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### GitHub API Rate Limit

Use a GitHub token to increase rate limits:
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### Canva API Errors

- Verify credentials in Canva Developer Portal
- Check OAuth redirect URI matches exactly
- Ensure required scopes are granted

### Claude API Errors

- Verify API key is correct
- Check you have sufficient credits
- Monitor usage in Anthropic Console

## Support

For issues specific to:
- GitHub API: https://docs.github.com/en/rest
- Canva API: https://www.canva.dev/docs/connect/
- Claude API: https://docs.anthropic.com/
- FastAPI: https://fastapi.tiangolo.com/

## License

MIT

