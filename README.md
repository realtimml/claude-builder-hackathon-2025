# 🎯 Hackathon Presentation Generator

Transform your GitHub repository and Devpost submission into a stunning presentation automatically using AI!

## Overview

This web application takes a hackathon team's GitHub repository and Devpost link, analyzes them using Claude AI, and generates a professional presentation in Canva. Perfect for hackathon teams who need to create compelling presentations for judges quickly.

## Features

- 🔍 **Automatic Data Extraction**: Fetches repository data from GitHub API and scrapes Devpost submissions
- 🤖 **AI-Powered Content Generation**: Uses Claude AI to analyze and structure presentation content
- 🎨 **Canva Integration**: Creates presentations directly in Canva with proper formatting
- ⚡ **Fast & Easy**: Generate a complete presentation in minutes
- 🎭 **Beautiful UI**: Modern, responsive interface with real-time progress tracking

## Architecture

### Frontend
- **React** + **TypeScript** + **Vite**
- Modern UI with gradient backgrounds and animations
- Real-time progress indicators
- Responsive design for all devices

### Backend
- **Python** + **FastAPI**
- **PyGithub** for GitHub API integration
- **BeautifulSoup4** for Devpost scraping
- **Anthropic SDK** for Claude AI
- **Canva Connect API** for presentation creation

## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v18 or higher)
- Python 3.9 or higher
- pip (Python package manager)
- npm or yarn

You'll also need API keys for:
- Anthropic Claude API
- GitHub Personal Access Token (optional but recommended)
- Canva Connect API credentials

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hackathon-presentation-generator.git
cd hackathon-presentation-generator
```

### 2. Backend Setup

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit the `.env` file with your API keys:

```env
CLAUDE_API_KEY=your_anthropic_api_key_here
GITHUB_TOKEN=your_github_token_here
CANVA_CLIENT_ID=your_canva_client_id_here
CANVA_CLIENT_SECRET=your_canva_client_secret_here
PORT=8000
FRONTEND_URL=http://localhost:5173
```

### 3. Frontend Setup

```bash
cd ../front_end

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Start the Backend Server

In a separate terminal:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment if not already active
python main.py
```

The backend will start on `http://localhost:8000`

## Getting API Keys

### Claude API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

### GitHub Token
1. Go to GitHub Settings > Developer Settings > Personal Access Tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:user`
4. Copy the token

### Canva API Credentials
1. Visit [Canva Developers Portal](https://www.canva.dev/)
2. Create a new app
3. Get your Client ID and Client Secret
4. Configure OAuth redirect URI: `http://localhost:8000/api/canva/callback`

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Enter your GitHub repository URL (e.g., `https://github.com/username/repo`)
3. Enter your Devpost project URL (e.g., `https://devpost.com/software/project-name`)
4. Click "Generate Presentation ✨"
5. Wait for the AI to analyze your project (this takes 30-60 seconds)
6. Click the "Open in Canva" button to view and edit your presentation

## Project Structure

```
hackathon-presentation-generator/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment variables template
│   └── services/
│       ├── github_service.py     # GitHub API integration
│       ├── devpost_service.py    # Devpost scraping
│       ├── claude_service.py     # Claude AI integration
│       └── canva_service.py      # Canva API integration
├── front_end/
│   ├── src/
│   │   ├── App.tsx               # Main React component
│   │   ├── App.css               # Application styles
│   │   └── index.css             # Global styles
│   ├── package.json              # Node dependencies
│   └── vite.config.ts            # Vite configuration
└── README.md                      # This file
```

## API Endpoints

### `GET /api/health`
Health check endpoint to verify all services are configured correctly.

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

### `POST /api/generate-presentation`
Generate a presentation from GitHub and Devpost URLs.

**Request Body:**
```json
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
    "presentation_title": "Project Title",
    "slides": [...]
  }
}
```

## Presentation Structure

The generated presentation includes:

1. **Title Slide**: Project name, tagline, and team members
2. **Problem & Motivation** (2-3 slides): What problem does this solve and why?
3. **Solution Overview** (2 slides): What is the solution and how does it work?
4. **Technical Deep Dive** (2 slides): Architecture, tech stack, and innovations
5. **Demo & Features** (2 slides): Core functionality and user journey
6. **Impact & Use Cases** (1 slide): Real-world applications and potential impact
7. **Challenges & Learning** (1 slide): What the team learned and future plans

## Troubleshooting

### Backend Issues

**Error: "CLAUDE_API_KEY environment variable is required"**
- Make sure you've created a `.env` file in the `backend/` directory
- Verify your Claude API key is correct

**Error: "Failed to fetch GitHub data"**
- Check if the GitHub URL is correct
- Verify your GitHub token has the right permissions
- Public repos work without a token but have lower rate limits

**Error: "Failed to create Canva presentation"**
- Verify your Canva API credentials are correct
- Check that your Canva app has the right permissions
- The presentation data will still be provided even if Canva creation fails

### Frontend Issues

**Blank page or crashes**
- Check the browser console for errors
- Make sure the backend is running on port 8000
- Verify CORS is properly configured

**"Failed to generate presentation" error**
- Check that both URLs are valid and accessible
- Make sure the backend server is running
- Check backend logs for detailed error messages

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd front_end
npm test
```

### Building for Production

```bash
# Frontend
cd front_end
npm run build

# Backend
cd backend
# The FastAPI app can be deployed using Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your hackathon needs!

## Acknowledgments

- Built with [Claude AI](https://www.anthropic.com/) by Anthropic
- Uses [GitHub API](https://docs.github.com/en/rest) for repository data
- Integrates with [Canva Connect API](https://www.canva.dev/) for presentations
- Inspired by hackathon teams everywhere 🚀

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ for hackathon teams everywhere!

