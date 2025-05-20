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

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
}); 