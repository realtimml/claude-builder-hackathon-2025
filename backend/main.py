from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv
import os
from typing import Optional

from services.github_service import GitHubService
from services.devpost_service import DevpostService
from services.claude_service import ClaudeService
from services.canva_service import CanvaService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Hackathon Presentation Generator",
    description="Generate professional presentations from GitHub repos and Devpost submissions",
    version="1.0.0"
)

# CORS configuration
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:5173"),
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class PresentationRequest(BaseModel):
    github_url: str
    devpost_url: str

class PresentationResponse(BaseModel):
    success: bool
    canva_url: Optional[str] = None
    message: str
    presentation_data: Optional[dict] = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hackathon Presentation Generator API", "status": "running"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "github": bool(os.getenv("GITHUB_TOKEN")),
            "claude": bool(os.getenv("CLAUDE_API_KEY")),
            "canva": bool(os.getenv("CANVA_CLIENT_ID")) and bool(os.getenv("CANVA_CLIENT_SECRET"))
        }
    }

@app.post("/api/generate-presentation", response_model=PresentationResponse)
async def generate_presentation(request: PresentationRequest):
    """
    Main endpoint to generate a presentation from GitHub and Devpost URLs
    
    Args:
        request: PresentationRequest containing github_url and devpost_url
        
    Returns:
        PresentationResponse with Canva URL and presentation data
    """
    try:
        # Initialize services
        github_service = GitHubService()
        devpost_service = DevpostService()
        claude_service = ClaudeService()
        canva_service = CanvaService()
        
        # Step 1: Fetch GitHub repository data
        print(f"Fetching GitHub data from: {request.github_url}")
        github_data = await github_service.fetch_repo_data(request.github_url)
        
        # Step 2: Scrape Devpost data
        print(f"Scraping Devpost data from: {request.devpost_url}")
        devpost_data = await devpost_service.scrape_devpost(request.devpost_url)
        
        # Step 3: Generate presentation content with Claude
        print("Generating presentation content with Claude...")
        presentation_content = await claude_service.generate_presentation_content(
            github_data, devpost_data
        )
        
        # Step 4: Create Canva presentation
        print("Creating Canva presentation...")
        canva_url = await canva_service.create_presentation(presentation_content)
        
        return PresentationResponse(
            success=True,
            canva_url=canva_url,
            message="Presentation generated successfully!",
            presentation_data=presentation_content
        )
        
    except Exception as e:
        print(f"Error generating presentation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

