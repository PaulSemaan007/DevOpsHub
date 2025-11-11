"""
Projects Page - Track projects with SDLC compliance
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Projects - DevOpsHub", page_icon="📁", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .status-planning { background-color: #d1ecf1; color: #0c5460; }
    .status-inprogress { background-color: #fff3cd; color: #856404; }
    .status-testing { background-color: #e2e3e5; color: #383d41; }
    .status-deployed { background-color: #d4edda; color: #155724; }
    .status-onhold { background-color: #f8d7da; color: #721c24; }
    .sdlc-phase {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.25rem;
        background-color: #f8f9fa;
    }
    .sdlc-complete {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .sdlc-pending {
        background-color: #e2e3e5;
        border-left: 4px solid #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_projects():
    """Load projects data"""
    return pd.read_csv("data/projects.csv")

@st.cache_data
def load_requests():
    """Load requests data"""
    return pd.read_csv("data/requests.csv")

def save_projects(df):
    """Save projects data"""
    df.to_csv("data/projects.csv", index=False)
    st.cache_data.clear()

projects_df = load_projects()
requests_df = load_requests()

# Header
st.title("📁 Project Tracker")
st.markdown("Manage development projects with SDLC compliance")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 All Projects", "➕ New Project", "📊 Analytics"])

with tab1:
    st.subheader("Project Dashboard")

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        filter_status = st.multiselect(
            "Status",
            options=["Planning", "In Progress", "Testing", "Deployed", "On Hold"],
            default=["Planning", "In Progress", "Testing"]
        )

    with col2:
        search = st.text_input("Search projects", placeholder="Search by name or description...")

    # Apply filters
    filtered_df = projects_df[projects_df["Status"].isin(filter_status)]

    if search:
        filtered_df = filtered_df[
            filtered_df["Project Name"].str.contains(search, case=False, na=False) |
            filtered_df["Description"].str.contains(search, case=False, na=False)
        ]

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Projects", len(filtered_df))
    col2.metric("In Progress", len(filtered_df[filtered_df["Status"] == "In Progress"]))
    col3.metric("Testing", len(filtered_df[filtered_df["Status"] == "Testing"]))
    col4.metric("Deployed", len(projects_df[projects_df["Status"] == "Deployed"]))

    st.markdown("---")

    # Display projects
    if len(filtered_df) > 0:
        for _, proj in filtered_df.iterrows():
            with st.expander(f"**{proj['ID']}** - {proj['Project Name']}", expanded=False):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Description:** {proj['Description']}")
                    st.markdown(f"**Team Members:** {proj['Team Members']}")

                    # Show linked requests
                    if proj['Linked Requests']:
                        linked_ids = proj['Linked Requests'].split(",")
                        st.markdown(f"**Linked Requests ({len(linked_ids)}):**")
                        for req_id in linked_ids[:5]:  # Show first 5
                            req = requests_df[requests_df["ID"] == req_id.strip()]
                            if len(req) > 0:
                                st.markdown(f"- {req_id.strip()}: {req.iloc[0]['Title']}")

                with col2:
                    status_class = proj['Status'].lower().replace(" ", "")
                    st.markdown(
                        f'<span class="status-badge status-{status_class}">{proj["Status"]}</span>',
                        unsafe_allow_html=True
                    )

                    st.markdown(f"**Current Phase:** {proj['Current Phase']}")
                    st.markdown(f"**Start Date:** {proj['Start Date']}")
                    st.markdown(f"**Target Completion:** {proj['Target Completion']}")

                    if proj['Actual Completion']:
                        st.markdown(f"**Actual Completion:** {proj['Actual Completion']}")

                    # Calculate progress
                    target_date = pd.to_datetime(proj['Target Completion'])
                    days_until = (target_date - datetime.now()).days

                    if days_until < 0:
                        st.error(f"Overdue by {abs(days_until)} days")
                    elif days_until < 7:
                        st.warning(f"Due in {days_until} days")
                    else:
                        st.info(f"Due in {days_until} days")

                # SDLC Checklist
                st.markdown("---")
                st.markdown("**📋 SDLC Compliance Checklist**")

                # Parse SDLC checklist
                checklist = proj['SDLC Checklist'].split("|")

                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]

                for i, item in enumerate(checklist):
                    phase, status = item.split(":")
                    css_class = "sdlc-complete" if status == "Complete" else "sdlc-pending"
                    icon = "✓" if status == "Complete" else "○"

                    with cols[i % 3]:
                        st.markdown(
                            f'<div class="sdlc-phase {css_class}">'
                            f'{icon} <strong>{phase}</strong><br>'
                            f'<span style="font-size: 0.85rem;">{status}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                # Calculate completion percentage
                complete_count = sum(1 for item in checklist if ":Complete" in item)
                completion_pct = (complete_count / len(checklist)) * 100
                st.progress(completion_pct / 100)
                st.caption(f"SDLC Completion: {completion_pct:.0f}%")

                # Action buttons
                st.markdown("---")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("Move to Testing", key=f"test_{proj['ID']}"):
                        projects_df.loc[projects_df['ID'] == proj['ID'], 'Status'] = 'Testing'
                        projects_df.loc[projects_df['ID'] == proj['ID'], 'Current Phase'] = 'Testing & QA'
                        save_projects(projects_df)
                        st.success("Project moved to Testing!")
                        st.rerun()

                with col2:
                    if st.button("Mark as Deployed", key=f"dep_{proj['ID']}"):
                        projects_df.loc[projects_df['ID'] == proj['ID'], 'Status'] = 'Deployed'
                        projects_df.loc[projects_df['ID'] == proj['ID'], 'Actual Completion'] = datetime.now().strftime("%Y-%m-%d")
                        projects_df.loc[projects_df['ID'] == proj['ID'], 'Current Phase'] = 'Post-Deployment Review'
                        save_projects(projects_df)
                        st.success("Project deployed!")
                        st.rerun()

                with col3:
                    if st.button("Edit SDLC", key=f"sdlc_{proj['ID']}"):
                        st.info("SDLC editor available in Pro version")

    else:
        st.info("No projects match the selected filters.")

    # Export
    st.markdown("---")
    if st.button("📥 Export Projects to CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"projects_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with tab2:
    st.subheader("Create New Project")

    with st.form("new_project_form"):
        project_name = st.text_input("Project Name *", placeholder="e.g., Mobile Banking v3.0 Upgrade")
        description = st.text_area("Description *", placeholder="Detailed project description...", height=100)

        col1, col2, col3 = st.columns(3)

        with col1:
            start_date = st.date_input("Start Date *", value=datetime.now())

        with col2:
            target_date = st.date_input("Target Completion *", value=datetime.now() + timedelta(days=90))

        with col3:
            status = st.selectbox("Status *", ["Planning", "In Progress", "Testing", "Deployed", "On Hold"])

        team_members = st.text_input("Team Members *", placeholder="Alex Johnson, Maria Rodriguez")

        submitted = st.form_submit_button("Create Project")

        if submitted:
            if not all([project_name, description, team_members]):
                st.error("Please fill in all required fields (*)")
            else:
                # Generate new ID
                last_id = int(projects_df["ID"].str.replace("PROJ-", "").max())
                new_id = f"PROJ-{last_id + 1:03d}"

                # Create SDLC checklist
                sdlc_phases = [
                    "Requirements Gathering:Pending",
                    "Design & Architecture:Pending",
                    "Development:Pending",
                    "Testing & QA:Pending",
                    "Deployment:Pending",
                    "Post-Deployment Review:Pending"
                ]
                checklist_str = "|".join(sdlc_phases)

                # Create new project
                new_project = {
                    "ID": new_id,
                    "Project Name": project_name,
                    "Description": description,
                    "Status": status,
                    "Start Date": start_date.strftime("%Y-%m-%d"),
                    "Target Completion": target_date.strftime("%Y-%m-%d"),
                    "Actual Completion": "",
                    "Team Members": team_members,
                    "SDLC Checklist": checklist_str,
                    "Linked Requests": "",
                    "Current Phase": "Requirements Gathering"
                }

                # Add to dataframe
                new_df = pd.concat([projects_df, pd.DataFrame([new_project])], ignore_index=True)
                save_projects(new_df)

                st.success(f"✓ Project {new_id} created successfully!")
                st.balloons()

with tab3:
    st.subheader("Project Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Projects by Status**")
        status_counts = projects_df["Status"].value_counts()
        st.bar_chart(status_counts)

    with col2:
        st.markdown("**SDLC Completion Rate**")
        # Calculate average SDLC completion
        completion_rates = []
        for _, proj in projects_df.iterrows():
            checklist = proj['SDLC Checklist'].split("|")
            complete_count = sum(1 for item in checklist if ":Complete" in item)
            completion_pct = (complete_count / len(checklist)) * 100
            completion_rates.append(completion_pct)

        avg_completion = sum(completion_rates) / len(completion_rates)
        st.metric("Average SDLC Completion", f"{avg_completion:.1f}%")

        # Show breakdown
        for status in ["Planning", "In Progress", "Testing", "Deployed"]:
            status_projects = projects_df[projects_df["Status"] == status]
            if len(status_projects) > 0:
                status_completion = []
                for _, proj in status_projects.iterrows():
                    checklist = proj['SDLC Checklist'].split("|")
                    complete_count = sum(1 for item in checklist if ":Complete" in item)
                    completion_pct = (complete_count / len(checklist)) * 100
                    status_completion.append(completion_pct)
                avg = sum(status_completion) / len(status_completion)
                st.caption(f"{status}: {avg:.0f}% SDLC complete")

    st.markdown("---")

    # Timeline analysis
    st.markdown("**Project Timeline Analysis**")

    active_projects = projects_df[projects_df["Status"].isin(["Planning", "In Progress", "Testing"])]

    if len(active_projects) > 0:
        for _, proj in active_projects.iterrows():
            target = pd.to_datetime(proj['Target Completion'])
            days_until = (target - datetime.now()).days

            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(f"**{proj['Project Name']}**")
            col2.write(f"Due: {proj['Target Completion']}")

            if days_until < 0:
                col3.error(f"Overdue by {abs(days_until)} days")
            elif days_until < 7:
                col3.warning(f"{days_until} days left")
            else:
                col3.info(f"{days_until} days left")
    else:
        st.info("No active projects to analyze.")

# Footer
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("**DevOpsHub** — Powered by **AppForge Labs**")
with col2:
    if st.button("🚀 Upgrade to Pro"):
        st.info("Contact: paulsemaan007@gmail.com")
