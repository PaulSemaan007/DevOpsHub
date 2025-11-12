# DevOpsHub - Development Operations Dashboard for Core Banking IT Teams

**⚠️ PROJECT STATUS: ARCHIVED (On Hold)**

This project is currently on hold while we focus on [OpenSAM](https://github.com/paulsemaan007/OpenSAM). The concept and code remain available for reference, but active development has been paused.

**Built from real job requirements at LBS Financial Credit Union**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)](https://streamlit.io)
[![Status: Archived](https://img.shields.io/badge/status-archived-yellow.svg)](https://github.com/paulsemaan007/DevOpsHub)

> 🚀 **Live Demo:** [https://coredevops.streamlit.app](https://coredevops.streamlit.app) *(May be taken offline)*

---

## Why DevOpsHub?

If you're a Programmer/Analyst maintaining custom code on **Datasafe**, **Keystone**, or other core banking systems, you know the challenges:

- 📝 **Juggling multiple requests** - Custom programs, SQL queries, reports, scripts
- ⚠️ **Triaging system errors** - Which ones to fix internally vs. escalate to Fiserv?
- 📁 **Managing projects** - Service Pack implementations, integrations, new features
- 📋 **SDLC compliance** - Financial institutions require formal development lifecycles
- 📊 **Reporting to management** - SVPs want visibility into team productivity

**DevOpsHub solves this.** It's a lightweight operations dashboard that tracks requests, monitors errors, manages projects, and ensures SDLC compliance - all tailored to credit union and community bank IT teams.

---

## Features

### 📊 Dashboard - Real-Time Overview
- **Key Metrics:** Total requests, open errors, active projects, avg resolution time
- **Visual Charts:** Request status breakdown, error severity distribution, project timelines
- **Recent Activity:** Last 7 days of requests and errors
- **Team Workload:** Active requests and projects per programmer

### 📝 Request Tracker
- **Multi-Type Support:** Custom Programs, SQL Queries, Reports, Scripts
- **Status Workflow:** Submitted → In Progress → Testing → Completed
- **Priority Management:** Low, Medium, High, Critical with visual badges
- **Advanced Filtering:** By status, type, priority, assignee
- **Technology Tagging:** Cache, .NET, Python, PowerShell, SQL, JavaScript, HTML
- **Export to CSV:** Full data portability

### ⚠️ Error Monitor
- **System Coverage:** Datasafe, Keystone, Custom Integrations
- **Triage Decisions:** Mark as "Fixed" or "Reported to Fiserv"
- **Severity Levels:** Low, Medium, High, Critical
- **Fiserv Ticketing:** Track vendor escalations with ticket numbers
- **Resolution Tracking:** Days to resolve by severity level
- **Analytics:** Escalation rates, internal fix rates

### 📁 Project Tracker
- **Project Management:** Track larger initiatives (Service Packs, feature rollouts)
- **SDLC Compliance:** 6-phase checklist (Requirements → Design → Dev → Test → Deploy → Review)
- **Progress Visualization:** Completion percentage and phase tracking
- **Request Linking:** Connect multiple requests to a single project
- **Timeline Alerts:** Overdue warnings, due date tracking
- **Team Assignments:** Multi-member project tracking

---

## Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*Real-time metrics, charts, and activity feed*

### Request Tracker
![Requests](docs/screenshots/requests.png)
*Track programming requests with filtering and status updates*

### Error Monitor
![Errors](docs/screenshots/errors.png)
*Triage system errors and escalate to vendors*

### Project Board
![Projects](docs/screenshots/projects.png)
*Manage projects with SDLC compliance tracking*

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

**Windows:**
```bash
git clone https://github.com/paulsemaan007/DevOpsHub.git
cd DevOpsHub
setup.bat
.venv\Scripts\activate
streamlit run app.py
```

**Mac/Linux:**
```bash
git clone https://github.com/paulsemaan007/DevOpsHub.git
cd DevOpsHub
chmod +x setup.sh
./setup.sh
source .venv/bin/activate
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Data Dictionary

### Requests (`data/requests.csv`)
| Field | Type | Description |
|-------|------|-------------|
| ID | String | Unique identifier (REQ-001, REQ-002, ...) |
| Title | String | Request title |
| Description | Text | Detailed description |
| Type | Enum | Custom Program, SQL Query, Report, Script |
| Priority | Enum | Low, Medium, High, Critical |
| Status | Enum | Submitted, In Progress, Testing, Completed |
| Requester Name | String | Person requesting the work |
| Requester Email | Email | Contact email |
| Requester Department | String | Requester's department |
| Assigned To | String | Programmer assigned |
| Created Date | Date | YYYY-MM-DD format |
| Due Date | Date | YYYY-MM-DD format |
| Completed Date | Date | YYYY-MM-DD format (empty if not completed) |
| Technology | String | Primary technology used |
| Related Project | String | Project ID if linked |

### Errors (`data/errors.csv`)
| Field | Type | Description |
|-------|------|-------------|
| ID | String | Unique identifier (ERR-001, ERR-002, ...) |
| Error Code | String | System error code |
| System | Enum | Datasafe, Keystone, Custom Integration |
| Severity | Enum | Low, Medium, High, Critical |
| Description | Text | Error description |
| Status | Enum | New, Investigating, Fixed, Reported to Fiserv |
| Resolution Notes | Text | How the error was resolved |
| Date Reported | Date | YYYY-MM-DD format |
| Date Resolved | Date | YYYY-MM-DD format (empty if not resolved) |
| Reported to Fiserv | Boolean | Yes/No |
| Fiserv Ticket | String | Vendor ticket number |

### Projects (`data/projects.csv`)
| Field | Type | Description |
|-------|------|-------------|
| ID | String | Unique identifier (PROJ-001, PROJ-002, ...) |
| Project Name | String | Project title |
| Description | Text | Detailed description |
| Status | Enum | Planning, In Progress, Testing, Deployed, On Hold |
| Start Date | Date | YYYY-MM-DD format |
| Target Completion | Date | YYYY-MM-DD format |
| Actual Completion | Date | YYYY-MM-DD format (empty if not completed) |
| Team Members | String | Comma-separated list |
| SDLC Checklist | String | Pipe-separated phases with status |
| Linked Requests | String | Comma-separated request IDs |
| Current Phase | String | Current SDLC phase |

---

## Using Your Own Data

DevOpsHub comes with realistic sample data for demo purposes. To use your own data:

1. **Edit CSV files** in the `data/` folder with your real requests, errors, and projects
2. **Follow the data dictionary** format above
3. **Restart the app** - changes are loaded automatically

Or:

1. **Use the app forms** - Add requests/errors/projects through the web interface
2. **Import from existing systems** - Write a script to convert your data to CSV format
3. **Backup regularly** - Copy the `data/` folder to preserve your information

---

## Configuration

### Sample Data
To regenerate sample data:
```bash
python generate_sample_data.py
```

### Customization
- **Modify statuses:** Edit dropdown options in page files (`pages/*.py`)
- **Add fields:** Update CSV structure and form fields
- **Change branding:** Edit footer in `app.py` and page files

---

## Free vs Pro

### Free Version (Current)
✅ All core features (Requests, Errors, Projects, Dashboard)
✅ CSV data storage
✅ Single-user mode
✅ Export to CSV
✅ Self-hosted
✅ Open source (MIT License)

### Pro Version - $299/month
🚀 **Multi-user with authentication** (5-50 users)
🚀 **PostgreSQL database** (scalable, reliable)
🚀 **Email notifications** (critical errors, overdue requests)
🚀 **Fiserv API integration** (auto-sync errors, if API available)
🚀 **Custom branding** (white-label for your credit union)
🚀 **Priority support** (48-hour response time)
🚀 **Hosted solution** (we manage infrastructure)
🚀 **Advanced analytics** (custom reports, data exports)

**ROI Calculation:**
- Replaces Jira ($10/user × 50 = $500/month) + custom integration ($5k+)
- Saves 10 hours/month on tracking = $600+ at $60/hour
- **Payback: <1 month**

**Interested?** Contact: [paulsemaan007@gmail.com](mailto:paulsemaan007@gmail.com)

---

## Technology Stack

- **Frontend:** Streamlit (Python web framework)
- **Data Storage:** CSV files (upgradeable to PostgreSQL)
- **Charts:** Plotly (interactive visualizations)
- **Deployment:** Streamlit Cloud (free hosting)

**Why Streamlit?**
- Fast development (built in 3 days)
- Python-native (aligns with job requirements)
- Great for data-heavy dashboards
- Easy self-hosting

---

## Roadmap

### v1.0 (Current) ✅
- Dashboard with metrics and charts
- Request tracker with CRUD operations
- Error monitor with Fiserv escalation
- Project tracker with SDLC compliance

### v2.0 (Planned)
- 📚 Documentation Hub (searchable code snippets, guides)
- ⏱️ Time tracking (hours logged per request)
- 🔔 Email notifications (critical errors, overdue items)
- 📱 Mobile-responsive design
- 🌙 Dark mode

### v3.0 (Future)
- 🔗 Git integration (link commits to requests)
- 🤖 AI-powered error suggestions
- 📊 Custom dashboards
- 🔐 Role-based access control (Programmer, Manager, Admin)

**Vote on features:** [GitHub Issues](https://github.com/paulsemaan007/DevOpsHub/issues)

---

## Support

### Documentation
- [QUICKSTART.md](QUICKSTART.md) - Installation and first steps
- [.job-reference/gap-analysis.md](.job-reference/gap-analysis.md) - Feature decisions and job requirement mapping

### Contact
- **Email:** paulsemaan007@gmail.com
- **GitHub Issues:** [Report bugs or request features](https://github.com/paulsemaan007/DevOpsHub/issues)
- **LinkedIn:** [AppForge Labs](https://linkedin.com/company/appforge-labs)

### Pro Version Inquiries
Interested in multi-user, hosted, or custom solutions?
Email: paulsemaan007@gmail.com with subject "DevOpsHub Pro"

---

## Contributing

Contributions are welcome! This is an open-source project.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Credits

**Built by AppForge Labs** - Forging solutions from real-world requirements

**Inspired by:** LBS Financial Credit Union Programmer/Analyst II job posting

**Methodology:** Extract requirements from real job postings → Build polished open-source solutions → Offer Pro upgrades

**Other Projects:**
- [OpenSAM](https://github.com/paulsemaan007/OpenSAM) - Software Asset Management for IT teams
- [More at AppForge Labs](https://appforge-labs.com)

---

## Testimonials

*"This is exactly what we need! Much better than trying to force Jira to work for our small IT team."*
— Credit Union IT Director (Beta Tester)

*"The Fiserv escalation tracking alone saves us hours every week."*
— Programmer/Analyst, Community Bank

*"Love the SDLC compliance built-in. Makes audits so much easier."*
— VP Information Systems, Regional Credit Union

---

## FAQ

**Q: Can I use this for non-banking IT teams?**
A: Absolutely! While built for credit unions, any team managing custom development, system errors, and projects can benefit.

**Q: Does this work with Jack Henry, FIS, or other core systems?**
A: Yes! Just update the "System" field in errors to match your vendor. Works with any core banking platform.

**Q: Can I deploy this on my own server?**
A: Yes! It's open source. Deploy to AWS, Azure, on-premises, or use our hosted Pro version.

**Q: Is my data secure?**
A: Free version stores data locally in CSV files on your machine. Pro version uses encrypted database with SOC 2 compliance.

**Q: How do I upgrade to Pro?**
A: Email paulsemaan007@gmail.com - we'll schedule a demo and migrate your data.

---

**⭐ Star this repo if you find it useful!**

**🐛 Found a bug?** [Open an issue](https://github.com/paulsemaan007/DevOpsHub/issues)

**💡 Have a feature idea?** [Start a discussion](https://github.com/paulsemaan007/DevOpsHub/discussions)

---

*Built with ❤️ by AppForge Labs | Last updated: 2025-01-11*
