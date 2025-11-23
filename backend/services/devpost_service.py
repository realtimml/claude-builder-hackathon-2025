import requests
from bs4 import BeautifulSoup
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class DevpostService:
    """Service for scraping data from Devpost project pages"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def fetch_project_data(self, devpost_url: str) -> Dict:
        """
        Scrape project data from Devpost
        
        Args:
            devpost_url: Devpost project URL
            
        Returns:
            Dictionary containing project data
        """
        try:
            logger.info(f"Fetching Devpost data from {devpost_url}")
            
            response = requests.get(devpost_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ""
            title_elem = soup.find('h1', {'id': 'software-title'})
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            # Extract tagline
            tagline = ""
            tagline_elem = soup.find('p', {'id': 'software-tagline'})
            if tagline_elem:
                tagline = tagline_elem.get_text(strip=True)
            
            # Extract built with (tech stack)
            built_with = []
            built_with_section = soup.find('div', {'id': 'built-with'})
            if built_with_section:
                tags = built_with_section.find_all('span', class_='cp-tag')
                built_with = [tag.get_text(strip=True) for tag in tags]
            
            # Extract main sections
            sections = {}
            
            # Look for the details section
            details_div = soup.find('div', {'id': 'app-details-left'})
            if details_div:
                # Find all section headers and their content
                headers = details_div.find_all(['h2', 'h3'])
                for header in headers:
                    section_title = header.get_text(strip=True).lower()
                    
                    # Get the content after this header
                    content = []
                    for sibling in header.find_next_siblings():
                        if sibling.name in ['h2', 'h3']:
                            break
                        if sibling.name == 'p':
                            text = sibling.get_text(strip=True)
                            if text:
                                content.append(text)
                    
                    if content:
                        sections[section_title] = ' '.join(content)
            
            # Try alternative structure for sections
            if not sections:
                section_divs = soup.find_all('div', class_='software-section')
                for div in section_divs:
                    header = div.find(['h2', 'h3'])
                    if header:
                        section_title = header.get_text(strip=True).lower()
                        paragraphs = div.find_all('p')
                        content = ' '.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                        if content:
                            sections[section_title] = content
            
            # Map common section names
            inspiration = sections.get('inspiration', '')
            what_it_does = sections.get('what it does', '')
            how_we_built_it = sections.get('how we built it', sections.get('how i built it', ''))
            challenges = sections.get('challenges we ran into', sections.get('challenges i ran into', ''))
            accomplishments = sections.get('accomplishments that we\'re proud of', sections.get('accomplishments that i\'m proud of', ''))
            what_we_learned = sections.get('what we learned', sections.get('what i learned', ''))
            whats_next = sections.get('what\'s next for ' + title.lower(), sections.get('what\'s next', ''))
            
            # Extract team members
            team_members = []
            team_section = soup.find('div', {'id': 'software-team'})
            if team_section:
                members = team_section.find_all('a', class_='software-team-member')
                team_members = [member.get_text(strip=True) for member in members]
            
            # Extract gallery/media info
            has_video = bool(soup.find('div', class_='software-video'))
            gallery_images = soup.find_all('img', class_='software-image')
            num_images = len(gallery_images)
            
            return {
                "title": title,
                "tagline": tagline,
                "url": devpost_url,
                "built_with": built_with,
                "inspiration": inspiration,
                "what_it_does": what_it_does,
                "how_we_built_it": how_we_built_it,
                "challenges": challenges,
                "accomplishments": accomplishments,
                "what_we_learned": what_we_learned,
                "whats_next": whats_next,
                "team_members": team_members,
                "has_video": has_video,
                "num_images": num_images,
                "all_sections": sections,  # Include all sections for flexibility
            }
        
        except requests.RequestException as e:
            raise ValueError(f"Error fetching Devpost page: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing Devpost data: {str(e)}")
