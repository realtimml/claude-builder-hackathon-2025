# Project Summary - Hackathon Presentation Generator

## What Was Built

A full-stack web application that automatically generates professional presentations from GitHub repositories and Devpost submissions using AI.

## Architecture

### Frontend (React + TypeScript + Vite)
**Location:** `front_end/`

**Key Features:**
- Modern, gradient-based UI with glassmorphism effects
- Form inputs with URL validation
- Multi-stage loading indicators (Fetching → Analyzing → Creating)
- Success view with Canva link and presentation preview
- Comprehensive error handling
- Fully responsive design

**Files Created:**
- `src/App.tsx` - Main React component with all UI logic
- `src/App.css` - Beautiful styling with animations
- `src/index.css` - Global styles

### Backend (Python + FastAPI)
**Location:** `backend/`

**Core Components:**

1. **Main API** (`main.py`)
   - FastAPI application with CORS configuration
   - Health check endpoint
   - Main presentation generation endpoint
   - Request/response models with Pydantic

2. **GitHub Service** (`services/github_service.py`)
   - Uses PyGithub library for official API access
   - Fetches repository metadata, README, languages, dependencies
   - Analyzes repository structure (docs, tests, CI/CD)
   - Gets contributor information
   - Handles various GitHub URL formats

3. **Devpost Service** (`services/devpost_service.py`)
   - Web scraping with BeautifulSoup4
   - Extracts all standard Devpost sections (inspiration, challenges, etc.)
   - Parses team member information
   - Extracts tech stack tags
   - Collects project images
   - Robust error handling for missing content

4. **Claude Service** (`services/claude_service.py`)
   - Integrates Anthropic's Claude API
   - Creates comprehensive prompts combining GitHub + Devpost data
   - Generates structured presentation content
   - Returns JSON with slide titles, content, and speaker notes
   - Handles JSON parsing from Claude responses

5. **Canva Service** (`services/canva_service.py`)
   - Canva Connect API integration
   - OAuth 2.0 client credentials flow
   - Creates presentation designs
   - Adds pages and text elements
   - Returns shareable edit URLs
   - Graceful error handling

## Presentation Structure

Generated presentations include 11 slides:

1. **Title Slide** - Project name, tagline, team
2-3. **Problem & Motivation** - What problem and why
4-5. **Solution Overview** - The solution and how it works
6-7. **Technical Deep Dive** - Architecture and tech stack
8-9. **Demo & Features** - Core functionality
10. **Impact & Use Cases** - Real-world applications
11. **Challenges & Learning** - Learnings and future plans

## API Flow

```
User Input (GitHub + Devpost URLs)
         ↓
Frontend (React)
         ↓
POST /api/generate-presentation
         ↓
Backend (FastAPI)
         ↓
    ┌────┴────┬──────────┬────────┐
    ↓         ↓          ↓        ↓
GitHub API  Devpost  Claude API  Canva API
    ↓         ↓          ↓        ↓
    └────┬────┴──────────┴────────┘
         ↓
  Canva URL + Presentation Data
         ↓
    Frontend Display
```

## Documentation

Comprehensive documentation created:

1. **README.md** (Root)
   - Project overview
   - Complete setup instructions
   - API key acquisition guides
   - Usage instructions
   - Troubleshooting guide

2. **QUICKSTART.md**
   - 5-minute setup guide
   - Step-by-step instructions
   - Common issues and solutions

3. **backend/README.md**
   - Backend-specific documentation
   - Service descriptions
   - API endpoint details
   - Deployment options

4. **front_end/README.md**
   - Frontend-specific documentation
   - Development guide
   - Build instructions

## Testing

**Test Script:** `backend/test_services.py`
- Validates all services are configured correctly
- Checks environment variables
- Tests GitHub API connection
- Verifies Claude and Canva initialization

## Dependencies

### Backend (`backend/requirements.txt`)
- fastapi - Modern web framework
- uvicorn - ASGI server
- PyGithub - GitHub API wrapper
- beautifulsoup4 - HTML parsing
- requests - HTTP client
- anthropic - Claude API
- python-dotenv - Environment variables
- httpx - Async HTTP client
- pydantic - Data validation

### Frontend (`front_end/package.json`)
- react 19.1.1
- react-dom 19.1.1
- typescript 5.9.3
- vite 7.1.7
- @vitejs/plugin-react 5.0.4

## Environment Variables Required

```env
CLAUDE_API_KEY=<Anthropic API key>
GITHUB_TOKEN=<GitHub personal access token>
CANVA_CLIENT_ID=<Canva app client ID>
CANVA_CLIENT_SECRET=<Canva app client secret>
PORT=8000
FRONTEND_URL=http://localhost:5173
```

## Security Considerations

- API keys stored in `.env` (not committed to git)
- CORS properly configured for frontend origin
- Input validation on URLs
- Error messages don't expose sensitive information
- Rate limiting awareness for external APIs

## Future Enhancements

Potential improvements:

1. **Caching** - Cache GitHub and Devpost data to reduce API calls
2. **Templates** - Multiple Canva template options
3. **Customization** - User-selectable presentation styles
4. **Batch Processing** - Generate multiple presentations
5. **Export Options** - PDF, PowerPoint export in addition to Canva
6. **User Accounts** - Save generated presentations
7. **Analytics** - Track most used features
8. **AI Improvements** - More sophisticated content generation
9. **Image Integration** - Automatically include project screenshots
10. **Collaboration** - Share and edit presentations with team

## Project Stats

- **Total Files Created:** 15+
- **Lines of Code:** ~2,000+
- **Services Integrated:** 4 (GitHub, Devpost, Claude, Canva)
- **API Endpoints:** 2
- **Development Time:** ~2 hours
- **Technologies Used:** 10+

## How to Use

1. **Setup** (5 minutes)
   - Install dependencies
   - Configure API keys
   - Start backend and frontend

2. **Generate Presentation** (1 minute)
   - Enter GitHub URL
   - Enter Devpost URL
   - Click generate

3. **Edit in Canva** (5-10 minutes)
   - Open in Canva
   - Customize design
   - Add images/graphics
   - Export/present

Total time from setup to presentation: **15-20 minutes**

## Success Criteria ✅

- ✅ Full-stack application working
- ✅ GitHub API integration
- ✅ Devpost scraping
- ✅ Claude AI content generation
- ✅ Canva API integration
- ✅ Beautiful, responsive UI
- ✅ Comprehensive documentation
- ✅ Error handling throughout
- ✅ Easy setup process
- ✅ Ready for hackathon use

## Deployment Ready

The application is ready to be deployed:

- **Frontend:** Can be deployed to Vercel, Netlify, or any static host
- **Backend:** Can be deployed to Heroku, Railway, Render, AWS, GCP, etc.
- **Docker:** Ready for containerization
- **CI/CD:** Can be integrated with GitHub Actions

---

**Built with ❤️ for hackathon teams everywhere!**

