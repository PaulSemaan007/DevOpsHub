"""
Generate realistic sample data for DevOpsHub
"""
import pandas as pd
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)

# Sample data pools
REQUESTERS = [
    ("Sarah Martinez", "smartinez@lbsfinancial.org", "Branch Manager"),
    ("Michael Chen", "mchen@lbsfinancial.org", "Loan Officer"),
    ("Jennifer Walsh", "jwalsh@lbsfinancial.org", "Compliance Manager"),
    ("David Kumar", "dkumar@lbsfinancial.org", "Operations Director"),
    ("Lisa Thompson", "lthompson@lbsfinancial.org", "Member Services Manager"),
    ("Robert Garcia", "rgarcia@lbsfinancial.org", "Accounting Manager"),
    ("Emily Davis", "edavis@lbsfinancial.org", "Risk Management"),
    ("James Wilson", "jwilson@lbsfinancial.org", "IT Support Lead"),
]

PROGRAMMERS = [
    "Alex Johnson",
    "Maria Rodriguez",
    "Kevin Park",
    "Unassigned"
]

REQUEST_TYPES = ["Custom Program", "SQL Query", "Report", "Script"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
REQUEST_STATUSES = ["Submitted", "In Progress", "Testing", "Completed"]

ERROR_SYSTEMS = ["Datasafe", "Keystone", "Custom Integration"]
ERROR_SEVERITIES = ["Low", "Medium", "High", "Critical"]
ERROR_STATUSES = ["New", "Investigating", "Fixed", "Reported to Fiserv"]

PROJECT_STATUSES = ["Planning", "In Progress", "Testing", "Deployed", "On Hold"]

TECHNOLOGIES = ["Intersystems Cache", "Microsoft .NET", "Python", "PowerShell", "MS SQL", "JavaScript", "HTML"]

def random_date(start_days_ago, end_days_ago=0):
    """Generate random date between start_days_ago and end_days_ago"""
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_days = random.random() * delta.days
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_requests():
    """Generate 30 realistic programming requests"""
    requests = []

    request_scenarios = [
        ("Custom Program", "Member Auto-Pay Enrollment Module", "Build automated enrollment system for member auto-pay setup via online banking", "High"),
        ("SQL Query", "Dormant Accounts Report Q1 2025", "Query to identify accounts with no activity for 12+ months for compliance review", "Medium"),
        ("Report", "Monthly Loan Portfolio Analysis", "Generate executive dashboard with loan breakdown by type, delinquency rates, and trends", "High"),
        ("Script", "Nightly ATM Transaction Reconciliation", "PowerShell script to reconcile ATM transactions with Datasafe core system", "Critical"),
        ("Custom Program", "Wire Transfer Approval Workflow", "Multi-level approval system for wire transfers over $10k with audit trail", "Critical"),
        ("SQL Query", "New Member Growth by Branch", "Extract new member signups by branch location for last 90 days", "Low"),
        ("Report", "Quarterly Regulatory Compliance Report", "NCUA compliance report with asset-to-liability ratios and net worth calculations", "High"),
        ("Script", "Certificate of Deposit Maturity Alerts", "Python script to email members 30 days before CD maturity with renewal options", "Medium"),
        ("Custom Program", "Loan Officer Performance Dashboard", "Real-time dashboard showing loan originations, approval rates, and pipeline by officer", "Medium"),
        ("SQL Query", "Overdraft Fee Analysis", "Query to analyze overdraft fees charged, waived, and member impact for board review", "Medium"),
        ("Report", "Year-End Tax Document Generation", "Automate 1099-INT generation for members with dividend income over $10", "Critical"),
        ("Script", "Daily Branch Cash Limit Monitor", "PowerShell script to alert when branch cash on hand exceeds insurance limits", "High"),
        ("Custom Program", "Member Communication Preference Center", "Allow members to opt in/out of email, SMS, and mail communications by category", "Low"),
        ("SQL Query", "Inactive Loan Officers Cleanup", "Identify loan officer IDs with no activity for employee offboarding", "Low"),
        ("Report", "Mobile Banking Adoption Report", "Track mobile app logins, bill pay usage, and mobile deposit trends", "Medium"),
        ("Script", "Shared Branch Daily Settlement", "Automate settlement file generation for shared branching network transactions", "High"),
        ("Custom Program", "Credit Card Fraud Alert System", "Real-time monitoring for suspicious card transactions with auto-decline rules", "Critical"),
        ("SQL Query", "Member Demographics Breakdown", "Extract member age, income, and location data for marketing campaign planning", "Low"),
        ("Report", "Teller Transaction Accuracy Audit", "Generate report on teller errors, overages/shortages by employee and branch", "Medium"),
        ("Script", "ACH Return Processing Automation", "Python script to parse ACH return files and update member accounts automatically", "High"),
        ("Custom Program", "Collateral Tracking System", "Track loan collateral (vehicles, property) with lien release workflow and valuations", "Medium"),
        ("SQL Query", "High-Value Depositor Identification", "Query members with deposits over $100k for VIP relationship management", "Low"),
        ("Report", "Loan Delinquency Aging Report", "30/60/90 day delinquency report with collection status and payment plans", "High"),
        ("Script", "Service Pack 2024-Q4 Deployment", "PowerShell script to deploy Datasafe Service Pack 2024-Q4 to test environment", "Critical"),
        ("Custom Program", "Branch Appointment Scheduling System", "Online booking system for loan consultations and account openings", "Low"),
        ("SQL Query", "Cross-Sell Opportunity Analysis", "Identify members with checking but no loans for lending campaign targeting", "Medium"),
        ("Report", "Merchant Services Monthly Statement", "Generate merchant processing fees, transaction volumes, and chargebacks by merchant", "Medium"),
        ("Script", "Escheatment Compliance Monitor", "Python script to flag dormant accounts approaching state escheatment deadlines", "High"),
        ("Custom Program", "Employee Security Access Audit Tool", "Track employee access to sensitive member data with timestamped audit logs", "Critical"),
        ("SQL Query", "Credit Bureau Reporting Verification", "Validate loan data accuracy before monthly credit bureau reporting submission", "High"),
    ]

    for i, (req_type, title, description, priority) in enumerate(request_scenarios, 1):
        requester = random.choice(REQUESTERS)
        programmer = random.choice(PROGRAMMERS)

        # Distribute statuses realistically
        if i <= 20:
            status = "Completed"
            created = random_date(90, 30)
            due_date = (datetime.strptime(created, "%Y-%m-%d") + timedelta(days=random.randint(7, 21))).strftime("%Y-%m-%d")
            completed_date = (datetime.strptime(due_date, "%Y-%m-%d") + timedelta(days=random.randint(-3, 5))).strftime("%Y-%m-%d")
        elif i <= 25:
            status = "In Progress"
            created = random_date(30, 5)
            due_date = (datetime.strptime(created, "%Y-%m-%d") + timedelta(days=random.randint(7, 21))).strftime("%Y-%m-%d")
            completed_date = ""
        elif i <= 28:
            status = "Testing"
            created = random_date(14, 5)
            due_date = (datetime.strptime(created, "%Y-%m-%d") + timedelta(days=random.randint(7, 14))).strftime("%Y-%m-%d")
            completed_date = ""
        else:
            status = "Submitted"
            created = random_date(7, 0)
            due_date = (datetime.strptime(created, "%Y-%m-%d") + timedelta(days=random.randint(7, 21))).strftime("%Y-%m-%d")
            completed_date = ""

        requests.append({
            "ID": f"REQ-{i:03d}",
            "Title": title,
            "Description": description,
            "Type": req_type,
            "Priority": priority,
            "Status": status,
            "Requester Name": requester[0],
            "Requester Email": requester[1],
            "Requester Department": requester[2],
            "Assigned To": programmer if status != "Submitted" else "Unassigned",
            "Created Date": created,
            "Due Date": due_date,
            "Completed Date": completed_date,
            "Technology": random.choice(TECHNOLOGIES),
            "Related Project": f"PROJ-{random.randint(1, 8):03d}" if random.random() > 0.6 else ""
        })

    return pd.DataFrame(requests)

def generate_errors():
    """Generate 20 realistic system errors"""
    errors = []

    error_scenarios = [
        ("Datasafe", "High", "ERR-BATCH-001", "Nightly batch job failed - member dividend calculation", "Fixed", "Memory overflow in calculation loop. Added pagination to process members in chunks of 1000.", ""),
        ("Datasafe", "Critical", "ERR-API-002", "Core API timeout on loan origination", "Reported to Fiserv", "API response time exceeds 30s for complex loan products. Fiserv investigating server performance.", "FSV-2024-1847"),
        ("Keystone", "Medium", "ERR-SYNC-003", "Member photo sync failure from imaging system", "Fixed", "Incorrect file path in sync script. Updated to use UNC path instead of mapped drive.", ""),
        ("Custom Integration", "Low", "ERR-RPT-004", "Daily overdraft report email not sending", "Fixed", "SMTP authentication expired. Updated credentials in config file.", ""),
        ("Datasafe", "High", "ERR-TRAN-005", "ATM transaction posting delay", "Investigating", "Transactions from ATM ID 4521 posting 2+ hours late. Checking network connectivity and ISO8583 message queue.", ""),
        ("Datasafe", "Critical", "ERR-WIRE-006", "Wire transfer file generation corrupted", "Reported to Fiserv", "Output file contains invalid characters causing bank rejection. Fiserv patching file encoding logic.", "FSV-2024-1923"),
        ("Custom Integration", "Medium", "ERR-MOB-007", "Mobile banking login intermittent failures", "Fixed", "Session token expiration too aggressive. Extended from 15min to 30min.", ""),
        ("Keystone", "Low", "ERR-LOG-008", "Audit log entries missing timestamps", "Fixed", "Timezone configuration error. Corrected to Pacific Time in system settings.", ""),
        ("Datasafe", "High", "ERR-ACH-009", "ACH return file parsing error", "Fixed", "New return code R85 not recognized. Added to ACH return code lookup table.", ""),
        ("Datasafe", "Medium", "ERR-BAL-010", "Account balance mismatch on statements", "Investigating", "5 member accounts showing incorrect balances on monthly statements. Investigating GL posting sequence.", ""),
        ("Custom Integration", "Critical", "ERR-FRAUD-011", "Credit card fraud detection system offline", "Fixed", "Database connection pool exhausted. Increased max connections from 50 to 100.", ""),
        ("Datasafe", "Low", "ERR-SCH-012", "Certificate maturity reminder job skipped", "Fixed", "Cron job disabled during maintenance and not re-enabled. Reactivated and backfilled missed notices.", ""),
        ("Keystone", "High", "ERR-COLL-013", "Collateral valuation import failure", "Reported to Fiserv", "NADA vehicle value XML format changed. Fiserv updating parser for new schema.", "FSV-2024-2001"),
        ("Custom Integration", "Medium", "ERR-WEB-014", "Online banking dashboard charts not loading", "Fixed", "JavaScript library CDN outage. Switched to local hosting of Chart.js library.", ""),
        ("Datasafe", "Low", "ERR-PRNT-015", "Member statement printing alignment issue", "Fixed", "Printer driver update changed margin defaults. Adjusted print template margins by 0.25in.", ""),
        ("Datasafe", "Critical", "ERR-CORE-016", "Core system slow response during peak hours", "Investigating", "Query response times spike 10x between 9-11am. Running SQL profiler to identify bottlenecks.", ""),
        ("Custom Integration", "Medium", "ERR-EML-017", "Member email notifications delayed", "Fixed", "Email queue processing script hung. Added timeout and retry logic.", ""),
        ("Keystone", "High", "ERR-LOAN-018", "Loan payment allocation error", "Reported to Fiserv", "Extra payments incorrectly applying to future due dates instead of principal. Fiserv investigating payment allocation logic.", "FSV-2024-2043"),
        ("Datasafe", "Low", "ERR-RPT-019", "Board report footer missing page numbers", "Fixed", "Report template variable incorrectly named. Changed {PAGE_NUM} to {PAGE_NUMBER}.", ""),
        ("Custom Integration", "Medium", "ERR-INT-020", "Third-party credit bureau interface timeout", "Investigating", "Experian API calls timing out intermittently. Checking firewall rules and API rate limits.", ""),
    ]

    for i, (system, severity, code, desc, status, notes, ticket) in enumerate(error_scenarios, 1):
        reported = random_date(60, 0)
        resolved = ""
        if status in ["Fixed", "Reported to Fiserv"]:
            resolved = (datetime.strptime(reported, "%Y-%m-%d") + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")

        errors.append({
            "ID": f"ERR-{i:03d}",
            "Error Code": code,
            "System": system,
            "Severity": severity,
            "Description": desc,
            "Status": status,
            "Resolution Notes": notes,
            "Date Reported": reported,
            "Date Resolved": resolved,
            "Reported to Fiserv": "Yes" if status == "Reported to Fiserv" else "No",
            "Fiserv Ticket": ticket
        })

    return pd.DataFrame(errors)

def generate_projects():
    """Generate 8 realistic projects"""
    projects = []

    project_scenarios = [
        ("Datasafe Service Pack 2024-Q4 Implementation", "Deploy latest Datasafe core system updates including security patches and new API endpoints", "Testing", "2024-12-01", "2025-01-15", "", "Alex Johnson, Maria Rodriguez"),
        ("Online Account Opening Portal", "Build member-facing portal for checking/savings account applications with e-signature integration", "In Progress", "2024-11-15", "2025-02-28", "", "Kevin Park"),
        ("Loan Delinquency Management System", "Comprehensive system to track past-due loans, automate collection workflows, and generate skip-trace reports", "Planning", "2025-01-20", "2025-04-30", "", "Alex Johnson"),
        ("Regulatory Compliance Dashboard", "Executive dashboard for NCUA compliance metrics including capital ratios, delinquency rates, and asset quality", "Deployed", "2024-09-01", "2024-11-30", "2024-11-28", "Maria Rodriguez"),
        ("Mobile Banking App v3.0 Upgrade", "Major mobile app update with biometric login, mobile check deposit limit increases, and P2P payments", "In Progress", "2024-10-15", "2025-02-15", "", "Kevin Park, Alex Johnson"),
        ("ACH Processing Automation Enhancement", "Improve ACH file processing with auto-reconciliation, exception handling, and return file automation", "Testing", "2024-11-01", "2025-01-10", "", "Maria Rodriguez"),
        ("Member Data Analytics Platform", "Build data warehouse and analytics tools for member segmentation, cross-sell opportunities, and retention analysis", "Planning", "2025-02-01", "2025-06-30", "", "Unassigned"),
        ("Disaster Recovery System Upgrade", "Implement automated failover to backup data center with RPO < 1 hour and RTO < 4 hours", "On Hold", "2024-08-01", "2025-03-31", "", "Alex Johnson, Kevin Park"),
    ]

    for i, (name, desc, status, start, target, actual, team) in enumerate(project_scenarios, 1):
        # Generate SDLC checklist
        sdlc_phases = [
            "Requirements Gathering",
            "Design & Architecture",
            "Development",
            "Testing & QA",
            "Deployment",
            "Post-Deployment Review"
        ]

        # Mark phases complete based on status
        completion_map = {
            "Planning": 1,
            "In Progress": 3,
            "Testing": 4,
            "Deployed": 6,
            "On Hold": 2
        }
        completed_phases = completion_map[status]

        sdlc_checklist = []
        for j, phase in enumerate(sdlc_phases, 1):
            sdlc_checklist.append({
                "Phase": phase,
                "Status": "Complete" if j <= completed_phases else "Pending",
                "Notes": "Phase completed" if j <= completed_phases else ""
            })

        # Convert checklist to string for CSV storage
        checklist_str = "|".join([f"{p['Phase']}:{p['Status']}" for p in sdlc_checklist])

        # Link to related requests
        request_count = random.randint(2, 5)
        linked_requests = ",".join([f"REQ-{random.randint(1, 30):03d}" for _ in range(request_count)])

        projects.append({
            "ID": f"PROJ-{i:03d}",
            "Project Name": name,
            "Description": desc,
            "Status": status,
            "Start Date": start,
            "Target Completion": target,
            "Actual Completion": actual,
            "Team Members": team,
            "SDLC Checklist": checklist_str,
            "Linked Requests": linked_requests,
            "Current Phase": sdlc_phases[min(completed_phases, len(sdlc_phases)-1)]
        })

    return pd.DataFrame(projects)

if __name__ == "__main__":
    print("Generating sample data for DevOpsHub...")

    # Generate data
    requests_df = generate_requests()
    errors_df = generate_errors()
    projects_df = generate_projects()

    # Save to CSV
    requests_df.to_csv("data/requests.csv", index=False)
    errors_df.to_csv("data/errors.csv", index=False)
    projects_df.to_csv("data/projects.csv", index=False)

    print(f"[OK] Generated {len(requests_df)} requests")
    print(f"[OK] Generated {len(errors_df)} errors")
    print(f"[OK] Generated {len(projects_df)} projects")
    print("\nSample data saved to data/ folder")
