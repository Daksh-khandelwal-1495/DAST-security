# Free AI API Setup Guide

This guide helps you set up **completely FREE** AI services for vulnerability classification.

## 🆓 Option 1: Google Gemini (Recommended - FREE)

### Features:
- ✅ **100% Free** - 60 requests per minute
- ✅ **No credit card required**
- ✅ **Best accuracy for security analysis**
- ✅ **Easy setup (2 minutes)**

### Setup Steps:

1. **Get API Key:**
   - Go to: https://makersuite.google.com/app/apikey
   - Click "Get API Key"
   - Click "Create API key in new project"
   - Copy your API key

2. **Add to .env file:**
   ```bash
   GEMINI_API_KEY=your-api-key-here
   ```

3. **That's it!** No payment info needed.

---

## 🚀 Option 2: Groq (FREE & Super Fast)

### Features:
- ✅ **100% Free** - Fast inference
- ✅ **No credit card required**
- ✅ **Uses Llama 3.3 70B model**
- ✅ **Very fast responses**

### Setup Steps:

1. **Get API Key:**
   - Go to: https://console.groq.com/
   - Sign up with email (no payment needed)
   - Go to "API Keys" section
   - Create new API key
   - Copy your API key

2. **Add to .env file:**
   ```bash
   GROQ_API_KEY=your-api-key-here
   ```

---

## 🔧 Option 3: Local Pattern Matching (No API Needed)

If you don't want to use any external APIs:

1. **Set in .env:**
   ```bash
   USE_AI_CLASSIFICATION=false
   ```

2. **Uses built-in pattern matching** - No AI, but still effective!

---

## 🎯 Which One Should You Choose?

### For Best Results:
**Use both Gemini + Groq:**
```bash
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
USE_AI_CLASSIFICATION=true
```
The system will automatically use Gemini first, fall back to Groq if needed.

### For Zero Cost & Privacy:
**Use local pattern matching:**
```bash
USE_AI_CLASSIFICATION=false
```

### For Speed:
**Use Groq only:**
```bash
GROQ_API_KEY=your-groq-key
USE_AI_CLASSIFICATION=true
```

---

## 📊 Comparison:

| Feature | Gemini | Groq | Local |
|---------|---------|------|-------|
| Cost | FREE | FREE | FREE |
| Speed | Fast | Very Fast | Instant |
| Accuracy | Excellent | Very Good | Good |
| API Required | Yes | Yes | No |
| Rate Limit | 60/min | High | None |
| Privacy | External | External | Local |

---

## 🧪 Testing Your Setup:

After adding your API keys:

```bash
# Test the AI classifier
python ai_classifier.py

# Test full integration
python test_enhanced_integration.py
```

---

## 🔒 Security Notes:

1. **Never commit API keys** to git
2. **Keep .env file private**
3. **API keys are free but personal** - don't share
4. **Both services are legitimate** and widely used

---

## 💡 Pro Tips:

1. **Use both Gemini and Groq** for redundancy
2. **Gemini is better** for complex vulnerability analysis
3. **Groq is faster** for bulk classifications
4. **Local mode** is perfect for air-gapped environments
5. **All options are production-ready**

---

## ⚠️ Troubleshooting:

### "API key invalid":
- Make sure you copied the complete key
- Check for extra spaces
- Regenerate the key if needed

### "Rate limit exceeded":
- Wait a minute and try again
- Use both Gemini + Groq for redundancy
- Consider local mode for high-volume scanning

### "Import errors":
- Run: `pip install -r requirements.txt`
- Make sure you have Python 3.8+

---

## 🎉 Ready to Go!

Once you have at least one API key configured, you can:

1. Run enhanced security scans with AI classification
2. Get intelligent vulnerability categorization
3. Receive better Slack notifications
4. All completely FREE!

**No credit cards. No trials. Just free AI-powered security scanning!** 🚀