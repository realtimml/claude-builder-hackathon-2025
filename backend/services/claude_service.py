import anthropic
from typing import Dict
import logging
import base64

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
        languages = ", ".join(github_data.get("languages", {}).keys())
        contributors = ", ".join([c["name"] for c in github_data.get("contributors", [])[:5]])
        
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
{", ".join(github_data.get("topics", []))}

**Repository Structure:**
{", ".join(github_data.get("structure", [])[:20])}

**README Content:**
{github_data.get("readme", "No README available")[:3000]}

**Recent Commits (Sample):**
"""
        
        for commit in github_data.get("commits", [])[:5]:
            formatted += f"\n- {commit.get('message', '')} by {commit.get('author', 'Unknown')}"
        
        return formatted
    
    def _format_devpost_data(self, devpost_data: Dict) -> str:
        """Format Devpost data for Claude prompt"""
        
        formatted = f"""
## Devpost Submission

**Project Title:** {devpost_data.get("title", "Unknown")}
**Tagline:** {devpost_data.get("tagline", "")}

**Built With:**
{", ".join(devpost_data.get("built_with", []))}

**Team Members:**
{", ".join(devpost_data.get("team_members", ["Not specified"]))}

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
            
            # Call Claude with PowerPoint skill
            response = self.client.beta.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                betas=["skills-2025-10-02"],
                container={
                    "skills": [
                        {
                            "type": "anthropic",
                            "skill_id": "pptx",
                            "version": "latest"
                        }
                    ]
                },
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            logger.info(f"Claude response received with {len(response.content)} content blocks")
            
            # Extract the PowerPoint file from the response
            pptx_data = None
            
            for content_block in response.content:
                logger.info(f"Content block type: {content_block.type}")
                
                # Check if this is a tool use block with file output
                if hasattr(content_block, 'type') and content_block.type == 'tool_use':
                    logger.info(f"Tool use block found: {content_block.name}")
                    
                    # Check if there are any files in the output
                    if hasattr(content_block, 'output') and content_block.output:
                        output = content_block.output
                        logger.info(f"Tool output type: {type(output)}")
                        
                        # Handle different output formats
                        if isinstance(output, dict):
                            # Check for files in output
                            if 'files' in output and output['files']:
                                for file_info in output['files']:
                                    if file_info.get('name', '').endswith('.pptx'):
                                        # File content might be base64 encoded
                                        if 'content' in file_info:
                                            pptx_data = base64.b64decode(file_info['content'])
                                            logger.info("Found PPTX file in tool output")
                                            break
                        elif isinstance(output, str):
                            # Try to decode if it's base64
                            try:
                                pptx_data = base64.b64decode(output)
                                logger.info("Decoded PPTX from base64 string")
                            except:
                                pass
            
            # If we didn't find the file in tool_use blocks, check for file downloads via beta files API
            if not pptx_data:
                logger.info("Attempting to retrieve file via Files API...")
                
                # Check response for any file references
                for content_block in response.content:
                    if hasattr(content_block, 'type') and content_block.type == 'tool_use':
                        if hasattr(content_block, 'output'):
                            output = content_block.output
                            
                            # Look for file ID or reference
                            if isinstance(output, dict) and 'file_id' in output:
                                file_id = output['file_id']
                                logger.info(f"Found file ID: {file_id}")
                                
                                # Download file using Files API
                                file_content = self.client.beta.files.content(file_id)
                                pptx_data = file_content.read()
                                logger.info("Downloaded PPTX file via Files API")
                                break
            
            if not pptx_data:
                # Log the response for debugging
                logger.error("Could not find PPTX file in response")
                logger.error(f"Response content blocks: {[str(block) for block in response.content]}")
                raise ValueError("Failed to extract PowerPoint file from Claude's response. The PowerPoint skill may not have generated a file.")
            
            logger.info(f"Successfully generated presentation ({len(pptx_data)} bytes)")
            return pptx_data
        
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise ValueError(f"Claude API error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating presentation: {str(e)}")
            raise ValueError(f"Failed to generate presentation: {str(e)}")
