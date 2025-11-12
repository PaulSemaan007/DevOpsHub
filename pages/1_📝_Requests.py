"""
Requests Page - Track programming requests, SQL queries, and reports
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Requests - DevOpsHub", page_icon="📝", layout="wide")

# Custom CSS - DevOps Tech Theme
st.markdown("""
<style>
    /* DevOps Tech Theme - Consistent with main app */
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 0.3rem;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .status-completed { background-color: #27ae60; color: white; }
    .status-inprogress { background-color: #f39c12; color: white; }
    .status-submitted { background-color: #3498db; color: white; }
    .status-testing { background-color: #95a5a6; color: white; }
    .priority-critical { background-color: #e74c3c; color: white; }
    .priority-high { background-color: #e67e22; color: white; }
    .priority-medium { background-color: #3498db; color: white; }
    .priority-low { background-color: #1abc9c; color: white; }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
    }
    [data-testid="stSidebar"] * {
        color: #ecf0f1 !important;
    }
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_requests():
    """Load requests data"""
    return pd.read_csv("data/requests.csv")

def save_requests(df):
    """Save requests data"""
    df.to_csv("data/requests.csv", index=False)
    st.cache_data.clear()

requests_df = load_requests()

# Header
st.title("📝 Request Tracker")
st.markdown("Track custom programming requests, SQL queries, reports, and scripts")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 All Requests", "➕ New Request", "📊 Analytics"])

with tab1:
    st.subheader("All Requests")

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        filter_status = st.multiselect(
            "Status",
            options=["Submitted", "In Progress", "Testing", "Completed"],
            default=["Submitted", "In Progress", "Testing"]
        )

    with col2:
        filter_type = st.multiselect(
            "Type",
            options=requests_df["Type"].unique().tolist(),
            default=requests_df["Type"].unique().tolist()
        )

    with col3:
        filter_priority = st.multiselect(
            "Priority",
            options=["Low", "Medium", "High", "Critical"],
            default=["Low", "Medium", "High", "Critical"]
        )

    with col4:
        filter_assignee = st.multiselect(
            "Assigned To",
            options=requests_df["Assigned To"].unique().tolist(),
            default=requests_df["Assigned To"].unique().tolist()
        )

    # Apply filters
    filtered_df = requests_df[
        (requests_df["Status"].isin(filter_status)) &
        (requests_df["Type"].isin(filter_type)) &
        (requests_df["Priority"].isin(filter_priority)) &
        (requests_df["Assigned To"].isin(filter_assignee))
    ]

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Requests", len(filtered_df))
    col2.metric("High/Critical", len(filtered_df[filtered_df["Priority"].isin(["High", "Critical"])]))
    col3.metric("Unassigned", len(filtered_df[filtered_df["Assigned To"] == "Unassigned"]))
    col4.metric("Overdue", len(filtered_df[pd.to_datetime(filtered_df["Due Date"]) < datetime.now()]))

    st.markdown("---")

    # Display requests
    if len(filtered_df) > 0:
        # Sort by created date descending
        filtered_df = filtered_df.sort_values("Created Date", ascending=False)

        for _, req in filtered_df.iterrows():
            with st.expander(f"**{req['ID']}** - {req['Title']}", expanded=False):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Description:** {req['Description']}")
                    st.markdown(f"**Requester:** {req['Requester Name']} ({req['Requester Department']})")
                    st.markdown(f"**Email:** {req['Requester Email']}")
                    if req['Related Project']:
                        st.markdown(f"**Related Project:** {req['Related Project']}")

                with col2:
                    status_class = req['Status'].lower().replace(" ", "")
                    priority_class = req['Priority'].lower()

                    st.markdown(
                        f'<span class="status-badge status-{status_class}">{req["Status"]}</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<span class="status-badge priority-{priority_class}">{req["Priority"]} Priority</span>',
                        unsafe_allow_html=True
                    )

                    st.markdown(f"**Type:** {req['Type']}")
                    st.markdown(f"**Technology:** {req['Technology']}")
                    st.markdown(f"**Assigned To:** {req['Assigned To']}")
                    st.markdown(f"**Created:** {req['Created Date']}")
                    st.markdown(f"**Due Date:** {req['Due Date']}")
                    if req['Completed Date']:
                        st.markdown(f"**Completed:** {req['Completed Date']}")

                # Edit section (simplified for demo)
                st.markdown("---")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(f"Mark as In Progress", key=f"prog_{req['ID']}"):
                        requests_df.loc[requests_df['ID'] == req['ID'], 'Status'] = 'In Progress'
                        save_requests(requests_df)
                        st.success("Status updated!")
                        st.rerun()

                with col2:
                    if st.button(f"Mark as Completed", key=f"comp_{req['ID']}"):
                        requests_df.loc[requests_df['ID'] == req['ID'], 'Status'] = 'Completed'
                        requests_df.loc[requests_df['ID'] == req['ID'], 'Completed Date'] = datetime.now().strftime("%Y-%m-%d")
                        save_requests(requests_df)
                        st.success("Request completed!")
                        st.rerun()

                with col3:
                    if st.button(f"Export Details", key=f"exp_{req['ID']}"):
                        st.info("Export feature available in Pro version")
    else:
        st.info("No requests match the selected filters.")

    # Export all
    st.markdown("---")
    if st.button("📥 Export Filtered Requests to CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"requests_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with tab2:
    st.subheader("Create New Request")

    with st.form("new_request_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Request Title *", placeholder="e.g., Monthly Loan Portfolio Report")
            req_type = st.selectbox("Type *", ["Custom Program", "SQL Query", "Report", "Script"])
            priority = st.selectbox("Priority *", ["Low", "Medium", "High", "Critical"])
            technology = st.selectbox("Technology", ["Intersystems Cache", "Microsoft .NET", "Python", "PowerShell", "MS SQL", "JavaScript", "HTML"])

        with col2:
            requester_name = st.text_input("Your Name *", placeholder="John Smith")
            requester_email = st.text_input("Your Email *", placeholder="jsmith@lbsfinancial.org")
            requester_dept = st.text_input("Department *", placeholder="Loan Operations")
            due_date = st.date_input("Due Date *", value=datetime.now() + timedelta(days=14))

        description = st.text_area("Description *", placeholder="Detailed description of the request...", height=150)

        submitted = st.form_submit_button("Submit Request")

        if submitted:
            if not all([title, requester_name, requester_email, requester_dept, description]):
                st.error("Please fill in all required fields (*)")
            else:
                # Generate new ID
                last_id = int(requests_df["ID"].str.replace("REQ-", "").max())
                new_id = f"REQ-{last_id + 1:03d}"

                # Create new request
                new_request = {
                    "ID": new_id,
                    "Title": title,
                    "Description": description,
                    "Type": req_type,
                    "Priority": priority,
                    "Status": "Submitted",
                    "Requester Name": requester_name,
                    "Requester Email": requester_email,
                    "Requester Department": requester_dept,
                    "Assigned To": "Unassigned",
                    "Created Date": datetime.now().strftime("%Y-%m-%d"),
                    "Due Date": due_date.strftime("%Y-%m-%d"),
                    "Completed Date": "",
                    "Technology": technology,
                    "Related Project": ""
                }

                # Add to dataframe
                new_df = pd.concat([requests_df, pd.DataFrame([new_request])], ignore_index=True)
                save_requests(new_df)

                st.success(f"✓ Request {new_id} created successfully!")
                st.balloons()

with tab3:
    st.subheader("Request Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Requests by Requester Department**")
        dept_counts = requests_df["Requester Department"].value_counts().head(10)
        st.bar_chart(dept_counts)

    with col2:
        st.markdown("**Requests by Technology**")
        tech_counts = requests_df["Technology"].value_counts()
        st.bar_chart(tech_counts)

    st.markdown("---")

    # Completion rate over time
    st.markdown("**Completion Rate Trend**")
    completed = requests_df[requests_df["Status"] == "Completed"].copy()
    if len(completed) > 0:
        completed["Completed Date"] = pd.to_datetime(completed["Completed Date"])
        completed["Month"] = completed["Completed Date"].dt.to_period("M").astype(str)
        monthly_counts = completed.groupby("Month").size()
        st.line_chart(monthly_counts)
    else:
        st.info("No completed requests to analyze yet.")

# Footer
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("**DevOpsHub** — Powered by **AppForge Labs**")
with col2:
    if st.button("🚀 Upgrade to Pro"):
        st.info("Contact: paulsemaan007@gmail.com")
