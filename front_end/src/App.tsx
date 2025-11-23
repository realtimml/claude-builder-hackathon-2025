import { useState } from 'react'
import './App.css'

interface PresentationResponse {
  success: boolean
  canva_url?: string
  message: string
  presentation_data?: any
}

type LoadingStage = 'idle' | 'fetching' | 'analyzing' | 'creating' | 'success' | 'error'

function App() {
  const [githubUrl, setGithubUrl] = useState('')
  const [devpostUrl, setDevpostUrl] = useState('')
  const [loadingStage, setLoadingStage] = useState<LoadingStage>('idle')
  const [result, setResult] = useState<PresentationResponse | null>(null)
  const [error, setError] = useState<string>('')

  const validateUrls = (): boolean => {
    if (!githubUrl || !devpostUrl) {
      setError('Please provide both GitHub and Devpost URLs')
      return false
    }

    if (!githubUrl.includes('github.com')) {
      setError('Please provide a valid GitHub URL')
      return false
    }

    if (!devpostUrl.includes('devpost.com')) {
      setError('Please provide a valid Devpost URL')
      return false
    }

    return true
  }

  const handleGenerate = async () => {
    setError('')
    setResult(null)

    if (!validateUrls()) {
      return
    }

    try {
      setLoadingStage('fetching')
      
      // Simulate stage progression for demo
      setTimeout(() => setLoadingStage('analyzing'), 2000)
      setTimeout(() => setLoadingStage('creating'), 4000)

      const response = await fetch('http://localhost:8000/api/generate-presentation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          github_url: githubUrl,
          devpost_url: devpostUrl,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate presentation')
      }

      setResult(data)
      setLoadingStage('success')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setLoadingStage('error')
    }
  }

  const getLoadingMessage = () => {
    switch (loadingStage) {
      case 'fetching':
        return 'Fetching data from GitHub and Devpost...'
      case 'analyzing':
        return 'Analyzing project with Claude AI...'
      case 'creating':
        return 'Creating presentation in Canva...'
      default:
        return ''
    }
  }

  const handleReset = () => {
    setLoadingStage('idle')
    setResult(null)
    setError('')
    setGithubUrl('')
    setDevpostUrl('')
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">🎯 Hackathon Presentation Generator</h1>
          <p className="subtitle">
            Transform your GitHub repo and Devpost submission into a stunning presentation
          </p>
        </header>

        {loadingStage === 'idle' && (
          <div className="form-container">
            <div className="input-group">
              <label htmlFor="github-url">GitHub Repository URL</label>
              <input
                id="github-url"
                type="url"
                placeholder="https://github.com/username/repository"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                className="input"
              />
            </div>

            <div className="input-group">
              <label htmlFor="devpost-url">Devpost Project URL</label>
              <input
                id="devpost-url"
                type="url"
                placeholder="https://devpost.com/software/project-name"
                value={devpostUrl}
                onChange={(e) => setDevpostUrl(e.target.value)}
                className="input"
              />
            </div>

            <button 
              onClick={handleGenerate}
              className="generate-button"
              disabled={!githubUrl || !devpostUrl}
            >
              Generate Presentation ✨
            </button>

            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}
          </div>
        )}

        {['fetching', 'analyzing', 'creating'].includes(loadingStage) && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p className="loading-message">{getLoadingMessage()}</p>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ 
                  width: loadingStage === 'fetching' ? '33%' : 
                         loadingStage === 'analyzing' ? '66%' : '90%' 
                }}
              ></div>
            </div>
          </div>
        )}

        {loadingStage === 'success' && result && (
          <div className="success-container">
            <div className="success-icon">✅</div>
            <h2>Presentation Created!</h2>
            <p className="success-message">{result.message}</p>
            
            {result.canva_url && (
              <a 
                href={result.canva_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="canva-link"
              >
                Open in Canva 🎨
              </a>
            )}

            {result.presentation_data && (
              <div className="presentation-preview">
                <h3>Presentation Overview</h3>
                <p className="preview-title">
                  {result.presentation_data.presentation_title}
                </p>
                <p className="slide-count">
                  {result.presentation_data.slides?.length || 0} slides generated
                </p>
                
                <details className="presentation-details">
                  <summary>View Presentation Data</summary>
                  <pre className="presentation-json">
                    {JSON.stringify(result.presentation_data, null, 2)}
                  </pre>
                </details>
              </div>
            )}

            <button onClick={handleReset} className="reset-button">
              Generate Another Presentation
            </button>
          </div>
        )}

        {loadingStage === 'error' && (
          <div className="error-container">
            <div className="error-icon-large">❌</div>
            <h2>Oops! Something went wrong</h2>
            <p className="error-details">{error}</p>
            <button onClick={handleReset} className="reset-button">
              Try Again
            </button>
          </div>
        )}

        <footer className="footer">
          <p>Powered by Claude AI, GitHub API, and Canva</p>
        </footer>
      </div>
    </div>
  )
}

export default App
