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

// Start server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`JSON Server is running on port ${PORT}`);
  console.log(`API endpoint: http://localhost:${PORT}/api/register`);
  console.log(`Users endpoint: http://localhost:${PORT}/users`);
});