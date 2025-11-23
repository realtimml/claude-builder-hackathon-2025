# Backend - Hackathon Presentation Generator

Python FastAPI backend that orchestrates data collection and AI-powered presentation generation.

## Architecture

### Services

#### `github_service.py`
- Uses PyGithub to fetch comprehensive repository data
- Handles URL parsing and validation
- Fetches: README, statistics, languages, commits, contributors, structure
- Error handling for private repos and rate limits

#### `devpost_service.py`
- Web scraper using BeautifulSoup and requests
- Extracts project details from Devpost pages
- Parses: title, tagline, tech stack, inspiration, challenges, accomplishments
- Handles various Devpost page layouts

#### `claude_service.py`
- Integrates with Anthropic Claude API
- Uses Claude's PowerPoint Skill (beta feature)
- Formats data into comprehensive prompts
- Extracts and returns generated .pptx files
- Handles API errors and file extraction

### API Endpoints

#### `POST /api/generate-presentation`
Main endpoint for generating presentations.

**Request:**
```json
{
  "github_url": "https://github.com/username/repo",
  "devpost_url": "https://devpost.com/software/project"
}
```

**Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- Body: PowerPoint file bytes
- Filename: `{project_name}_presentation.pptx`

**Errors:**
- 400: Invalid URLs or validation errors
- 500: Server errors (API failures, processing errors)

#### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run the server:
```bash
python main.py
```

Server runs on `http://localhost:8000`

## Environment Variables

- `ANTHROPIC_API_KEY` (required): Anthropic API key
- `GITHUB_TOKEN` (optional): GitHub PAT for higher rate limits

## API Documentation

When the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Claude PowerPoint Skill

This backend uses Claude's PowerPoint Skill (beta feature) to generate presentations. The skill is accessed via:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "anthropic",
                "skill_id": "pptx",
                "version": "latest"
            }
        ]
    },
    ...
)
```

## Logging

Logging is configured at INFO level. Check console output for:
- Request processing steps
- Data fetching progress
- API calls and responses
- Errors and warnings

## Error Handling

The backend handles:
- Invalid GitHub URLs
- Private or non-existent repositories
- GitHub API rate limits
- Invalid Devpost URLs
- Network errors
- Claude API errors
- File extraction failures

All errors are logged and returned with appropriate HTTP status codes.
