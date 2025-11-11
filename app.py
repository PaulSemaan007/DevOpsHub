"""
DevOpsHub - Internal Development Operations Hub for Core Banking IT Teams
Built from real job requirements at LBS Financial Credit Union
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="DevOpsHub - Development Operations Dashboard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .status-completed { background-color: #d4edda; color: #155724; }
    .status-inprogress { background-color: #fff3cd; color: #856404; }
    .status-submitted { background-color: #d1ecf1; color: #0c5460; }
    .status-testing { background-color: #e2e3e5; color: #383d41; }
    .status-critical { background-color: #f8d7da; color: #721c24; }
    .status-high { background-color: #fff3cd; color: #856404; }
    .status-medium { background-color: #d1ecf1; color: #0c5460; }
    .status-low { background-color: #d4edda; color: #155724; }
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
        text-align: center;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load all CSV data"""
    try:
        requests = pd.read_csv("data/requests.csv")
        errors = pd.read_csv("data/errors.csv")
        projects = pd.read_csv("data/projects.csv")
        return requests, errors, projects
    except FileNotFoundError:
        st.error("Data files not found. Please run generate_sample_data.py first.")
        st.stop()

requests_df, errors_df, projects_df = load_data()

# Sidebar navigation
st.sidebar.markdown("# 🔧 DevOpsHub")
st.sidebar.markdown("*Development Operations Dashboard*")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigate to:",
    ["📊 Dashboard", "📝 Requests", "⚠️ Errors", "📁 Projects"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "DevOpsHub helps internal development teams track programming requests, "
    "monitor system errors, and manage projects with SDLC compliance."
)

st.sidebar.markdown("### Free vs Pro")
st.sidebar.markdown("""
**Free (Current)**
- Single-user mode
- CSV data storage
- All core features

**Pro Version**
- Multi-user with auth
- Database backend
- Email notifications
- Fiserv API integration
- Custom branding
""")

if st.sidebar.button("🚀 Upgrade to Pro"):
    st.sidebar.success("Contact: paulsemaan007@gmail.com")

# Main content
if page == "📊 Dashboard":
    st.markdown('<div class="main-header">📊 DevOpsHub Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Real-time overview of development operations</div>', unsafe_allow_html=True)

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_requests = len(requests_df)
        open_requests = len(requests_df[requests_df["Status"] != "Completed"])
        st.metric(
            "Total Requests",
            total_requests,
            f"{open_requests} open",
            delta_color="inverse"
        )

    with col2:
        total_errors = len(errors_df)
        open_errors = len(errors_df[errors_df["Status"].isin(["New", "Investigating"])])
        st.metric(
            "System Errors",
            total_errors,
            f"{open_errors} open",
            delta_color="inverse"
        )

    with col3:
        active_projects = len(projects_df[projects_df["Status"].isin(["Planning", "In Progress", "Testing"])])
        total_projects = len(projects_df)
        st.metric(
            "Active Projects",
            active_projects,
            f"of {total_projects} total"
        )

    with col4:
        completed_requests = requests_df[requests_df["Status"] == "Completed"].copy()
        if len(completed_requests) > 0:
            completed_requests["Created Date"] = pd.to_datetime(completed_requests["Created Date"])
            completed_requests["Completed Date"] = pd.to_datetime(completed_requests["Completed Date"])
            completed_requests["Resolution Days"] = (completed_requests["Completed Date"] - completed_requests["Created Date"]).dt.days
            avg_resolution = completed_requests["Resolution Days"].mean()
            st.metric(
                "Avg Resolution Time",
                f"{avg_resolution:.1f} days",
                "for completed requests"
            )

    st.markdown("---")

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Requests by Status")
        status_counts = requests_df["Status"].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color=status_counts.index,
            color_discrete_map={
                "Completed": "#28a745",
                "In Progress": "#ffc107",
                "Testing": "#6c757d",
                "Submitted": "#17a2b8"
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("📊 Requests by Type")
        type_counts = requests_df["Type"].value_counts()
        fig = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            labels={"x": "Request Type", "y": "Count"},
            color=type_counts.values,
            color_continuous_scale="Blues"
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, width='stretch')

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚠️ Errors by Severity")
        severity_counts = errors_df["Severity"].value_counts()
        severity_order = ["Low", "Medium", "High", "Critical"]
        severity_counts = severity_counts.reindex(severity_order, fill_value=0)

        fig = px.bar(
            x=severity_counts.index,
            y=severity_counts.values,
            labels={"x": "Severity", "y": "Count"},
            color=severity_counts.index,
            color_discrete_map={
                "Low": "#28a745",
                "Medium": "#ffc107",
                "High": "#fd7e14",
                "Critical": "#dc3545"
            }
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("📁 Projects by Status")
        project_status_counts = projects_df["Status"].value_counts()
        fig = px.bar(
            x=project_status_counts.index,
            y=project_status_counts.values,
            labels={"x": "Project Status", "y": "Count"},
            color=project_status_counts.values,
            color_continuous_scale="Viridis"
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, width='stretch')

    st.markdown("---")

    # Recent activity
    st.subheader("🕐 Recent Activity")

    # Get recent requests (last 7 days)
    requests_df["Created Date"] = pd.to_datetime(requests_df["Created Date"])
    recent_date = datetime.now() - timedelta(days=7)
    recent_requests = requests_df[requests_df["Created Date"] >= recent_date].sort_values("Created Date", ascending=False)

    if len(recent_requests) > 0:
        st.markdown("**Recent Requests (Last 7 Days)**")
        for _, req in recent_requests.head(5).iterrows():
            status_class = req["Status"].lower().replace(" ", "")
            st.markdown(
                f'<div style="padding: 0.5rem; margin: 0.5rem 0; background-color: #f8f9fa; border-radius: 0.25rem;">'
                f'<strong>{req["ID"]}</strong> - {req["Title"]}<br>'
                f'<span class="status-badge status-{status_class}">{req["Status"]}</span> '
                f'<span style="color: #666;">| {req["Type"]} | Priority: {req["Priority"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("No recent requests in the last 7 days.")

    # Team workload
    st.markdown("---")
    st.subheader("👥 Team Workload")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Requests by Assignee**")
        active_requests = requests_df[requests_df["Status"] != "Completed"]
        assignee_counts = active_requests["Assigned To"].value_counts()

        for assignee, count in assignee_counts.items():
            if assignee != "Unassigned":
                st.markdown(f"**{assignee}**: {count} active requests")

    with col2:
        st.markdown("**Projects by Team Member**")
        # Parse team members from projects
        team_workload = {}
        for _, proj in projects_df[projects_df["Status"].isin(["In Progress", "Testing"])].iterrows():
            members = proj["Team Members"].split(", ")
            for member in members:
                if member != "Unassigned":
                    team_workload[member] = team_workload.get(member, 0) + 1

        for member, count in sorted(team_workload.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"**{member}**: {count} active projects")

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer">'
    '<strong>DevOpsHub</strong> — Powered by <strong>AppForge Labs</strong><br>'
    'Built from real job requirements | '
    '<a href="mailto:paulsemaan007@gmail.com">Contact for Pro Version</a>'
    '</div>',
    unsafe_allow_html=True
)
