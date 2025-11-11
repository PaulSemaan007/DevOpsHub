# DevOpsHub Quickstart Guide

Get DevOpsHub running in 5 minutes!

---

## Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed ([Download here](https://www.python.org/downloads/))
- **Git** (optional, for cloning) ([Download here](https://git-scm.com/downloads))
- **10 MB free disk space**

To check your Python version:
```bash
python --version
```

---

## Installation

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
# Clone or download the repository
git clone https://github.com/paulsemaan007/DevOpsHub.git
cd DevOpsHub

# Run the setup script
setup.bat

# Activate virtual environment
.venv\Scripts\activate

# Start the app
streamlit run app.py
```

**Mac/Linux:**
```bash
# Clone or download the repository
git clone https://github.com/paulsemaan007/DevOpsHub.git
cd DevOpsHub

# Make setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Start the app
streamlit run app.py
```

### Option 2: Manual Setup

If the automated scripts don't work:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Start the app
streamlit run app.py
```

---

## First Launch

1. **The app will open automatically** in your default browser at `http://localhost:8501`
2. **If it doesn't open**, manually navigate to `http://localhost:8501`
3. **You'll see the Dashboard** with sample data pre-loaded

---

## Exploring the Demo

### Dashboard (Home Page)
- View key metrics: Total requests, errors, active projects
- See charts showing request status, error severity, project distribution
- Check recent activity and team workload

### Requests Page
- Click **"📝 Requests"** in the sidebar
- Browse 30 sample programming requests
- Try filtering by Status, Type, Priority
- Click on any request to expand and see details
- Test the "Mark as In Progress" or "Mark as Completed" buttons

### Errors Page
- Click **"⚠️ Errors"** in the sidebar
- View 20 system errors from Datasafe, Keystone, and custom integrations
- See how errors are triaged (Fixed vs. Reported to Fiserv)
- Try updating an error status

### Projects Page
- Click **"📁 Projects"** in the sidebar
- View 8 projects with SDLC compliance tracking
- Expand a project to see the SDLC checklist (Requirements → Design → Dev → Test → Deploy → Review)
- Check linked requests and team assignments

---

## Using Your Own Data

Once you've explored the demo, replace the sample data with your own:

### Method 1: Edit CSV Files

1. Navigate to the `data/` folder
2. Open `requests.csv`, `errors.csv`, or `projects.csv` in Excel or a text editor
3. Follow the format in the existing data
4. Save your changes
5. Refresh the app in your browser (or restart with `streamlit run app.py`)

### Method 2: Use the App Forms

1. Go to the **Requests** page
2. Click the **"➕ New Request"** tab
3. Fill out the form and click "Submit Request"
4. Repeat for Errors and Projects

---

## Common Tasks

### Add a New Request
1. Go to **Requests** page
2. Click **"➕ New Request"** tab
3. Fill in:
   - Title (e.g., "Monthly Loan Report")
   - Type (Custom Program, SQL Query, Report, Script)
   - Priority (Low, Medium, High, Critical)
   - Your name, email, department
   - Description
   - Due date
4. Click **"Submit Request"**

### Log a System Error
1. Go to **Errors** page
2. Click **"➕ Log New Error"** tab
3. Fill in:
   - Error code (e.g., "ERR-BATCH-001")
   - System (Datasafe, Keystone, Custom Integration)
   - Severity (Low, Medium, High, Critical)
   - Description
4. Click **"Log Error"**

### Create a Project
1. Go to **Projects** page
2. Click **"➕ New Project"** tab
3. Fill in:
   - Project name
   - Description
   - Start and target completion dates
   - Status
   - Team members (comma-separated)
4. Click **"Create Project"**

### Update Status
- **Requests:** Expand a request → Click "Mark as In Progress" or "Mark as Completed"
- **Errors:** Expand an error → Click "Mark as Investigating", "Mark as Fixed", or "Report to Fiserv"
- **Projects:** Expand a project → Click "Move to Testing" or "Mark as Deployed"

### Export Data
- Go to any page (Requests, Errors, Projects)
- Click **"📥 Export to CSV"** at the bottom
- Download the CSV file

---

## Stopping the App

To stop DevOpsHub:

1. Go to your terminal/command prompt
2. Press `Ctrl + C`
3. Type `deactivate` to exit the virtual environment

---

## Restarting the App

To restart DevOpsHub later:

**Windows:**
```bash
cd DevOpsHub
.venv\Scripts\activate
streamlit run app.py
```

**Mac/Linux:**
```bash
cd DevOpsHub
source .venv/bin/activate
streamlit run app.py
```

---

## Troubleshooting

### "Python not found"
- Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### "Streamlit command not found"
- Make sure virtual environment is activated
- Try: `python -m streamlit run app.py` instead

### "Port 8501 already in use"
- Another instance of DevOpsHub is running
- Stop it with `Ctrl + C` or change the port:
```bash
streamlit run app.py --server.port 8502
```

### "Data files not found"
- Run: `python generate_sample_data.py` to regenerate sample data
- Or check that you're in the DevOpsHub folder

### Charts not displaying
- Clear browser cache
- Try a different browser (Chrome, Firefox, Edge)
- Check console for JavaScript errors (F12)

### CSV changes not showing
- Refresh the browser (F5)
- Or restart the app (`Ctrl + C` then `streamlit run app.py`)

---

## Next Steps

### Customize DevOpsHub
- **Update team members:** Edit the `PROGRAMMERS` list in `generate_sample_data.py`
- **Change statuses:** Modify dropdown options in page files (`pages/*.py`)
- **Add your branding:** Update footer in `app.py` and page files

### Deploy to Production
- **Free hosting:** Deploy to [Streamlit Cloud](https://streamlit.io/cloud)
- **Self-hosted:** Deploy to AWS, Azure, or your own server
- **Pro version:** Contact paulsemaan007@gmail.com for hosted solution

### Backup Your Data
Regularly copy the `data/` folder to a safe location:
```bash
# Windows
xcopy data backup\data /E /I
# Mac/Linux
cp -r data/ backup/data/
```

### Upgrade to Pro
For multi-user, database backend, email notifications, and more:
Email: paulsemaan007@gmail.com

---

## Getting Help

- **Email:** paulsemaan007@gmail.com
- **GitHub Issues:** [Report bugs](https://github.com/paulsemaan007/DevOpsHub/issues)
- **Documentation:** [README.md](README.md)

---

## FAQ

**Q: Can I use this in production?**
A: Yes! The free version is fully functional. For teams >5 people, consider the Pro version with database backend.

**Q: How do I share this with my team?**
A: Deploy to Streamlit Cloud (free) or use the Pro hosted version. The free version is single-user unless you set up a shared server.

**Q: Can I customize the fields?**
A: Yes! Edit the CSV structure and update the forms in page files. See README.md for data dictionary.

**Q: Is my data backed up?**
A: CSV files are stored locally. You're responsible for backups. Pro version includes automated backups.

**Q: Can I import data from Jira/Excel?**
A: Yes! Convert your data to the CSV format (see data dictionary in README) and replace the files in `data/`.

---

**Ready to start?** Run `streamlit run app.py` and explore!

**Need help?** Email paulsemaan007@gmail.com

---

*Built by AppForge Labs | [appforge-labs.com](https://appforge-labs.com)*
