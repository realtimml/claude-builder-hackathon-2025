import os
from anthropic import Anthropic
from typing import Dict, List
import json

class ClaudeService:
    """Service for generating presentation content using Claude API"""
    
    def __init__(self):
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise ValueError("CLAUDE_API_KEY environment variable is required")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def _create_prompt(self, github_data: Dict, devpost_data: Dict) -> str:
        """
        Create a comprehensive prompt for Claude to generate presentation content
        
        Args:
            github_data: Data from GitHub repository
            devpost_data: Data from Devpost submission
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a presentation expert helping to create a compelling hackathon project presentation. 
Based on the GitHub repository data and Devpost submission below, generate structured content for a professional presentation.

# GitHub Repository Data:
- Project Name: {github_data.get('name', 'N/A')}
- Description: {github_data.get('description', 'N/A')}
- Primary Language: {github_data.get('primary_language', 'N/A')}
- Tech Stack: {', '.join(github_data.get('languages', {}).keys())}
- Stars: {github_data.get('stars', 0)}
- Contributors: {len(github_data.get('contributors', []))}
- Has Documentation: {github_data.get('structure', {}).get('has_docs', False)}
- Has Tests: {github_data.get('structure', {}).get('has_tests', False)}
- Dependencies: {json.dumps(list(github_data.get('dependencies', {}).keys()))}

README Summary:
{github_data.get('readme', 'No README available')[:2000]}

# Devpost Submission Data:
- Title: {devpost_data.get('title', 'N/A')}
- Tagline: {devpost_data.get('tagline', 'N/A')}
- Inspiration: {devpost_data.get('inspiration', 'N/A')}
- What it does: {devpost_data.get('what_it_does', 'N/A')}
- How we built it: {devpost_data.get('how_we_built_it', 'N/A')}
- Challenges: {devpost_data.get('challenges', 'N/A')}
- Accomplishments: {devpost_data.get('accomplishments', 'N/A')}
- What we learned: {devpost_data.get('what_we_learned', 'N/A')}
- What's next: {devpost_data.get('whats_next', 'N/A')}
- Tech Stack from Devpost: {', '.join(devpost_data.get('tech_stack', []))}
- Team Members: {', '.join([m.get('name', '') for m in devpost_data.get('team_members', [])])}

# Instructions:
Generate a structured presentation with the following slides. For each slide, provide:
1. A compelling title
2. 3-5 bullet points or key messages
3. Optional speaker notes for presenting

The presentation should tell a compelling story following this structure:

**Slide 1: Title Slide**
- Project title and tagline
- Team member names
- A hook that captures attention

**Slides 2-3: Problem & Motivation**
- What problem does this solve?
- Why is it important?
- Who does it help?
- Real-world context

**Slides 4-5: Solution Overview**
- What is the solution?
- Key features and capabilities
- How does it work (high-level)?
- Unique value proposition

**Slides 6-7: Technical Deep Dive**
- Architecture overview
- Technology stack and why these choices
- Key technical innovations
- Integration points

**Slides 8-9: Demo & Features**
- Core functionality showcase
- User journey/workflow
- Key features with examples
- Screenshots or demo plan

**Slide 10: Impact & Use Cases**
- Who can benefit from this?
- Real-world applications
- Potential impact and scalability
- Success metrics or vision

**Slide 11: Challenges & Learning**
- Key technical challenges overcome
- What the team learned
- Growth and development
- Future improvements and roadmap

Return the response as a valid JSON object with this structure:
{{
  "presentation_title": "string",
  "team_members": ["string"],
  "slides": [
    {{
      "slide_number": 1,
      "title": "string",
      "content": ["bullet point 1", "bullet point 2", ...],
      "speaker_notes": "string"
    }}
  ]
}}

Make the content engaging, concise, and tailored for a hackathon judge audience. Focus on innovation, technical excellence, and real-world impact.
"""
        return prompt
    
    async def generate_presentation_content(
        self, 
        github_data: Dict, 
        devpost_data: Dict
    ) -> Dict:
        """
        Generate structured presentation content using Claude
        
        Args:
            github_data: Data from GitHub repository
            devpost_data: Data from Devpost submission
            
        Returns:
            Structured presentation content as dictionary
        """
        try:
            # Create prompt
            prompt = self._create_prompt(github_data, devpost_data)
            
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Parse JSON response
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            presentation_content = json.loads(response_text)
            
            # Add metadata
            presentation_content['github_url'] = github_data.get('url', '')
            presentation_content['devpost_url'] = devpost_data.get('url', '')
            presentation_content['generated_by'] = 'Claude API'
            
            return presentation_content
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse Claude response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating presentation content: {str(e)}")

