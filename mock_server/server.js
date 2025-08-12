/**
 * Custom JSON Server with middleware
 */
const jsonServer = require('json-server');
const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();
const customMiddleware = require('./middleware');

// Set default middlewares (logger, cors, no-cache)
server.use(middlewares);

// Parse JSON bodies
server.use(jsonServer.bodyParser);

// Add /config endpoint for health check
server.get('/config', (req, res) => {
  const db = router.db.getState();
  res.json(db.config || {
    password_min_length: 8,
    password_max_length: 128,
    email_max_length: 255,
    allowed_domains: ["gmail.com", "naver.com", "test.com", "example.com"],
    password_regex: "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
  });
});

// Add custom middleware for /api/register
server.use(customMiddleware);

// Use default router
server.use(router);

// Function to find available port
const net = require('net');

function findAvailablePort(startPort) {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    
    server.listen(startPort, () => {
      const port = server.address().port;
      server.close(() => resolve(port));
    });
    
    server.on('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        // Port is in use, try next port
        console.log(`Port ${startPort} is in use, trying ${startPort + 1}...`);
        findAvailablePort(startPort + 1).then(resolve).catch(reject);
      } else {
        reject(err);
      }
    });
  });
}

// Start server with dynamic port allocation
const DEFAULT_PORT = process.env.PORT || 3000;

async function startServer() {
  try {
    const PORT = await findAvailablePort(DEFAULT_PORT);
    
    server.listen(PORT, () => {
      console.log(`JSON Server is running on port ${PORT}`);
      console.log(`API endpoint: http://localhost:${PORT}/api/register`);
      console.log(`Users endpoint: http://localhost:${PORT}/users`);
      
      // Save port to file for test scripts to read
      const fs = require('fs');
      const path = require('path');
      const portFile = path.join(__dirname, '.port');
      fs.writeFileSync(portFile, PORT.toString());
      
      if (PORT !== DEFAULT_PORT) {
        console.log(`⚠️  Note: Using port ${PORT} instead of default ${DEFAULT_PORT}`);
        console.log(`   Update your test configuration if needed.`);
      }
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();