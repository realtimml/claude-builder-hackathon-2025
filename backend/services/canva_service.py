import os
import httpx
from typing import Dict, List, Optional
import json
import base64

class CanvaService:
    """Service for creating presentations using Canva Connect API"""
    
    def __init__(self):
        self.client_id = os.getenv("CANVA_CLIENT_ID")
        self.client_secret = os.getenv("CANVA_CLIENT_SECRET")
        self.redirect_uri = os.getenv("CANVA_REDIRECT_URI", "http://localhost:8000/api/canva/callback")
        
        if not self.client_id or not self.client_secret:
            raise ValueError("CANVA_CLIENT_ID and CANVA_CLIENT_SECRET environment variables are required")
        
        self.base_url = "https://api.canva.com/rest/v1"
        self.access_token = None
    
    async def _get_access_token(self) -> str:
        """
        Get access token using client credentials flow
        
        Returns:
            Access token string
        """
        if self.access_token:
            return self.access_token
        
        # Prepare credentials for Basic Auth
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.canva.com/rest/v1/oauth/token",
                headers={
                    "Authorization": f"Basic {encoded_credentials}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "client_credentials",
                    "scope": "design:content:write design:meta:read"
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get Canva access token: {response.text}")
            
            data = response.json()
            self.access_token = data.get("access_token")
            return self.access_token
    
    async def _create_design(self, title: str) -> str:
        """
        Create a new Canva design/presentation
        
        Args:
            title: Title for the presentation
            
        Returns:
            Design ID
        """
        token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/designs",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "design_type": "Presentation",
                    "title": title
                }
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to create Canva design: {response.text}")
            
            data = response.json()
            return data.get("design", {}).get("id")
    
    async def _add_page(self, design_id: str) -> str:
        """
        Add a new page/slide to the design
        
        Args:
            design_id: ID of the design
            
        Returns:
            Page ID
        """
        token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/designs/{design_id}/pages",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={}
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to add page to Canva design: {response.text}")
            
            data = response.json()
            return data.get("page", {}).get("id")
    
    async def _add_text_to_page(self, design_id: str, page_id: str, text: str, position: Dict) -> None:
        """
        Add text element to a page
        
        Args:
            design_id: ID of the design
            page_id: ID of the page
            text: Text content to add
            position: Position and styling info
        """
        token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/designs/{design_id}/pages/{page_id}/elements",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "type": "text",
                    "text": text,
                    "font_size": position.get("font_size", 24),
                    "top": position.get("top", 100),
                    "left": position.get("left", 100),
                    "width": position.get("width", 800),
                    "height": position.get("height", 100)
                }
            )
            
            if response.status_code not in [200, 201]:
                print(f"Warning: Failed to add text to Canva page: {response.text}")
    
    async def _get_design_url(self, design_id: str) -> str:
        """
        Get the edit URL for the design
        
        Args:
            design_id: ID of the design
            
        Returns:
            Canva edit URL
        """
        token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/designs/{design_id}",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
            
            if response.status_code != 200:
                # If we can't get the URL from API, construct it manually
                return f"https://www.canva.com/design/{design_id}/edit"
            
            data = response.json()
            return data.get("design", {}).get("urls", {}).get("edit_url", f"https://www.canva.com/design/{design_id}/edit")
    
    async def create_presentation(self, presentation_data: Dict) -> str:
        """
        Create a complete presentation in Canva
        
        Args:
            presentation_data: Structured presentation data from Claude
            
        Returns:
            URL to edit the presentation in Canva
        """
        try:
            # For MVP, we'll create a simple text-based approach
            # In production, you'd use Canva's autofill API with templates
            
            title = presentation_data.get("presentation_title", "Hackathon Presentation")
            slides = presentation_data.get("slides", [])
            
            # Create the design
            print(f"Creating Canva design: {title}")
            design_id = await self._create_design(title)
            
            # Add slides
            for i, slide in enumerate(slides):
                print(f"Adding slide {i+1}/{len(slides)}: {slide.get('title', 'Untitled')}")
                
                if i > 0:  # First page is created automatically
                    page_id = await self._add_page(design_id)
                else:
                    # Use first page
                    page_id = None  # Will need to get first page ID
                
                # Add slide title
                slide_title = slide.get("title", "")
                if slide_title and page_id:
                    await self._add_text_to_page(
                        design_id, page_id, slide_title,
                        {"font_size": 48, "top": 50, "left": 50, "width": 900, "height": 100}
                    )
                
                # Add bullet points
                content = slide.get("content", [])
                if content and page_id:
                    bullets_text = "\n".join([f"• {point}" for point in content])
                    await self._add_text_to_page(
                        design_id, page_id, bullets_text,
                        {"font_size": 24, "top": 200, "left": 50, "width": 900, "height": 400}
                    )
            
            # Get the edit URL
            edit_url = await self._get_design_url(design_id)
            
            print(f"Canva presentation created: {edit_url}")
            return edit_url
            
        except Exception as e:
            # If Canva API fails, return a placeholder message
            print(f"Error creating Canva presentation: {str(e)}")
            # Return presentation data as JSON for manual creation
            raise Exception(f"Unable to create Canva presentation automatically. Error: {str(e)}. Please use the presentation data provided to create manually.")

