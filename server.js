const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(__dirname));

const submissionsPath = path.join(__dirname, 'submissions.json');

app.post('/submissions.json', (req, res) => {
  const submission = req.body;
  fs.readFile(submissionsPath, 'utf8', (err, data) => {
    let submissions = [];
    if (!err && data) {
      try {
        submissions = JSON.parse(data);
      } catch (e) {
        // If file is corrupted, start fresh
        submissions = [];
      }
    }
    submissions.push(submission);
    fs.writeFile(submissionsPath, JSON.stringify(submissions, null, 2), (err) => {
      if (err) {
        console.error('Error writing to submissions.json:', err);
        return res.status(500).json({ success: false, error: 'Failed to save submission.' });
      }
      res.json({ success: true });
    });
  });
});

app.get('/submissions.json', (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const perPage = parseInt(req.query.per_page) || 10;

  fs.readFile(submissionsPath, 'utf8', (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') {
        return res.json({
          success: true,
          submissions: [],
          pagination: {
            page,
            per_page: perPage,
            total: 0,
            total_pages: 0
          }
        });
      }
      console.error('Error reading submissions.json:', err);
      return res.status(500).json({ success: false, error: 'Failed to load submissions.' });
    }

    try {
      const submissions = JSON.parse(data || '[]');
      const total = submissions.length;
      const start = (page - 1) * perPage;
      const paginated = submissions.slice(start, start + perPage);

      res.json({
        success: true,
        submissions: paginated,
        pagination: {
          page,
          per_page: perPage,
          total,
          total_pages: Math.ceil(total / perPage)
        }
      });
    } catch (e) {
      console.error('Error parsing submissions.json:', e);
      res.status(500).json({ success: false, error: 'Failed to parse submissions.' });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
}); 
