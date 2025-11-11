"""
Errors Page - Monitor system errors and triage decisions
"""
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Errors - DevOpsHub", page_icon="⚠️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .severity-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .severity-low { background-color: #d4edda; color: #155724; }
    .severity-medium { background-color: #fff3cd; color: #856404; }
    .severity-high { background-color: #fff3cd; color: #fd7e14; }
    .severity-critical { background-color: #f8d7da; color: #721c24; }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
    }
    .status-new { background-color: #d1ecf1; color: #0c5460; }
    .status-investigating { background-color: #fff3cd; color: #856404; }
    .status-fixed { background-color: #d4edda; color: #155724; }
    .status-reportedtofiserv { background-color: #e2e3e5; color: #383d41; }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_errors():
    """Load errors data"""
    return pd.read_csv("data/errors.csv")

def save_errors(df):
    """Save errors data"""
    df.to_csv("data/errors.csv", index=False)
    st.cache_data.clear()

errors_df = load_errors()

# Header
st.title("⚠️ Error Monitor")
st.markdown("Track Datasafe/Keystone system errors and triage decisions")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 All Errors", "➕ Log New Error", "📊 Analytics"])

with tab1:
    st.subheader("Error Dashboard")

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        filter_status = st.multiselect(
            "Status",
            options=["New", "Investigating", "Fixed", "Reported to Fiserv"],
            default=["New", "Investigating"]
        )

    with col2:
        filter_severity = st.multiselect(
            "Severity",
            options=["Low", "Medium", "High", "Critical"],
            default=["Low", "Medium", "High", "Critical"]
        )

    with col3:
        filter_system = st.multiselect(
            "System",
            options=errors_df["System"].unique().tolist(),
            default=errors_df["System"].unique().tolist()
        )

    with col4:
        filter_fiserv = st.selectbox(
            "Reported to Fiserv",
            options=["All", "Yes", "No"],
            index=0
        )

    # Apply filters
    filtered_df = errors_df[
        (errors_df["Status"].isin(filter_status)) &
        (errors_df["Severity"].isin(filter_severity)) &
        (errors_df["System"].isin(filter_system))
    ]

    if filter_fiserv != "All":
        filtered_df = filtered_df[filtered_df["Reported to Fiserv"] == filter_fiserv]

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Errors", len(filtered_df))
    col2.metric("Critical/High", len(filtered_df[filtered_df["Severity"].isin(["High", "Critical"])]))
    col3.metric("Open", len(filtered_df[filtered_df["Status"].isin(["New", "Investigating"])]))
    col4.metric("Escalated to Fiserv", len(filtered_df[filtered_df["Reported to Fiserv"] == "Yes"]))

    st.markdown("---")

    # Display errors
    if len(filtered_df) > 0:
        # Sort by severity and date
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        filtered_df["Severity_Sort"] = filtered_df["Severity"].map(severity_order)
        filtered_df = filtered_df.sort_values(["Severity_Sort", "Date Reported"], ascending=[True, False])

        for _, error in filtered_df.iterrows():
            with st.expander(f"**{error['ID']}** - {error['Error Code']}: {error['Description'][:100]}...", expanded=False):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Full Description:** {error['Description']}")

                    if error['Resolution Notes']:
                        st.markdown(f"**Resolution Notes:**")
                        st.info(error['Resolution Notes'])

                with col2:
                    severity_class = error['Severity'].lower()
                    status_class = error['Status'].lower().replace(" ", "")

                    st.markdown(
                        f'<span class="severity-badge severity-{severity_class}">{error["Severity"]}</span> '
                        f'<span class="status-badge status-{status_class}">{error["Status"]}</span>',
                        unsafe_allow_html=True
                    )

                    st.markdown(f"**System:** {error['System']}")
                    st.markdown(f"**Error Code:** {error['Error Code']}")
                    st.markdown(f"**Reported:** {error['Date Reported']}")

                    if error['Date Resolved']:
                        st.markdown(f"**Resolved:** {error['Date Resolved']}")
                        days_to_resolve = (pd.to_datetime(error['Date Resolved']) - pd.to_datetime(error['Date Reported'])).days
                        st.markdown(f"**Resolution Time:** {days_to_resolve} days")

                    if error['Reported to Fiserv'] == "Yes":
                        st.markdown(f"**Fiserv Ticket:** {error['Fiserv Ticket']}")

                # Action buttons
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button("Mark as Investigating", key=f"inv_{error['ID']}"):
                        errors_df.loc[errors_df['ID'] == error['ID'], 'Status'] = 'Investigating'
                        save_errors(errors_df)
                        st.success("Status updated!")
                        st.rerun()

                with col2:
                    if st.button("Mark as Fixed", key=f"fix_{error['ID']}"):
                        errors_df.loc[errors_df['ID'] == error['ID'], 'Status'] = 'Fixed'
                        errors_df.loc[errors_df['ID'] == error['ID'], 'Date Resolved'] = datetime.now().strftime("%Y-%m-%d")
                        save_errors(errors_df)
                        st.success("Error marked as fixed!")
                        st.rerun()

                with col3:
                    if st.button("Report to Fiserv", key=f"fis_{error['ID']}"):
                        errors_df.loc[errors_df['ID'] == error['ID'], 'Status'] = 'Reported to Fiserv'
                        errors_df.loc[errors_df['ID'] == error['ID'], 'Reported to Fiserv'] = 'Yes'
                        errors_df.loc[errors_df['ID'] == error['ID'], 'Fiserv Ticket'] = f"FSV-2024-{len(errors_df) + 2000}"
                        save_errors(errors_df)
                        st.success("Escalated to Fiserv!")
                        st.rerun()

                with col4:
                    if st.button("Add Notes", key=f"note_{error['ID']}"):
                        st.info("Notes editor available in Pro version")

    else:
        st.info("No errors match the selected filters.")

    # Export
    st.markdown("---")
    if st.button("📥 Export Filtered Errors to CSV"):
        csv = filtered_df.drop("Severity_Sort", axis=1, errors='ignore').to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"errors_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with tab2:
    st.subheader("Log New Error")

    with st.form("new_error_form"):
        col1, col2 = st.columns(2)

        with col1:
            error_code = st.text_input("Error Code *", placeholder="e.g., ERR-BATCH-001")
            system = st.selectbox("System *", ["Datasafe", "Keystone", "Custom Integration"])
            severity = st.selectbox("Severity *", ["Low", "Medium", "High", "Critical"])

        with col2:
            description = st.text_area("Description *", placeholder="Detailed error description...", height=100)

        submitted = st.form_submit_button("Log Error")

        if submitted:
            if not all([error_code, description]):
                st.error("Please fill in all required fields (*)")
            else:
                # Generate new ID
                last_id = int(errors_df["ID"].str.replace("ERR-", "").max())
                new_id = f"ERR-{last_id + 1:03d}"

                # Create new error
                new_error = {
                    "ID": new_id,
                    "Error Code": error_code,
                    "System": system,
                    "Severity": severity,
                    "Description": description,
                    "Status": "New",
                    "Resolution Notes": "",
                    "Date Reported": datetime.now().strftime("%Y-%m-%d"),
                    "Date Resolved": "",
                    "Reported to Fiserv": "No",
                    "Fiserv Ticket": ""
                }

                # Add to dataframe
                new_df = pd.concat([errors_df, pd.DataFrame([new_error])], ignore_index=True)
                save_errors(new_df)

                st.success(f"✓ Error {new_id} logged successfully!")
                st.balloons()

with tab3:
    st.subheader("Error Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Errors by System**")
        system_counts = errors_df["System"].value_counts()
        st.bar_chart(system_counts)

    with col2:
        st.markdown("**Escalation Rate**")
        total = len(errors_df)
        escalated = len(errors_df[errors_df["Reported to Fiserv"] == "Yes"])
        fixed_internal = len(errors_df[errors_df["Status"] == "Fixed"])

        st.metric("Total Errors", total)
        st.metric("Fixed Internally", fixed_internal, f"{fixed_internal/total*100:.1f}%")
        st.metric("Escalated to Fiserv", escalated, f"{escalated/total*100:.1f}%")

    st.markdown("---")

    # Resolution time analysis
    st.markdown("**Average Resolution Time by Severity**")
    resolved = errors_df[errors_df["Date Resolved"] != ""].copy()
    if len(resolved) > 0:
        resolved["Date Reported"] = pd.to_datetime(resolved["Date Reported"])
        resolved["Date Resolved"] = pd.to_datetime(resolved["Date Resolved"])
        resolved["Resolution Days"] = (resolved["Date Resolved"] - resolved["Date Reported"]).dt.days

        avg_by_severity = resolved.groupby("Severity")["Resolution Days"].mean().reindex(["Low", "Medium", "High", "Critical"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Low", f"{avg_by_severity['Low']:.1f} days")
        col2.metric("Medium", f"{avg_by_severity['Medium']:.1f} days")
        col3.metric("High", f"{avg_by_severity['High']:.1f} days")
        col4.metric("Critical", f"{avg_by_severity['Critical']:.1f} days")
    else:
        st.info("No resolved errors to analyze yet.")

# Footer
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("**DevOpsHub** — Powered by **AppForge Labs**")
with col2:
    if st.button("🚀 Upgrade to Pro"):
        st.info("Contact: paulsemaan007@gmail.com")
