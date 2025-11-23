import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re

class DevpostService:
    """Service for scraping Devpost project pages"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_section(self, soup: BeautifulSoup, heading_text: str) -> Optional[str]:
        """
        Extract content from a section based on its heading
        
        Args:
            soup: BeautifulSoup object
            heading_text: Text of the heading to search for
            
        Returns:
            Section content as string or None if not found
        """
        # Try to find the heading
        headings = soup.find_all(['h2', 'h3', 'h4'])
        for heading in headings:
            if heading_text.lower() in heading.get_text().lower():
                # Get content after heading
                content_parts = []
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['h2', 'h3', 'h4']:
                        break
                    text = self._clean_text(sibling.get_text())
                    if text:
                        content_parts.append(text)
                
                if content_parts:
                    return ' '.join(content_parts)
        
        return None
    
    def _extract_team_members(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract team member information"""
        team_members = []
        
        # Try to find team member section
        team_section = soup.find('div', class_=re.compile(r'software-team|team-members'))
        if not team_section:
            # Try alternative selectors
            team_section = soup.find('section', id=re.compile(r'team|built-with'))
        
        if team_section:
            member_elements = team_section.find_all('a', class_=re.compile(r'user-profile|software-team-member'))
            for member in member_elements:
                name_elem = member.find(['h5', 'h6', 'span'])
                if name_elem:
                    team_members.append({
                        'name': self._clean_text(name_elem.get_text()),
                        'profile_url': member.get('href', '')
                    })
        
        return team_members
    
    def _extract_tech_stack(self, soup: BeautifulSoup) -> List[str]:
        """Extract technologies/tools used"""
        tech_stack = []
        
        # Look for "Built With" section
        built_with_section = soup.find('div', id='built-with')
        if not built_with_section:
            built_with_section = soup.find('div', class_=re.compile(r'built-with'))
        
        if built_with_section:
            tech_tags = built_with_section.find_all('span', class_=re.compile(r'cp-tag'))
            if not tech_tags:
                tech_tags = built_with_section.find_all(['a', 'span'])
            
            for tag in tech_tags:
                tech_name = self._clean_text(tag.get_text())
                if tech_name and len(tech_name) > 1:
                    tech_stack.append(tech_name)
        
        return tech_stack
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract project images and screenshots"""
        images = []
        
        # Find gallery or image sections
        gallery = soup.find('div', class_=re.compile(r'gallery|screenshots'))
        if gallery:
            img_tags = gallery.find_all('img')
            for img in img_tags:
                src = img.get('src') or img.get('data-src')
                if src and 'http' in src:
                    images.append(src)
        
        # Also check for main project image
        main_img = soup.find('img', class_=re.compile(r'software-image'))
        if main_img:
            src = main_img.get('src') or main_img.get('data-src')
            if src and 'http' in src and src not in images:
                images.insert(0, src)
        
        return images[:5]  # Limit to 5 images
    
    async def scrape_devpost(self, devpost_url: str) -> Dict[str, any]:
        """
        Scrape Devpost project page for information
        
        Args:
            devpost_url: URL to Devpost project page
            
        Returns:
            Dictionary containing all extracted information
        """
        try:
            # Fetch the page
            response = requests.get(devpost_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract project title
            title_elem = soup.find('h1', id='software-title')
            if not title_elem:
                title_elem = soup.find('h1')
            title = self._clean_text(title_elem.get_text()) if title_elem else "Untitled Project"
            
            # Extract tagline
            tagline_elem = soup.find('p', id='software-tagline')
            if not tagline_elem:
                tagline_elem = soup.find('p', class_=re.compile(r'tagline'))
            tagline = self._clean_text(tagline_elem.get_text()) if tagline_elem else ""
            
            # Extract main description/about section
            description = ""
            desc_section = soup.find('div', id='app-details-left')
            if desc_section:
                paragraphs = desc_section.find_all('p')
                description = ' '.join([self._clean_text(p.get_text()) for p in paragraphs[:3]])
            
            # Extract structured sections
            inspiration = self._extract_section(soup, "Inspiration")
            what_it_does = self._extract_section(soup, "What it does")
            how_we_built = self._extract_section(soup, "How we built it") or self._extract_section(soup, "How I built it")
            challenges = self._extract_section(soup, "Challenges") or self._extract_section(soup, "Challenges we ran into")
            accomplishments = self._extract_section(soup, "Accomplishments") or self._extract_section(soup, "proud of")
            what_we_learned = self._extract_section(soup, "What we learned") or self._extract_section(soup, "What I learned")
            whats_next = self._extract_section(soup, "What's next") or self._extract_section(soup, "future")
            
            # Extract team members
            team_members = self._extract_team_members(soup)
            
            # Extract tech stack
            tech_stack = self._extract_tech_stack(soup)
            
            # Extract images
            images = self._extract_images(soup)
            
            # Compile all data
            devpost_data = {
                'url': devpost_url,
                'title': title,
                'tagline': tagline,
                'description': description or what_it_does or inspiration or "",
                'inspiration': inspiration,
                'what_it_does': what_it_does,
                'how_we_built_it': how_we_built,
                'challenges': challenges,
                'accomplishments': accomplishments,
                'what_we_learned': what_we_learned,
                'whats_next': whats_next,
                'team_members': team_members,
                'tech_stack': tech_stack,
                'images': images
            }
            
            return devpost_data
            
        except requests.RequestException as e:
            raise Exception(f"Error fetching Devpost page: {str(e)}")
        except Exception as e:
            raise Exception(f"Error parsing Devpost data: {str(e)}")

