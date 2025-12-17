const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

const users = [
  { id: 1, username: 'admin', password: 'password123', balance: 10000 },
  { id: 2, username: 'test', password: 'test', balance: 500 }
];

const documents = [
  { id: 1, userId: 1, title: 'Secret Document', content: 'Admin only content' },
  { id: 2, userId: 2, title: 'User Document', content: 'Regular user content' }
];

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Vulnerable search (Reflected XSS)
app.get('/search', (req, res) => {
  const q = req.query.q || '';
  res.send(`<h1>Results for: ${q}</h1>`);
});

// Stored XSS vulnerability
app.post('/comment', (req, res) => {
  const { comment } = req.body;
  // In real app, this would be stored in DB
  res.send(`<p>Comment posted: ${comment}</p>`);
});

// Open redirect
app.get('/redirect', (req, res) => {
  const url = req.query.url;
  if (url) {
    res.redirect(url); // Unsafe
  } else {
    res.send('No URL provided.');
  }
});

// Insecure login (no hashing, no validation, verbose error messages)
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);

  if (user) {
    res.send(`Welcome, ${username}!`);
  } else {
    res.status(401).send('Invalid username or password. Hint: try admin/password123');
  }
});

// SQL Injection simulation (No parameterization)
app.get('/user', (req, res) => {
  const id = req.query.id;
  // Pretend SQL query without sanitization
  res.send(`Fetched user with ID: ${id}<br>Query: SELECT * FROM users WHERE id = ${id}`);
});

// IDOR - Insecure Direct Object Reference
app.get('/api/document/:id', (req, res) => {
  const docId = parseInt(req.params.id);
  const doc = documents.find(d => d.id === docId);
  
  // No authorization check - any user can access any document!
  if (doc) {
    res.json(doc);
  } else {
    res.status(404).json({ error: 'Document not found' });
  }
});

// CSRF - No CSRF token validation
app.post('/api/transfer', (req, res) => {
  const { from, to, amount } = req.body;
  // No CSRF protection - vulnerable to cross-site request forgery
  res.json({ 
    success: true,
    message: `Transferred $${amount} from user ${from} to user ${to}`,
    warning: 'No CSRF protection!'
  });
});

// Command Injection vulnerability
app.get('/ping', (req, res) => {
  const host = req.query.host || 'localhost';
  // Dangerous - executes shell command with user input
  res.send(`Pinging ${host}... (Command: ping -c 3 ${host})`);
});

// Path Traversal vulnerability
app.get('/download', (req, res) => {
  const filename = req.query.file;
  // Vulnerable to path traversal: /download?file=../../../etc/passwd
  res.send(`Downloading file: ${filename}`);
});

// XXE - XML External Entity (simulation)
app.post('/upload-xml', (req, res) => {
  const xml = req.body.xml;
  // Simulated XXE vulnerability - would parse XML without disabling external entities
  res.send(`Processing XML: ${xml}<br>Warning: XXE vulnerability present`);
});

// SSRF - Server-Side Request Forgery
app.get('/fetch-url', (req, res) => {
  const url = req.query.url;
  // Vulnerable to SSRF - server makes request to arbitrary URL
  res.send(`Fetching URL: ${url}<br>Warning: SSRF vulnerability`);
});

// Insecure Deserialization (simulation)
app.post('/api/import', (req, res) => {
  const data = req.body.data;
  // Would deserialize untrusted data without validation
  res.json({ 
    message: 'Data imported',
    warning: 'Insecure deserialization vulnerability',
    data: data
  });
});

// Race Condition vulnerability
let accountBalance = 1000;
app.post('/withdraw', (req, res) => {
  const amount = parseInt(req.body.amount);
  // Race condition - no locking mechanism
  if (accountBalance >= amount) {
    setTimeout(() => {
      accountBalance -= amount;
      res.json({ balance: accountBalance, withdrawn: amount });
    }, 100);
  } else {
    res.status(400).json({ error: 'Insufficient funds' });
  }
});

// Information Disclosure via Error Messages
app.get('/api/admin', (req, res) => {
  const token = req.query.token;
  if (token !== 'secret-admin-token-12345') {
    // Verbose error revealing internal details
    res.status(401).json({
      error: 'Unauthorized',
      details: 'Invalid token. Expected format: secret-admin-token-XXXXX',
      validTokenExample: 'secret-admin-token-12345'
    });
  } else {
    res.json({ message: 'Admin access granted' });
  }
});

// Weak Session Management
app.post('/session', (req, res) => {
  const { username } = req.body;
  // Predictable session ID
  const sessionId = `${username}-${Date.now()}`;
  res.json({ sessionId, warning: 'Predictable session ID' });
});

// Sensitive data exposure
app.get('/config', (req, res) => {
  res.send({
    dbHost: 'localhost',
    dbUser: 'root',
    dbPassword: 'supersecret',
    apiKey: 'sk-proj-abcd1234567890',
    jwtSecret: 'my-secret-key-12345'
  });
});

// Missing security headers
app.get('/', (req, res) => {
  res.send(`
    <h1>Welcome to the Vulnerable App</h1>
    <p>Test various security vulnerabilities:</p>
    
    <h2>XSS Tests</h2>
    <form action="/search" method="get">
      <input type="text" name="q" placeholder="Search...">
      <button type="submit">Search (XSS)</button>
    </form>
    
    <form action="/comment" method="post">
      <input type="text" name="comment" placeholder="Comment...">
      <button type="submit">Post Comment (Stored XSS)</button>
    </form>
    
    <h2>Injection Tests</h2>
    <a href="/user?id=1 OR 1=1">SQL Injection</a><br>
    <a href="/ping?host=localhost; cat /etc/passwd">Command Injection</a><br>
    
    <h2>Access Control</h2>
    <a href="/api/document/1">IDOR Test</a><br>
    <a href="/api/admin?token=wrong">Admin Access</a><br>
    
    <h2>Other Vulnerabilities</h2>
    <a href="/redirect?url=https://evil.com">Open Redirect</a><br>
    <a href="/download?file=../../../etc/passwd">Path Traversal</a><br>
    <a href="/fetch-url?url=http://169.254.169.254/latest/meta-data/">SSRF</a><br>
    <a href="/config">Sensitive Data Exposure</a><br>
    
    <form action="/login" method="post">
      <input type="text" name="username" placeholder="Username">
      <input type="password" name="password" placeholder="Password">
      <button type="submit">Login</button>
    </form>
  `);
});

// Health check endpoint for Docker
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
  console.log(`Vulnerable endpoints ready for DAST testing`);
});
