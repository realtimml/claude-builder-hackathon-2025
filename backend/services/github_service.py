import os
from github import Github, GithubException
from typing import Dict, Optional, List
import base64

class GitHubService:
    """Service for interacting with GitHub API to fetch repository data"""
    
    def __init__(self):
        github_token = os.getenv("GITHUB_TOKEN")
        self.github = Github(github_token) if github_token else Github()
        
    def _parse_github_url(self, url: str) -> tuple[str, str]:
        """
        Parse GitHub URL to extract owner and repo name
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo_name)
        """
        # Remove trailing slash if present
        url = url.rstrip('/')
        
        # Handle various GitHub URL formats
        if 'github.com/' in url:
            parts = url.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                owner = parts[0]
                repo_name = parts[1]
                return owner, repo_name
        
        raise ValueError(f"Invalid GitHub URL format: {url}")
    
    def _get_readme_content(self, repo) -> Optional[str]:
        """
        Fetch README content from various possible locations
        
        Args:
            repo: PyGithub Repository object
            
        Returns:
            README content as string or None if not found
        """
        readme_paths = ['README.md', 'README.MD', 'readme.md', 'README', 
                       'docs/README.md', '.github/README.md']
        
        for path in readme_paths:
            try:
                content_file = repo.get_contents(path)
                if isinstance(content_file, list):
                    continue
                content = base64.b64decode(content_file.content).decode('utf-8')
                return content
            except:
                continue
        
        return None
    
    def _extract_dependencies(self, repo) -> Dict[str, List[str]]:
        """
        Extract dependencies from various dependency files
        
        Args:
            repo: PyGithub Repository object
            
        Returns:
            Dictionary of dependency types and their contents
        """
        dependencies = {}
        dependency_files = {
            'package.json': 'npm',
            'requirements.txt': 'pip',
            'Pipfile': 'pipenv',
            'pyproject.toml': 'poetry',
            'go.mod': 'go',
            'Cargo.toml': 'rust',
            'composer.json': 'composer',
            'Gemfile': 'bundler'
        }
        
        for filename, dep_type in dependency_files.items():
            try:
                content_file = repo.get_contents(filename)
                if isinstance(content_file, list):
                    continue
                content = base64.b64decode(content_file.content).decode('utf-8')
                dependencies[dep_type] = content
            except:
                continue
        
        return dependencies
    
    def _get_language_breakdown(self, repo) -> Dict[str, int]:
        """Get programming language statistics"""
        try:
            return repo.get_languages()
        except:
            return {}
    
    def _get_top_contributors(self, repo, limit: int = 5) -> List[Dict[str, str]]:
        """Get top contributors to the repository"""
        try:
            contributors = []
            for contributor in repo.get_contributors()[:limit]:
                contributors.append({
                    'login': contributor.login,
                    'name': contributor.name or contributor.login,
                    'avatar_url': contributor.avatar_url,
                    'contributions': contributor.contributions
                })
            return contributors
        except:
            return []
    
    def _analyze_repo_structure(self, repo) -> Dict[str, any]:
        """Analyze repository structure and key files"""
        structure = {
            'has_docs': False,
            'has_tests': False,
            'has_ci_cd': False,
            'key_directories': []
        }
        
        try:
            contents = repo.get_contents("")
            for content in contents:
                if content.type == "dir":
                    dir_name = content.name.lower()
                    structure['key_directories'].append(content.name)
                    
                    if dir_name in ['docs', 'documentation', 'doc']:
                        structure['has_docs'] = True
                    if dir_name in ['test', 'tests', '__tests__', 'spec']:
                        structure['has_tests'] = True
                    if dir_name in ['.github', '.gitlab', '.circleci']:
                        structure['has_ci_cd'] = True
        except:
            pass
        
        return structure
    
    async def fetch_repo_data(self, github_url: str) -> Dict[str, any]:
        """
        Fetch comprehensive repository data from GitHub
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Dictionary containing all repository information
        """
        try:
            # Parse URL
            owner, repo_name = self._parse_github_url(github_url)
            
            # Get repository
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Fetch all data
            readme_content = self._get_readme_content(repo)
            dependencies = self._extract_dependencies(repo)
            languages = self._get_language_breakdown(repo)
            contributors = self._get_top_contributors(repo)
            structure = self._analyze_repo_structure(repo)
            
            # Get commit statistics
            try:
                commit_count = repo.get_commits().totalCount
                latest_commit = repo.get_commits()[0]
                latest_commit_date = latest_commit.commit.author.date.isoformat()
            except:
                commit_count = 0
                latest_commit_date = None
            
            # Compile data
            repo_data = {
                'name': repo.name,
                'full_name': repo.full_name,
                'owner': owner,
                'description': repo.description or '',
                'url': github_url,
                'homepage': repo.homepage or '',
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'watchers': repo.watchers_count,
                'open_issues': repo.open_issues_count,
                'created_at': repo.created_at.isoformat(),
                'updated_at': repo.updated_at.isoformat(),
                'latest_commit_date': latest_commit_date,
                'commit_count': commit_count,
                'default_branch': repo.default_branch,
                'license': repo.license.name if repo.license else None,
                'topics': repo.get_topics(),
                'readme': readme_content,
                'languages': languages,
                'primary_language': repo.language,
                'dependencies': dependencies,
                'contributors': contributors,
                'structure': structure
            }
            
            return repo_data
            
        except GithubException as e:
            raise Exception(f"GitHub API error: {e.data.get('message', str(e))}")
        except ValueError as e:
            raise Exception(f"Invalid URL: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching GitHub data: {str(e)}")

