from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
import os
from dotenv import load_dotenv
from services.github_service import GitHubService
from services.devpost_service import DevpostService
from services.claude_service import ClaudeService
import tempfile
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hackathon Presentation Generator")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PresentationRequest(BaseModel):
    github_url: HttpUrl
    devpost_url: HttpUrl

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/api/generate-presentation")
async def generate_presentation(request: PresentationRequest):
    """
    Generate a PowerPoint presentation from GitHub repo and Devpost submission
    """
    try:
        logger.info(f"Generating presentation for GitHub: {request.github_url}, Devpost: {request.devpost_url}")
        
        # Initialize services
        github_service = GitHubService(os.getenv("GITHUB_TOKEN"))
        devpost_service = DevpostService()
        claude_service = ClaudeService(os.getenv("ANTHROPIC_API_KEY"))
        
        # Step 1: Fetch GitHub data
        logger.info("Fetching GitHub repository data...")
        github_data = await github_service.fetch_repo_data(str(request.github_url))
        
        # Step 2: Fetch Devpost data
        logger.info("Fetching Devpost submission data...")
        devpost_data = await devpost_service.fetch_project_data(str(request.devpost_url))
        
        # Step 3: Generate presentation using Claude with PowerPoint skill
        logger.info("Generating presentation with Claude...")
        pptx_bytes = await claude_service.generate_presentation(github_data, devpost_data)
        
        # Step 4: Save to temporary file and return
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_file:
            tmp_file.write(pptx_bytes)
            tmp_path = tmp_file.name
        
        # Extract project name for filename
        project_name = devpost_data.get("title", "presentation").replace(" ", "_")
        filename = f"{project_name}_presentation.pptx"
        
        logger.info(f"Presentation generated successfully: {filename}")
        
        return FileResponse(
            tmp_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=filename,
            background=None
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating presentation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate presentation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


