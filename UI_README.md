# GuardianAI - Modern Web UI

Clean, simple, and beautiful interface for the GuardianAI fraud detection environment.

## ✨ Features

- **🌙 Dark/Light Mode** - Toggle between dark and light themes, saved automatically
- **📊 Run Episodes** - Run individual agents on demand with real-time results
- **⚖️ Compare Agents** - See how Conservative, Balanced, and Aggressive agents compare
- **📈 Live Charts** - Watch performance metrics displayed as interactive charts
- **📱 Responsive Design** - Works great on desktop, tablet, and mobile
- **⚡ Fast & Simple** - No complex menus or confusing options

## 🚀 Quick Start

### Option 1: Double-Click (Windows)
```
start_ui.bat
```

### Option 2: Command Line
```bash
python app_ui.py
```

### Option 3: PowerShell (Windows)
```powershell
.\start_ui.ps1
```

Then open your browser to: **http://127.0.0.1:5000**

## 📖 How to Use

### Tab 1: Run Episode ▶️
1. **Select Agent** - Choose Conservative, Balanced, or Aggressive
2. **Set Difficulty** - Easy (obvious fraud), Medium (realistic), or Hard (subtle)
3. **Set Steps** - How many transactions to evaluate (50-500)
4. **Click Start** - Watch the results appear with metrics and charts

**You'll see:**
- Accuracy - % of correct predictions
- Precision - accuracy of fraud detection
- Recall - % of actual fraud caught
- F1-Score - balanced metric
- Total Reward - cumulative score
- Charts showing performance over time

### Tab 2: Compare Agents ⚖️
1. **Set Difficulty** - Choose easy, medium, or hard
2. **Set Steps** - How many transactions
3. **Click Compare** - See all 3 agents side-by-side

**Compare:**
- Which agent catches most fraud
- Which is most accurate
- Which has fewest false alarms
- Which performs best at each difficulty

### Tab 3: How It Works ℹ️
- Complete explanation of what GuardianAI does
- How agents learn from feedback
- What each metric means
- Why different agents exist

## 🎨 Customization

### Colors
Edit the CSS variables in `templates/index.html`:
```css
:root {
    --primary: #6366f1;        /* Main color */
    --success: #10b981;        /* Success green */
    --danger: #ef4444;         /* Error red */
}
```

### Difficulty Levels
Adjust fraud rates in `guardianai/environment.py`:
- Easy: 8% fraud rate
- Medium: 5% fraud rate
- Hard: 2.5% fraud rate

### Agent Strategies
Modify agent logic in `agents/__init__.py`:
- Conservative - More cautious decisions
- Balanced - Moderate approach
- Aggressive - Catch maximum fraud

## 📊 Understanding The Metrics

**Accuracy**
- What: % of all predictions correct
- Goal: Higher is better
- Range: 0-100%

**Precision**
- What: When agent says "fraud", how often correct
- Goal: Higher is better (fewer false alarms)
- Range: 0-100%

**Recall**
- What: % of actual fraud the agent catches
- Goal: Higher is better (fewer missed fraud)
- Range: 0-100%

**F1-Score**
- What: Balanced between precision and recall
- Goal: Higher is better
- Range: 0-100%

**Total Reward**
- What: Cumulative score from all decisions
- Positive: Good decisions
- Negative: Bad decisions
- Goal: Maximize

## 🛠️ Technical Details

**Backend:** Python Flask  
**Frontend:** HTML5 + CSS3 + Vanilla JavaScript  
**Charts:** Chart.js  
**Environment:** Gymnasium (OpenEnv standard)  
**Agents:** Pre-trained strategies  

## 🔧 Troubleshooting

**Port already in use?**
```python
# Edit app_ui.py, change port from 5000 to another number:
app.run(host='127.0.0.1', port=5001)  # Use 5001 instead
```

**Flask not installed?**
```bash
pip install flask
```

**Charts not showing?**
- Check that Chart.js loads (requires internet)
- Try refreshing the page
- Check browser console for errors

## 📝 Notes

- All data is local - nothing uploaded to internet
- Episodes reset after each run
- Agents don't learn between runs (stateless)
- Results are random but realistic
- Dark mode preference saved in browser

## 🎓 For Researchers

This UI is built for understanding:
- How AI agents learn from reward signals
- Trade-offs between precision and recall
- Different strategy performance
-Real-world fraud detection challenges

Perfect for:
- Student projects
- Research papers
- Fraud detection studies
- AI agent development

## 📞 Support

For issues or questions about the environment, check:
- docs/ folder for detailed documentation
- examples/ folder for code samples
- README.md for project overview
