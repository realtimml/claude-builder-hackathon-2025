# 🎯 Hackathon Presentation Generator

An AI-powered web application that automatically generates professional PowerPoint presentations for hackathon teams by analyzing their GitHub repository and Devpost submission using Claude AI's PowerPoint skill.

## Features

- 🤖 **AI-Powered Analysis**: Claude AI deeply analyzes your GitHub repo and Devpost submission
- 📊 **Comprehensive Presentations**: Automatically generates 10-15 slide presentations covering:
  - Problem statement and solution
  - Technical architecture and implementation
  - Impact and use cases
  - Team and development journey
  - Challenges and accomplishments
- 🎨 **Professional Design**: Claude creates visually appealing slides with proper hierarchy
- ⚡ **Fast Generation**: Get your presentation in minutes
- 📥 **Direct Download**: Download your .pptx file directly

## Tech Stack

### Frontend
- React 19 with TypeScript
- Vite for fast development
- Modern CSS with gradient backgrounds

### Backend
- FastAPI (Python)
- Anthropic Claude API with PowerPoint Skill
- PyGithub for repository analysis
- BeautifulSoup for web scraping

## Prerequisites

- Node.js 18+ and npm
- Python 3.12+
- Anthropic API key
- (Optional) GitHub Personal Access Token for higher rate limits

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `.env` and add your API keys:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GITHUB_TOKEN=your_github_token_here_optional
```

### 2. Frontend Setup

```bash
cd front_end

# Install dependencies
npm install
```

## Running the Application

### Start the Backend Server

```bash
cd backend
source venv/bin/activate  # If not already activated
python main.py
```

The backend will run on `http://localhost:8000`

### Start the Frontend Development Server

In a new terminal:

```bash
cd front_end
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. Open your browser to `http://localhost:5173`
2. Enter your GitHub repository URL (e.g., `https://github.com/username/repo`)
3. Enter your Devpost project URL (e.g., `https://devpost.com/software/project-name`)
4. Click "Generate Presentation"
5. Wait for the AI to analyze and generate your presentation
6. Your PowerPoint file will automatically download

## Testing with Sample Data

You can test the application with any public GitHub repository and Devpost submission. For example:

**GitHub URL:** `https://github.com/yourusername/your-hackathon-project`
**Devpost URL:** `https://devpost.com/software/your-project`

## API Endpoints

### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### `POST /api/generate-presentation`
Generate a presentation from GitHub and Devpost URLs

**Request:**
```json
{
  "github_url": "https://github.com/username/repo",
  "devpost_url": "https://devpost.com/software/project"
}
```

**Response:**
PowerPoint file download (.pptx)

## How It Works

1. **Data Collection**
   - Fetches comprehensive data from GitHub: README, commits, contributors, languages, statistics
   - Scrapes Devpost submission: inspiration, challenges, accomplishments, tech stack

2. **AI Analysis**
   - Claude AI analyzes all collected data
   - Structures content into presentation-ready format
   - Identifies key points and creates compelling narrative

3. **Presentation Generation**
   - Uses Claude's PowerPoint Skill to generate professional slides
   - Automatically designs layouts and visual hierarchy
   - Includes speaker notes for each slide

4. **Delivery**
   - Returns ready-to-use PowerPoint file
   - Can be edited further in PowerPoint/Keynote/Google Slides

## Project Structure

```
.
├── backend/
│   ├── services/
│   │   ├── github_service.py      # GitHub API integration
│   │   ├── devpost_service.py     # Devpost scraping
│   │   └── claude_service.py      # Claude AI integration
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment variables
├── front_end/
│   ├── src/
│   │   ├── App.tsx               # Main React component
│   │   ├── App.css               # Component styles
│   │   └── index.css             # Global styles
│   ├── package.json              # Node dependencies
│   └── vite.config.ts            # Vite configuration
└── README.md
```

## Environment Variables

### Backend (.env)

- `ANTHROPIC_API_KEY` (required): Your Anthropic API key from https://console.anthropic.com/
- `GITHUB_TOKEN` (optional): GitHub Personal Access Token for higher API rate limits

## Troubleshooting

### "Repository not found or is private"
- Ensure the GitHub URL is correct and the repository is public
- If using a private repository, add a GitHub token with appropriate permissions

### "GitHub API rate limit exceeded"
- Add a `GITHUB_TOKEN` to your `.env` file for higher rate limits

### "Failed to fetch Devpost page"
- Verify the Devpost URL is correct and accessible
- Check your internet connection

### CORS errors
- Ensure the backend is running on port 8000
- Check that CORS middleware is properly configured in `main.py`

## Contributing

This is a hackathon project. Feel free to fork and modify for your own use!

## License

MIT License - feel free to use this for your hackathon presentations!

## Acknowledgments

- Powered by [Anthropic Claude AI](https://www.anthropic.com/)
- Built for the Claude Builder Hackathon 2025
