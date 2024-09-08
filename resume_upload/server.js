const http = require('http');
const fs = require('fs');
const path = require('path');
const upload = require('./api/upload');

const server = http.createServer((req, res) => {
  console.log('Received request for:', req.url, 'Method:', req.method);

  if (req.url === '/api/upload' && req.method === 'POST') {
    upload(req, res);
  } else if (req.url === '/submit' && req.method === 'POST') {
    handleSubmit(req, res);
  } else if (req.url === '/' || req.url === '/index.html') {
    serveFile('index.html', res);
  } else if (req.url.startsWith('/result.html')) {
    serveFile('result.html', res);
  } else if (req.url === '/s_p.html') {
    serveFile('s_p.html', res);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
  }
});

function serveFile(filename, res) {
  const filePath = path.join(__dirname, filename);
  console.log('Attempting to serve file:', filePath);
  
  fs.readFile(filePath, (err, content) => {
    if (err) {
      console.error(`Error reading file ${filename}:`, err);
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end(`File ${filename} not found`);
      } else {
        res.writeHead(500);
        res.end(`Error loading ${filename}: ${err.code}`);
      }
    } else {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(content);
    }
  });
}
function handleSubmit(req, res) {
  console.log('Handling submit request');
  let body = '';
  req.on('data', chunk => {
    body += chunk.toString();
  });
  req.on('end', () => {
    console.log('Received data in /submit:', body); // Add this log
    try {
      const data = JSON.parse(body);
      // Process the data as needed
      console.log('Processed data:', data);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ message: 'Submission received', data: data }));
    } catch (error) {
      console.error('Error processing submit data:', error);
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Invalid data received' }));
    }
  });
}

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('Current working directory:', process.cwd());
});