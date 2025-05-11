const questions = [
  { text: "I carefully curate the photos and content I post online.", section: "selfPresentation" },
  { text: "I present a more idealized version of myself on social media.", section: "selfPresentation" },
  { text: "I often edit or filter my photos before posting.", section: "selfPresentation" },
  { text: "I avoid posting content that could reflect poorly on me.", section: "selfPresentation" },
  { text: "My online profile represents who I truly am.", section: "selfPresentation" },
  { text: "I use emojis, GIFs, or memes to express emotions online.", section: "communication" },
  { text: "I'm more comfortable expressing myself in writing than speaking.", section: "communication" },
  { text: "I frequently comment or engage on other people's posts.", section: "communication" },
  { text: "I prefer private messages over public comments.", section: "communication" },
  { text: "I adapt my tone and language depending on the platform or audience.", section: "communication" },
  { text: "I often share personal experiences or opinions publicly online.", section: "privacy" },
  { text: "I'm conscious of what information I share and who sees it.", section: "privacy" },
  { text: "I use different usernames or accounts to separate parts of my life.", section: "privacy" },
  { text: "I've regretted something I posted online.", section: "privacy" },
  { text: "I frequently review my privacy settings.", section: "privacy" },
  { text: "I feel more connected to people online than in real life.", section: "interaction" },
  { text: "I maintain friendships primarily through digital communication.", section: "interaction" },
  { text: "I feel anxious when people don't respond to my messages quickly.", section: "interaction" },
  { text: "I've formed meaningful relationships through online platforms.", section: "interaction" },
  { text: "I compare myself to others based on their social media.", section: "interaction" },
  { text: "I check my social media multiple times a day.", section: "platform" },
  { text: "I follow people or accounts that inspire or entertain me.", section: "platform" },
  { text: "I prefer platforms where I can control how I present myself.", section: "platform" },
  { text: "I enjoy experimenting with new online platforms or tools.", section: "platform" },
  { text: "I use different platforms for different purposes (e.g., work vs. fun).", section: "platform" }
];

window.onload = function () {
  const container = document.getElementById('questions');
  questions.forEach((q, i) => {
    const div = document.createElement('div');
    div.className = 'question';
    div.innerHTML = `${i + 1}. ${q.text} <select name="q${i + 1}">
      <option value="0">--</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option>
    </select>`;
    container.appendChild(div);
  });
};

function calculateResults() {
  const form = document.forms['quizForm'];
  const scores = {
    selfPresentation: 0,
    communication: 0,
    privacy: 0,
    interaction: 0,
    platform: 0
  };
  const counts = { ...scores };

  questions.forEach((q, i) => {
    let val = parseInt(form[`q${i + 1}`].value);
    if (!isNaN(val)) {
      scores[q.section] += val;
      counts[q.section]++;
    }
  });

  let resultText = `<h2>Your Results</h2>`;
  for (let section in scores) {
    let avg = (scores[section] / (counts[section] || 1)).toFixed(2);
    resultText += `<p><strong>${section.replace(/([A-Z])/g, ' $1')}:</strong> ${avg} / 5</p>`;
  }

  document.getElementById('results').innerHTML = resultText;
}
