/**
 * Custom middleware for JSON Server
 * Implements /api/register endpoint with validation
 * 
 * Educational Bugs (for QA testing demonstration):
 * - BUG_SHORT_PASSWORD: Allows 7-character passwords (TC-008)
 * - BUG_NO_LOWERCASE: Bypasses lowercase requirement (TC-010)
 * - BUG_XSS_BYPASS: Specific XSS pattern not blocked (TC-020)
 * - BUG_DUPLICATE_ALLOW: Allows duplicate emails in some cases (TC-024)
 */

// Educational bug flags - These are intentional for QA demonstration
const BUGS = {
  SHORT_PASSWORD: process.env.BUG_SHORT_PASSWORD !== 'false',    // TC-008
  NO_LOWERCASE: process.env.BUG_NO_LOWERCASE !== 'false',        // TC-010
  XSS_BYPASS: process.env.BUG_XSS_BYPASS !== 'false',           // TC-020
  DUPLICATE_ALLOW: process.env.BUG_DUPLICATE_ALLOW !== 'false'   // TC-024
};

module.exports = (req, res, next) => {
  // Handle /api/register endpoint
  if (req.path === '/api/register' && req.method === 'POST') {
    let { email, password } = req.body;
    
    // Trim email spaces
    if (typeof email === 'string') {
      email = email.trim();
      req.body.email = email;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      return res.status(400).json({
        error: '잘못된 이메일 형식입니다.',
        code: 'INVALID_EMAIL'
      });
    }
    
    // Security: Block SQL injection patterns in email
    if (email.includes("'") || email.includes('--') || email.includes(';')) {
      return res.status(400).json({
        error: '이메일에 허용되지 않는 문자가 포함되어 있습니다.',
        code: 'INVALID_EMAIL'
      });
    }
    
    // Security: Block XSS patterns in email
    // BUG: TC-020 - Specific XSS pattern bypasses validation
    if (BUGS.XSS_BYPASS && email === '<script>alert(\'XSS\')</script>@test.com') {
      // Intentional bug: This specific XSS pattern is not blocked
      console.log('[BUG TC-020] XSS pattern not blocked:', email);
    } else if (email.includes('<') || email.includes('>') || email.includes('script')) {
      return res.status(400).json({
        error: '이메일에 허용되지 않는 문자가 포함되어 있습니다.',
        code: 'INVALID_EMAIL'
      });
    }
    
    // Security: Block path traversal patterns in email
    if (email.includes('../') || email.includes('..\\')) {
      return res.status(400).json({
        error: '이메일에 허용되지 않는 문자가 포함되어 있습니다.',
        code: 'INVALID_EMAIL'
      });
    }
    
    // Password validation (minimum 8 characters)
    // BUG: TC-008 - Allows 7-character passwords
    if (BUGS.SHORT_PASSWORD && password && password.length === 7) {
      // Intentional bug: 7-character password is incorrectly allowed
      console.log('[BUG TC-008] Short password accepted:', password.length, 'chars');
      // Skip validation and continue
    } else if (!password || password.length < 8) {
      return res.status(400).json({
        error: '비밀번호는 최소 8자 이상이어야 합니다.',
        code: 'INVALID_PASSWORD'
      });
    }
    
    // Check for password complexity (uppercase, lowercase, number, special char)
    // Allow longer passwords up to 128 characters
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[@$!%*?&#]/.test(password);
    
    // BUG: TC-010 - Bypasses lowercase requirement for specific password
    if (BUGS.NO_LOWERCASE && password === 'NOLOWERCASE123!') {
      // Intentional bug: Password without lowercase is incorrectly allowed
      console.log('[BUG TC-010] Password without lowercase accepted');
      // Skip validation and continue
    } else if (!hasUpper || !hasLower || !hasNumber || !hasSpecial) {
      return res.status(400).json({
        error: '비밀번호는 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다.',
        code: 'WEAK_PASSWORD'
      });
    }
    
    // Maximum password length check
    if (password.length > 128) {
      return res.status(400).json({
        error: '비밀번호는 128자 이하여야 합니다.',
        code: 'INVALID_PASSWORD'
      });
    }
    
    // Check for duplicate email in database (case-insensitive)
    const fs = require('fs');
    const dbPath = require('path').join(__dirname, 'db.json');
    const dbContent = fs.readFileSync(dbPath, 'utf8');
    const db = JSON.parse(dbContent);
    
    // BUG: TC-024 - Allows duplicate for specific email
    if (BUGS.DUPLICATE_ALLOW && email === 'duplicate@test.com') {
      // Intentional bug: Duplicate check is bypassed for this specific email
      const duplicateCount = db.users.filter(u => u.email === email).length;
      if (duplicateCount > 0) {
        console.log('[BUG TC-024] Duplicate email allowed:', email, 'Count:', duplicateCount + 1);
        // Skip duplicate check and continue
      }
    } else {
      const existingUser = db.users.find(user => 
        user.email.toLowerCase() === email.toLowerCase()
      );
      if (existingUser) {
        return res.status(400).json({
          error: '이미 등록된 이메일입니다.',
          code: 'DUPLICATE_EMAIL'
        });
      }
    }
    
    // Security: Never store plain password - hash it
    const crypto = require('crypto');
    const hashedPassword = crypto.createHash('sha256').update(password).digest('hex');
    req.body.password = hashedPassword;
    
    // If all validations pass, redirect to standard /users endpoint
    req.url = '/users';
    req.body.created_at = new Date().toISOString();
    
    // Override the response to return status 200 instead of 201
    const originalSend = res.send;
    res.send = function(data) {
      if (res.statusCode === 201) {
        res.status(200);
      }
      originalSend.call(this, data);
    };
  }
  
  // Continue to JSON Server router
  next();
};