from github import Github, GithubException
from typing import Dict, Optional, List
import re
import logging

logger = logging.getLogger(__name__)


class GitHubService:
    """Service for fetching comprehensive data from GitHub repositories"""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub service
        
        Args:
            github_token: Optional GitHub personal access token for higher rate limits
        """
        self.github = Github(github_token) if github_token else Github()
    
    def _parse_github_url(self, url: str) -> tuple[str, str]:
        """
        Parse GitHub URL to extract owner and repo name
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo_name)
        """
        # Handle various GitHub URL formats
        patterns = [
            r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
            r'github\.com/([^/]+)/([^/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                # Remove .git suffix if present
                repo = repo.replace('.git', '')
                return owner, repo
        
        raise ValueError(f"Invalid GitHub URL format: {url}")
    
    async def fetch_repo_data(self, github_url: str) -> Dict:
        """
        Fetch comprehensive repository data
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Dictionary containing all repository data
        """
        try:
            owner, repo_name = self._parse_github_url(github_url)
            logger.info(f"Fetching data for {owner}/{repo_name}")
            
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Fetch README
            readme_content = ""
            try:
                readme = repo.get_readme()
                readme_content = readme.decoded_content.decode('utf-8')
            except Exception as e:
                logger.warning(f"Could not fetch README: {str(e)}")
            
            # Fetch repository statistics
            stats = {
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.watchers_count,
                "open_issues": repo.open_issues_count,
                "size_kb": repo.size,
            }
            
            # Fetch languages/tech stack
            languages = repo.get_languages()
            
            # Fetch recent commits (last 20)
            commits_data = []
            try:
                commits = repo.get_commits()[:20]
                for commit in commits:
                    commits_data.append({
                        "message": commit.commit.message,
                        "author": commit.commit.author.name if commit.commit.author else "Unknown",
                        "date": commit.commit.author.date.isoformat() if commit.commit.author else None,
                    })
            except Exception as e:
                logger.warning(f"Could not fetch commits: {str(e)}")
            
            # Fetch contributors
            contributors_data = []
            try:
                contributors = repo.get_contributors()[:10]  # Top 10 contributors
                for contributor in contributors:
                    contributors_data.append({
                        "username": contributor.login,
                        "contributions": contributor.contributions,
                        "name": contributor.name if hasattr(contributor, 'name') else contributor.login,
                    })
            except Exception as e:
                logger.warning(f"Could not fetch contributors: {str(e)}")
            
            # Get repository structure (top-level files and directories)
            structure = []
            try:
                contents = repo.get_contents("")
                structure = [item.path for item in contents]
            except Exception as e:
                logger.warning(f"Could not fetch repository structure: {str(e)}")
            
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description or "",
                "url": repo.html_url,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
                "readme": readme_content,
                "statistics": stats,
                "languages": languages,
                "commits": commits_data,
                "contributors": contributors_data,
                "structure": structure,
                "topics": repo.get_topics(),
                "homepage": repo.homepage or "",
                "license": repo.license.name if repo.license else None,
            }
        
        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"Repository not found or is private: {github_url}")
            elif e.status == 403:
                raise ValueError("GitHub API rate limit exceeded. Please provide a GitHub token.")
            else:
                raise ValueError(f"GitHub API error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error fetching GitHub data: {str(e)}")
