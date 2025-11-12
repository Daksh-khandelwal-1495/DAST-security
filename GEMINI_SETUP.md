# Getting Your Free Gemini API Key (2 Minutes)

## 🚀 Quick Setup Guide

### Step 1: Go to Google AI Studio
Visit: **https://makersuite.google.com/app/apikey**

### Step 2: Sign in with Google Account
- Use any Google account (personal or work)
- No credit card required ✅
- Completely FREE ✅

### Step 3: Create API Key
1. Click **"Create API Key"** button
2. Select **"Create API key in new project"** (or use existing)
3. Copy the generated API key (starts with `AIza...`)

### Step 4: Add to Your Project
```bash
# Open your .env file
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

## ✅ You're Done!

### Free Tier Limits (More than enough for DAST):
- ✅ **15 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **No credit card required**
- ✅ **No expiration**

### Test Your Setup:
```bash
cd /path/to/DAST-test
python ai_classifier_v2.py
```

You should see:
```
✅ Google Gemini initialized (Primary provider)
🤖 AI Providers: Gemini (Primary)
```

## 🔒 Security Best Practices:

1. ✅ **Keep `.env` in `.gitignore`** - Already configured
2. ✅ **Don't commit API keys** - Never push to GitHub
3. ✅ **Use GitHub Secrets for CI/CD** - Add `GEMINI_API_KEY` to repository secrets

## 🆘 Troubleshooting:

**Issue:** "API key not valid"
- **Solution:** Make sure you copied the entire key (starts with `AIza`)

**Issue:** "Quota exceeded"
- **Solution:** You've hit the 1,500/day limit. Wait 24 hours or use Groq as fallback

**Issue:** "Module not found: google.generativeai"
- **Solution:** Run `pip install -r requirements.txt`

## 🎯 For GitHub Actions:

Add your key to repository secrets:
1. Go to **Repository → Settings → Secrets and variables → Actions**
2. Click **"New repository secret"**
3. Name: `GEMINI_API_KEY`
4. Value: Your API key
5. Click **"Add secret"**

## 🚀 Alternative Providers (Optional):

If you want even faster inference or hit rate limits:

### Groq (Ultra Fast, Free):
- **30 requests/min** (2x more than Gemini)
- **14,400 requests/day** (10x more than Gemini)
- Get key: https://console.groq.com/keys

Uncomment in `requirements.txt`:
```bash
groq
```

Add to `.env`:
```bash
GROQ_API_KEY=your-groq-key-here
```

## 📊 Which Should You Use?

| Need | Use |
|------|-----|
| **Best Quality** | Gemini (Primary) ✅ |
| **Maximum Speed** | Groq (uncomment) |
| **High Volume** | Groq (14k/day vs 1.5k/day) |
| **No API Key** | Pattern Matching (automatic fallback) |

## ✨ Current Setup:

Your project is configured to use:
1. **Gemini** (Primary) - For quality
2. **Groq** (Optional) - Uncomment for speed
3. **OpenAI** (Optional) - Uncomment for alternative
4. **Pattern Matching** (Automatic fallback)

**Recommendation:** Start with Gemini (free, no credit card, excellent quality). Add Groq later if you need more speed or higher limits.