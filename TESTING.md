# Testing Guide

## Prerequisites for Testing

1. **Anthropic API Key** (Required)
   - Sign up at https://console.anthropic.com/
   - Create an API key
   - Add to `backend/.env` as `ANTHROPIC_API_KEY`

2. **GitHub Token** (Optional but Recommended)
   - Create a Personal Access Token at https://github.com/settings/tokens
   - No special permissions needed (public repo access)
   - Add to `backend/.env` as `GITHUB_TOKEN`

## Quick Start Testing

### Step 1: Set Up Environment

```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_key_here
GITHUB_TOKEN=your_github_token_optional
EOF
```

### Step 2: Start Backend

```bash
# In backend directory with venv activated
python main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Test Backend Health

In a new terminal:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status":"healthy","message":"API is running"}
```

### Step 4: Start Frontend

```bash
# In a new terminal
cd front_end
npm install  # If not already done
npm run dev
```

Expected output:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

### Step 5: Test Full Flow

1. Open browser to `http://localhost:5173`
2. Use these test examples:

#### Example 1: Small Public Repo
- **GitHub URL**: `https://github.com/octocat/Hello-World`
- **Devpost URL**: Use any valid Devpost project

#### Example 2: Your Hackathon Project
- **GitHub URL**: Your own public repository
- **Devpost URL**: Your Devpost submission

## Manual API Testing

You can test the API directly using curl:

```bash
curl -X POST http://localhost:8000/api/generate-presentation \
  -H "Content-Type: application/json" \
  -d '{
    "github_url": "https://github.com/username/repo",
    "devpost_url": "https://devpost.com/software/project"
  }' \
  --output test_presentation.pptx
```

If successful, you'll get a `test_presentation.pptx` file.

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Frontend starts and loads correctly
- [ ] Form validation works (try invalid URLs)
- [ ] Can submit valid GitHub and Devpost URLs
- [ ] Loading states show during generation
- [ ] Presentation downloads automatically
- [ ] PPTX file opens in PowerPoint/Keynote/Google Slides
- [ ] Presentation contains relevant content

## Expected Processing Time

- GitHub data fetch: 2-5 seconds
- Devpost scraping: 1-3 seconds
- Claude AI generation: 30-60 seconds
- **Total**: ~40-70 seconds

## Common Issues During Testing

### Issue: "Module 'anthropic' has no attribute 'beta'"

**Solution:** Update anthropic package:
```bash
pip install --upgrade anthropic
```

### Issue: "ANTHROPIC_API_KEY not found"

**Solution:** Make sure `.env` file exists in `backend/` directory with valid key:
```bash
cd backend
cat .env  # Should show your API key
```

### Issue: CORS errors in browser console

**Solution:** Verify:
1. Backend is running on port 8000
2. Frontend is running on port 5173
3. CORS middleware in `backend/main.py` includes the frontend URL

### Issue: "Repository not found"

**Solution:**
- Check that GitHub URL is correct
- Ensure repository is public
- Try adding a GitHub token to `.env`

### Issue: "Failed to extract PowerPoint file"

**Solution:**
- Check Anthropic API key is valid and has beta access
- Verify you're using the correct model name
- Check backend logs for detailed error messages

## Validation Tests

### Test 1: Invalid GitHub URL

**Input:**
```
GitHub URL: https://invalid-url.com
Devpost URL: https://devpost.com/software/project
```

**Expected:** Error message "Please enter a valid GitHub repository URL"

### Test 2: Invalid Devpost URL

**Input:**
```
GitHub URL: https://github.com/octocat/Hello-World
Devpost URL: https://invalid-url.com
```

**Expected:** Error message "Please enter a valid Devpost project URL"

### Test 3: Private GitHub Repository

**Input:** URL to a private repository

**Expected:** Error message "Repository not found or is private"

### Test 4: Valid Inputs

**Input:** Valid public GitHub repo and Devpost URL

**Expected:**
1. Loading spinner appears
2. Status message: "Fetching repository data..."
3. Status message: "Generating presentation with AI..."
4. File downloads automatically
5. Success message appears
6. Form resets after 3 seconds

## Presentation Quality Checks

After generating a presentation, verify:

- [ ] Title slide includes project name
- [ ] Problem/solution section is clear
- [ ] Technical architecture is accurate
- [ ] Team information is included
- [ ] Slides have consistent design
- [ ] Speaker notes are present
- [ ] 10-15 slides total
- [ ] Content is relevant to the project
- [ ] No Lorem ipsum or placeholder text

## Performance Testing

For load testing (optional):

```bash
# Install hey (HTTP load generator)
# brew install hey  # macOS
# apt-get install hey  # Linux

# Test 10 concurrent requests
hey -n 10 -c 2 -m POST \
  -H "Content-Type: application/json" \
  -d '{"github_url":"https://github.com/octocat/Hello-World","devpost_url":"https://devpost.com/software/project"}' \
  http://localhost:8000/api/generate-presentation
```

## Debugging

Enable detailed logging by modifying `backend/main.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

Then restart the backend and check logs for:
- API request details
- GitHub API responses
- Devpost scraping results
- Claude API interactions
- File processing steps

## Next Steps After Successful Testing

1. ✅ All tests pass
2. 📝 Document any issues found
3. 🎨 (Optional) Customize presentation templates
4. 🚀 (Optional) Deploy to production
5. 🎉 Use for your hackathon presentation!

## Production Deployment Considerations

Before deploying to production:

- [ ] Add rate limiting
- [ ] Implement request queuing for long-running tasks
- [ ] Add user authentication (if needed)
- [ ] Set up proper logging and monitoring
- [ ] Configure production CORS origins
- [ ] Add file cleanup jobs for generated presentations
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Add request timeout handling
- [ ] Implement caching for repeated requests
- [ ] Set up CI/CD pipeline

## Support

If you encounter issues not covered here:

1. Check the backend logs for detailed error messages
2. Verify all dependencies are installed correctly
3. Ensure API keys are valid and have proper permissions
4. Review the README.md for setup instructions
5. Check that all services are running on correct ports


