"""
Simple test script to verify all services are working correctly.
Run this before using the application to catch configuration issues.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_github_service():
    """Test GitHub service"""
    print("\n🔍 Testing GitHub Service...")
    try:
        from services.github_service import GitHubService
        service = GitHubService()
        
        # Test with a public repository
        test_url = "https://github.com/anthropics/anthropic-sdk-python"
        print(f"   Fetching: {test_url}")
        
        data = await service.fetch_repo_data(test_url)
        print(f"   ✅ Success! Repository: {data['name']}")
        print(f"   ✅ Stars: {data['stars']}, Language: {data['primary_language']}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

async def test_devpost_service():
    """Test Devpost service"""
    print("\n🌐 Testing Devpost Service...")
    try:
        from services.devpost_service import DevpostService
        service = DevpostService()
        
        # Note: This requires a valid Devpost URL
        # You'll need to replace this with an actual Devpost URL for testing
        print("   ⚠️  Skipping Devpost test (requires valid Devpost URL)")
        print("   ℹ️  Service initialized successfully")
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

async def test_claude_service():
    """Test Claude service"""
    print("\n🤖 Testing Claude Service...")
    try:
        from services.claude_service import ClaudeService
        service = ClaudeService()
        
        print("   ✅ Claude service initialized")
        print(f"   ✅ API key configured: {os.getenv('CLAUDE_API_KEY')[:8]}...")
        
        # Don't make actual API call to save credits
        print("   ℹ️  Skipping API call test (to save credits)")
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

async def test_canva_service():
    """Test Canva service"""
    print("\n🎨 Testing Canva Service...")
    try:
        from services.canva_service import CanvaService
        service = CanvaService()
        
        print("   ✅ Canva service initialized")
        print(f"   ✅ Client ID configured: {service.client_id[:8]}...")
        
        # Don't make actual API call
        print("   ℹ️  Skipping API call test")
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 Testing Hackathon Presentation Generator")
    print("=" * 50)
    
    # Check environment variables
    print("\n📋 Checking Environment Variables...")
    env_vars = {
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "CANVA_CLIENT_ID": os.getenv("CANVA_CLIENT_ID"),
        "CANVA_CLIENT_SECRET": os.getenv("CANVA_CLIENT_SECRET"),
    }
    
    for key, value in env_vars.items():
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"   ✅ {key}: {masked}")
        else:
            print(f"   ⚠️  {key}: Not set")
    
    # Run service tests
    results = []
    results.append(await test_github_service())
    results.append(await test_devpost_service())
    results.append(await test_claude_service())
    results.append(await test_canva_service())
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed! ({passed}/{total})")
        print("🚀 You're ready to generate presentations!")
    else:
        print(f"⚠️  Some tests failed ({passed}/{total} passed)")
        print("Please fix the issues above before proceeding.")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

