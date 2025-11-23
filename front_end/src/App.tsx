import { useState, FormEvent } from 'react'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [githubUrl, setGithubUrl] = useState('')
  const [devpostUrl, setDevpostUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [statusMessage, setStatusMessage] = useState('')

  const validateUrl = (url: string, type: 'github' | 'devpost'): boolean => {
    if (!url) return false
    
    if (type === 'github') {
      return url.includes('github.com') && url.includes('/')
    } else {
      return url.includes('devpost.com')
    }
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setStatusMessage('')

    // Validate URLs
    if (!validateUrl(githubUrl, 'github')) {
      setError('Please enter a valid GitHub repository URL')
      return
    }

    if (!validateUrl(devpostUrl, 'devpost')) {
      setError('Please enter a valid Devpost project URL')
      return
    }

    setLoading(true)
    setStatusMessage('Fetching repository data...')

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-presentation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          github_url: githubUrl,
          devpost_url: devpostUrl,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate presentation')
      }

      setStatusMessage('Generating presentation with AI...')

      // Get the filename from Content-Disposition header
      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = 'presentation.pptx'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }

      // Download the file
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)

      setStatusMessage('✓ Presentation generated successfully!')
      
      // Reset form after a delay
      setTimeout(() => {
        setGithubUrl('')
        setDevpostUrl('')
        setStatusMessage('')
      }, 3000)

    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred')
      setStatusMessage('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>🎯 Hackathon Presentation Generator</h1>
        <p className="subtitle">
          Transform your GitHub repo and Devpost submission into a professional presentation with AI
        </p>
      </header>

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="github-url">
            GitHub Repository URL
          </label>
          <input
            id="github-url"
            type="text"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            disabled={loading}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="devpost-url">
            Devpost Project URL
          </label>
          <input
            id="devpost-url"
            type="text"
            value={devpostUrl}
            onChange={(e) => setDevpostUrl(e.target.value)}
            placeholder="https://devpost.com/software/your-project"
            disabled={loading}
            required
          />
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {statusMessage && (
          <div className="status-message">
            {statusMessage}
          </div>
        )}

        <button 
          type="submit" 
          className="submit-button"
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Generating...
            </>
          ) : (
            'Generate Presentation'
          )}
        </button>
      </form>

      <footer>
        <p className="info-text">
          Powered by Claude AI • Analyzes your code, commits, and project details to create judge-ready slides
        </p>
      </footer>
    </div>
  )
}

export default App
