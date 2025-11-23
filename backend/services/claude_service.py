import anthropic
from typing import Dict, List
import logging
import base64
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
import io

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service for generating presentations using Claude with PowerPoint skill"""
    
    def __init__(self, api_key: str):
        """
        Initialize Claude service
        
        Args:
            api_key: Anthropic API key
        """
        if not api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def _format_github_data(self, github_data: Dict) -> str:
        """Format GitHub data for Claude prompt"""
        # Safely format languages
        languages = ", ".join(str(lang) for lang in github_data.get("languages", {}).keys() if lang)
        if not languages:
            languages = "Not specified"
        
        # Safely format contributors, filtering out None names
        contributors_list = github_data.get("contributors", [])[:5]
        contributors = ", ".join(
            str(c.get("name", c.get("username", "Unknown"))) 
            for c in contributors_list 
            if c and (c.get("name") or c.get("username"))
        )
        if not contributors:
            contributors = "Not specified"
        
        # Safely format topics
        topics = ", ".join(str(t) for t in github_data.get("topics", []) if t)
        if not topics:
            topics = "None"
        
        # Safely format structure
        structure = ", ".join(str(s) for s in github_data.get("structure", [])[:20] if s)
        if not structure:
            structure = "Not specified"
        
        formatted = f"""
## GitHub Repository Analysis

**Project Name:** {github_data.get("name", "Unknown")}
**Description:** {github_data.get("description", "No description")}
**Homepage:** {github_data.get("homepage", "N/A")}
**License:** {github_data.get("license", "N/A")}

**Statistics:**
- Stars: {github_data.get("statistics", {}).get("stars", 0)}
- Forks: {github_data.get("statistics", {}).get("forks", 0)}
- Open Issues: {github_data.get("statistics", {}).get("open_issues", 0)}

**Tech Stack (Languages):**
{languages}

**Top Contributors:**
{contributors}

**Topics/Tags:**
{topics}

**Repository Structure:**
{structure}

**README Content:**
{github_data.get("readme", "No README available")[:3000]}

**Recent Commits (Sample):**
"""
        
        # Safely format commits
        for commit in github_data.get("commits", [])[:5]:
            if commit:
                message = commit.get('message', 'No message')
                author = commit.get('author', 'Unknown')
                formatted += f"\n- {message} by {author}"
        
        return formatted
    
    def _format_devpost_data(self, devpost_data: Dict) -> str:
        """Format Devpost data for Claude prompt"""
        
        # Safely format built_with
        built_with = ", ".join(str(tech) for tech in devpost_data.get("built_with", []) if tech)
        if not built_with:
            built_with = "Not specified"
        
        # Safely format team_members
        team_members = ", ".join(str(member) for member in devpost_data.get("team_members", []) if member)
        if not team_members:
            team_members = "Not specified"
        
        formatted = f"""
## Devpost Submission

**Project Title:** {devpost_data.get("title", "Unknown")}
**Tagline:** {devpost_data.get("tagline", "")}

**Built With:**
{built_with}

**Team Members:**
{team_members}

**Inspiration:**
{devpost_data.get("inspiration", "Not provided")}

**What It Does:**
{devpost_data.get("what_it_does", "Not provided")}

**How We Built It:**
{devpost_data.get("how_we_built_it", "Not provided")}

**Challenges We Ran Into:**
{devpost_data.get("challenges", "Not provided")}

**Accomplishments That We're Proud Of:**
{devpost_data.get("accomplishments", "Not provided")}

**What We Learned:**
{devpost_data.get("what_we_learned", "Not provided")}

**What's Next:**
{devpost_data.get("whats_next", "Not provided")}
"""
        
        return formatted
    
    async def generate_presentation(self, github_data: Dict, devpost_data: Dict) -> bytes:
        """
        Generate a PowerPoint presentation using Claude's PowerPoint skill
        
        Args:
            github_data: Data fetched from GitHub
            devpost_data: Data fetched from Devpost
            
        Returns:
            PPTX file content as bytes
        """
        try:
            logger.info("Generating presentation with Claude PowerPoint skill...")
            
            # Format data for Claude
            github_content = self._format_github_data(github_data)
            devpost_content = self._format_devpost_data(devpost_data)
            
            # Create comprehensive prompt for presentation generation
            project_name = devpost_data.get("title", github_data.get("name", "Hackathon Project"))
            
            prompt = f"""Create a professional, engaging PowerPoint presentation for a hackathon project pitch to judges. 

The presentation should be approximately 10-15 slides and cover the following sections:

1. **Title Slide**: Project name, tagline, and team
2. **The Problem**: What problem does this solve? What's the inspiration?
3. **The Solution**: Overview of what the project does and its key features
4. **Live Demo / Product Showcase**: Highlight key features and user experience
5. **Technical Architecture**: How it was built, tech stack, and system design
6. **Technical Implementation**: Key technical challenges solved and implementation details
7. **Impact & Use Cases**: Real-world applications and potential impact
8. **Challenges & Learning**: What challenges were faced and what was learned
9. **Accomplishments**: What the team is proud of
10. **Future Roadmap**: What's next for the project
11. **Team**: Team members and their contributions
12. **Thank You / Q&A**: Closing slide

**Project Data:**

{devpost_content}

{github_content}

**Design Guidelines:**
- Use a modern, professional design with good visual hierarchy
- Include relevant icons and visual elements where appropriate
- Use bullet points effectively (3-5 points per slide)
- Keep text concise and impactful
- Add speaker notes with talking points for each slide
- Use consistent color scheme throughout
- Make it visually engaging for judges

Create this presentation now."""
            
            # Ask Claude to structure the presentation content
            structure_prompt = prompt + """

Please analyze all the project data and create a structured outline for the presentation.
Return ONLY a JSON object (no other text) with this exact structure:

{
  "title": "Project Title",
  "tagline": "Brief tagline",
  "slides": [
    {
      "title": "Slide Title",
      "content": ["Bullet point 1", "Bullet point 2", "Bullet point 3"],
      "notes": "Speaker notes for this slide"
    }
  ]
}

Make sure to include 10-15 slides covering all the sections mentioned above."""

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": structure_prompt
                }]
            )
            
            logger.info(f"Claude response received with {len(response.content)} content blocks")
            
            # Extract JSON content from Claude's response
            presentation_structure = None
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    text = content_block.text
                    logger.info(f"Received text response ({len(text)} chars)")
                    
                    # Try to extract JSON from the response
                    try:
                        # Look for JSON in the text
                        json_start = text.find('{')
                        json_end = text.rfind('}') + 1
                        if json_start >= 0 and json_end > json_start:
                            json_str = text[json_start:json_end]
                            presentation_structure = json.loads(json_str)
                            logger.info("Successfully parsed presentation structure from Claude")
                            break
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse JSON from response: {e}")
                        # Try the whole text
                        try:
                            presentation_structure = json.loads(text)
                            break
                        except:
                            pass
            
            if not presentation_structure:
                logger.error("Could not extract presentation structure from Claude's response")
                raise ValueError("Failed to get presentation structure from Claude")
            
            # Create PowerPoint presentation using python-pptx
            logger.info("Creating PowerPoint presentation...")
            pptx_data = self._create_powerpoint(presentation_structure)
            
            logger.info(f"Successfully generated presentation ({len(pptx_data)} bytes)")
            return pptx_data
        
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise ValueError(f"Claude API error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating presentation: {str(e)}")
            raise ValueError(f"Failed to generate presentation: {str(e)}")
    
    def _create_powerpoint(self, structure: Dict) -> bytes:
        """
        Create a PowerPoint presentation from structured data
        
        Args:
            structure: Dictionary with title, tagline, and slides
            
        Returns:
            PPTX file content as bytes
        """
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        # Title slide
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = structure.get("title", "Hackathon Project")
        subtitle.text = structure.get("tagline", "")
        
        # Content slides
        for slide_data in structure.get("slides", []):
            bullet_slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(bullet_slide_layout)
            
            # Set title
            title = slide.shapes.title
            title.text = slide_data.get("title", "")
            
            # Add content
            content_placeholder = slide.placeholders[1]
            text_frame = content_placeholder.text_frame
            text_frame.clear()
            
            for i, bullet in enumerate(slide_data.get("content", [])):
                if i == 0:
                    p = text_frame.paragraphs[0]
                else:
                    p = text_frame.add_paragraph()
                p.text = bullet
                p.level = 0
                
                # Format text
                for run in p.runs:
                    run.font.size = Pt(18)
            
            # Add speaker notes
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = slide_data.get("notes", "")
        
        # Save to bytes
        pptx_io = io.BytesIO()
        prs.save(pptx_io)
        pptx_io.seek(0)
        
        return pptx_io.read()
