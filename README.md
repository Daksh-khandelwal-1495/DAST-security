# DAST-test

## Samsung Prism DAST Testing Project

This project implements Dynamic Application Security Testing (DAST) with automated CI/CD integration and Slack notifications for Samsung Prism.

### 🚀 Features

- **Vulnerable Web Application**: Node.js/Express app with intentional security vulnerabilities for testing
- **Automated DAST Scanning**: OWASP ZAP integration via GitHub Actions
- **Slack Integration**: Automated security findings reporting to Slack channels
- **CI/CD Pipeline**: Continuous security testing on every push and pull request

### 🔒 Security Vulnerabilities (Intentional)

The test application includes the following vulnerabilities for DAST testing:

- **Reflected XSS**: Search endpoint vulnerable to cross-site scripting
- **Open Redirect**: Unvalidated URL redirection
- **Insecure Authentication**: Weak login implementation
- **SQL Injection**: Simulated SQL injection vulnerability
- **Sensitive Data Exposure**: Configuration endpoint exposing secrets
- **Missing Security Headers**: No security headers implementation

### 🛠️ Setup

1. **Install Dependencies**:
   ```bash
   npm install
   pip install -r requirements.txt
   ```

2. **Run the Vulnerable Application**:
   ```bash
   npm start
   ```

3. **Configure Slack Integration**:
   - Copy `.env.example` to `.env`
   - Follow instructions in `SLACK_SETUP.md`
   - Add your Slack credentials to GitHub Secrets

### 📊 DAST Scanning

The project uses OWASP ZAP for automated security scanning:

- **Triggers**: Push to main, Pull Requests, Weekly schedule
- **Target**: Deployed application on Railway
- **Reports**: HTML and JSON format
- **Notifications**: Automatic Slack reporting

### 🔧 Configuration Files

- `.github/workflows/zap-baseline.yml`: GitHub Actions workflow
- `.zap/rules.tsv`: ZAP scanning rules configuration
- `slack_reporter.py`: Slack integration script
- `SLACK_SETUP.md`: Detailed Slack setup guide

### 🧪 Testing Slack Integration

Run the test script to verify Slack integration:

```bash
python test_slack_integration.py
```

### 📈 Slack Notifications

The integration provides:
- 📊 Vulnerability count summaries
- 🎯 Target URL and scan timestamps
- 🔴🟠🟡 Color-coded severity indicators
- 📝 Detailed vulnerability listings
- 🔗 Pull request integration

### 🎯 Project Goals

This project demonstrates:
- Shift-left security practices
- Automated vulnerability detection
- ChatOps security reporting
- CI/CD security integration
- Real-time security feedback
