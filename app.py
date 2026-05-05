import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Smart Health Inspection Platform",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# CUSTOM STYLE
# =========================
st.markdown("""
<style>
.main {
    background-color: #f9f5ef;
}
.title-box {
    background-color: #1a1a2e;
    padding: 30px;
    border-radius: 15px;
    color: white;
}
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #c0392b;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
.warning {
    background-color: #fde8e8;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #c0392b;
}
.success {
    background-color: #e8f7ee;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #2e7d32;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="title-box">
    <h1>🛡️ Smart Health Inspection Platform</h1>
    <p>
    A digital decision-support platform for public health inspectors covering
    water quality, cosmetic safety, hygiene evaluation, contamination investigation,
    and risk-based inspection planning.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# =========================
# SIDEBAR NAVIGATION
# =========================
st.sidebar.title("Platform Menu")

page = st.sidebar.radio(
    "Choose a module:",
    [
        "Dashboard",
        "New Inspection",
        "Water Quality Assessment",
        "Cosmetic Product Safety",
        "Hygiene Evaluation",
        "Risk Scoring",
        "Investigation Report",
        "Training Knowledge Base"
    ]
)

# =========================
# SAMPLE DATA
# =========================
inspection_data = pd.DataFrame({
    "Facility": [
        "Hotel Pool A",
        "Clinic Water Cooler",
        "Cosmetic Store B",
        "Restaurant Kitchen",
        "Spa Center C"
    ],
    "Facility Type": [
        "Swimming Pool",
        "Water Dispenser",
        "Cosmetics",
        "Food Facility",
        "Spa"
    ],
    "Risk Score": [85, 72, 64, 91, 58],
    "Status": [
        "Critical",
        "High",
        "Moderate",
        "Critical",
        "Moderate"
    ],
    "District": [
        "Dubai",
        "Sharjah",
        "Dubai",
        "Abu Dhabi",
        "Ajman"
    ]
})

# =========================
# DASHBOARD
# =========================
if page == "Dashboard":
    st.header("📊 Inspection Intelligence Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Inspections", len(inspection_data))

    with col2:
        st.metric("Critical Facilities", len(inspection_data[inspection_data["Status"] == "Critical"]))

    with col3:
        st.metric("Average Risk Score", round(inspection_data["Risk Score"].mean(), 1))

    with col4:
        st.metric("High-Risk Threshold", "≥ 70")

    st.write("")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Risk Score by Facility")
        fig = px.bar(
            inspection_data,
            x="Facility",
            y="Risk Score",
            color="Status",
            text="Risk Score",
            title="Facility Risk Overview"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Inspection Status Distribution")
        fig2 = px.pie(
            inspection_data,
            names="Status",
            title="Risk Category Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Inspection Records")
    st.dataframe(inspection_data, use_container_width=True)

# =========================
# NEW INSPECTION FORM
# =========================
elif page == "New Inspection":
    st.header("📝 New Health Inspection Record")

    with st.form("inspection_form"):
        facility_name = st.text_input("Facility Name")
        facility_type = st.selectbox(
            "Facility Type",
            [
                "Drinking Water System",
                "Swimming Pool",
                "Water Dispenser",
                "Cosmetic Product",
                "Cosmetic Manufacturing Facility",
                "Restaurant / Kitchen",
                "Healthcare Facility",
                "Spa / Salon"
            ]
        )

        location = st.text_input("Location / District")
        inspector_name = st.text_input("Inspector Name")
        inspection_date = st.date_input("Inspection Date", date.today())

        observations = st.text_area("Field Observations")

        photo_evidence = st.file_uploader(
            "Upload Photo Evidence",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button("Save Inspection")

    if submitted:
        st.success("Inspection record saved successfully.")
        st.write("### Summary")
        st.write(f"**Facility:** {facility_name}")
        st.write(f"**Type:** {facility_type}")
        st.write(f"**Location:** {location}")
        st.write(f"**Inspector:** {inspector_name}")
        st.write(f"**Date:** {inspection_date}")
        st.write(f"**Observations:** {observations}")

        if photo_evidence:
            st.image(photo_evidence, caption="Uploaded Evidence", use_container_width=True)

# =========================
# WATER QUALITY ASSESSMENT
# =========================
elif page == "Water Quality Assessment":
    st.header("💧 Water Quality Assessment")

    st.info(
        "This module evaluates physical, chemical, and microbiological indicators "
        "for drinking water, swimming pools, and water dispensers."
    )

    water_type = st.selectbox(
        "Water System Type",
        ["Drinking Water", "Swimming Pool", "Water Dispenser / Cooler"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        ph = st.number_input("pH Value", min_value=0.0, max_value=14.0, value=7.2)

    with col2:
        chlorine = st.number_input("Residual / Free Chlorine mg/L", min_value=0.0, value=0.3)

    with col3:
        turbidity = st.number_input("Turbidity NTU", min_value=0.0, value=1.0)

    ecoli = st.selectbox("E. coli Detected?", ["No", "Yes"])
    legionella = st.selectbox("Legionella Detected?", ["No", "Yes"])
    biofilm = st.selectbox("Visible Biofilm?", ["No", "Yes"])
    maintenance_gap = st.selectbox("Maintenance Log Gap?", ["No", "Yes"])

    st.subheader("Assessment Result")

    risk_points = 0
    alerts = []

    if water_type == "Swimming Pool":
        if ph < 7.2 or ph > 7.8:
            risk_points += 20
            alerts.append("Pool pH is outside the recommended range of 7.2–7.8.")

        if chlorine < 1 or chlorine > 3:
            risk_points += 25
            alerts.append("Pool free chlorine is outside the recommended range of 1–3 mg/L.")

    else:
        if ph < 6.5 or ph > 8.5:
            risk_points += 15
            alerts.append("Drinking water pH is outside the typical acceptable range.")

        if chlorine < 0.2:
            risk_points += 20
            alerts.append("Residual chlorine is low. Investigate possible disinfection failure.")

    if ecoli == "Yes":
        risk_points += 50
        alerts.append("E. coli detected. Immediate closure and re-testing are required.")

    if legionella == "Yes":
        risk_points += 50
        alerts.append("Legionella detected. Immediate water risk management action is required.")

    if biofilm == "Yes":
        risk_points += 20
        alerts.append("Biofilm detected. Sanitation and internal cleaning are required.")

    if maintenance_gap == "Yes":
        risk_points += 15
        alerts.append("Maintenance documentation gap detected.")

    if risk_points >= 70:
        st.markdown("""
        <div class="warning">
        <h3>🚨 Critical Risk</h3>
        <p>Immediate corrective action is required. Consider temporary closure until corrective actions and re-testing are completed.</p>
        </div>
        """, unsafe_allow_html=True)

    elif risk_points >= 40:
        st.warning("High risk. Corrective action is required within a defined deadline.")

    elif risk_points >= 20:
        st.info("Moderate risk. Monitor and request improvement plan.")

    else:
        st.markdown("""
        <div class="success">
        <h3>✅ Low Risk</h3>
        <p>No critical issue detected based on entered values.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("### Risk Score:", risk_points)

    if alerts:
        st.write("### Alerts")
        for alert in alerts:
            st.write(f"- {alert}")

# =========================
# COSMETIC PRODUCT SAFETY
# =========================
elif page == "Cosmetic Product Safety":
    st.header("🧴 Cosmetic Product Safety Assessment")

    st.info(
        "This module supports inspection of cosmetic products and facilities "
        "using GMP, ingredient compliance, microbial safety, and storage control."
    )

    product_name = st.text_input("Product Name")
    batch_number = st.text_input("Batch Number")
    manufacturer = st.text_input("Manufacturer")

    iso_gmp = st.selectbox("ISO 22716 / GMP Documentation Available?", ["Yes", "No"])
    ingredient_compliance = st.selectbox("Ingredients within permitted limits?", ["Yes", "No"])
    banned_substances = st.selectbox("Banned or restricted substance detected?", ["No", "Yes"])
    microbial_test = st.selectbox("Microbiological test passed?", ["Yes", "No"])
    storage_ok = st.selectbox("Storage and transport conditions acceptable?", ["Yes", "No"])
    labeling_ok = st.selectbox("Labeling complete and clear?", ["Yes", "No"])

    cosmetic_risk = 0

    if iso_gmp == "No":
        cosmetic_risk += 20
    if ingredient_compliance == "No":
        cosmetic_risk += 30
    if banned_substances == "Yes":
        cosmetic_risk += 50
    if microbial_test == "No":
        cosmetic_risk += 40
    if storage_ok == "No":
        cosmetic_risk += 20
    if labeling_ok == "No":
        cosmetic_risk += 10

    st.subheader("Cosmetic Safety Decision")

    if cosmetic_risk >= 70:
        st.error("Critical product risk. Recommend product hold, recall review, or enforcement action.")
    elif cosmetic_risk >= 40:
        st.warning("High risk. Corrective action and documentation review required.")
    elif cosmetic_risk >= 20:
        st.info("Moderate risk. Request improvement and monitor compliance.")
    else:
        st.success("Low risk. Product appears compliant based on entered data.")

    st.write("### Cosmetic Risk Score:", cosmetic_risk)

# =========================
# HYGIENE EVALUATION
# =========================
elif page == "Hygiene Evaluation":
    st.header("🧼 Hygiene and Disinfection Program Evaluation")

    cleaning_schedule = st.selectbox("Cleaning schedule available?", ["Yes", "No"])
    chemical_labeling = st.selectbox("Chemicals correctly labeled?", ["Yes", "No"])
    dilution_control = st.selectbox("Correct chemical dilution followed?", ["Yes", "No"])
    ppe_available = st.selectbox("PPE available and used?", ["Yes", "No"])
    waste_management = st.selectbox("Biological waste managed correctly?", ["Yes", "No"])
    surface_swab = st.selectbox("Surface swab result acceptable?", ["Yes", "No", "Not Tested"])

    hygiene_score = 100

    if cleaning_schedule == "No":
        hygiene_score -= 15
    if chemical_labeling == "No":
        hygiene_score -= 15
    if dilution_control == "No":
        hygiene_score -= 20
    if ppe_available == "No":
        hygiene_score -= 15
    if waste_management == "No":
        hygiene_score -= 20
    if surface_swab == "No":
        hygiene_score -= 30
    if surface_swab == "Not Tested":
        hygiene_score -= 10

    st.subheader("Hygiene Program Score")
    st.progress(max(hygiene_score, 0) / 100)
    st.write(f"### Score: {max(hygiene_score, 0)} / 100")

    if hygiene_score >= 80:
        st.success("Good hygiene program.")
    elif hygiene_score >= 60:
        st.warning("Needs improvement.")
    else:
        st.error("Poor hygiene control. Immediate corrective action required.")

# =========================
# RISK SCORING
# =========================
elif page == "Risk Scoring":
    st.header("⚠️ Risk-Based Inspection Scoring")

    st.write(
        "Use this tool to prioritize facilities for inspection based on public health risk."
    )

    violation_history = st.slider("Previous Violations", 0, 10, 3)
    vulnerable_population = st.selectbox(
        "Serves vulnerable population?",
        ["No", "Yes"]
    )
    complaint_count = st.slider("Recent Complaints", 0, 20, 2)
    lab_failure = st.selectbox("Recent Laboratory Failure?", ["No", "Yes"])
    documentation_quality = st.slider("Documentation Quality", 0, 10, 6)
    facility_complexity = st.slider("Facility Complexity", 0, 10, 5)

    risk_score = 0
    risk_score += violation_history * 5
    risk_score += complaint_count * 2
    risk_score += facility_complexity * 3
    risk_score += (10 - documentation_quality) * 3

    if vulnerable_population == "Yes":
        risk_score += 20

    if lab_failure == "Yes":
        risk_score += 30

    st.write("### Total Risk Score:", risk_score)

    if risk_score >= 80:
        st.error("Priority Level: Critical — Immediate inspection required.")
    elif risk_score >= 60:
        st.warning("Priority Level: High — Schedule inspection soon.")
    elif risk_score >= 40:
        st.info("Priority Level: Moderate — Routine follow-up.")
    else:
        st.success("Priority Level: Low — Standard inspection cycle.")

# =========================
# INVESTIGATION REPORT
# =========================
elif page == "Investigation Report":
    st.header("📄 Contamination Investigation Report Generator")

    facility = st.text_input("Facility Name")
    incident_type = st.selectbox(
        "Incident Type",
        [
            "E. coli Detection",
            "Legionella Detection",
            "Chemical Contamination",
            "Cosmetic Product Failure",
            "Hygiene Program Failure",
            "Repeated Non-Compliance"
        ]
    )

    finding = st.text_area("Confirmed Finding")
    suspected_source = st.text_area("Suspected Source")
    sampling_points = st.text_area("Sampling Points")
    corrective_action = st.text_area("Corrective Actions Required")
    deadline = st.date_input("Correction Deadline")
    inspector = st.text_input("Inspector Name")

    if st.button("Generate Report"):
        report = f"""
        HEALTH INSPECTION INVESTIGATION REPORT

        Facility Name: {facility}
        Incident Type: {incident_type}
        Inspector: {inspector}
        Report Date: {date.today()}

        1. Confirmed Finding
        {finding}

        2. Suspected Source
        {suspected_source}

        3. Sampling Points
        {sampling_points}

        4. Required Corrective Actions
        {corrective_action}

        5. Correction Deadline
        {deadline}

        6. Recommended Follow-Up
        - Verify corrective action implementation.
        - Conduct re-sampling after remediation.
        - Review maintenance and hygiene records.
        - Maintain full documentation for legal and regulatory traceability.
        """

        st.text_area("Generated Report", report, height=400)

        st.download_button(
            label="Download Report as TXT",
            data=report,
            file_name="health_inspection_report.txt",
            mime="text/plain"
        )

# =========================
# TRAINING KNOWLEDGE BASE
# =========================
elif page == "Training Knowledge Base":
    st.header("📚 Inspector Training Knowledge Base")

    topic = st.selectbox(
        "Select Topic",
        [
            "Water Safety Standards",
            "Cosmetic GMP",
            "Biological Indicators",
            "Field Investigation",
            "Hygiene Evaluation",
            "Digital Inspection Transformation"
        ]
    )

    knowledge = {
        "Water Safety Standards": """
        Water inspection should evaluate physical, chemical, and microbiological indicators.
        Key parameters include pH, chlorine, turbidity, E. coli, Legionella, and maintenance records.
        E. coli should be absent in 100 mL of drinking water.
        """,

        "Cosmetic GMP": """
        Cosmetic inspection should assess ingredient compliance, microbiological safety,
        GMP documentation, storage conditions, labeling, and batch traceability.
        ISO 22716 is a major reference for cosmetic Good Manufacturing Practice.
        """,

        "Biological Indicators": """
        Biological indicators such as E. coli, Legionella, Pseudomonas, yeast, mold,
        and total aerobic microbial count help detect contamination before harm occurs.
        """,

        "Field Investigation": """
        A strong contamination investigation follows five steps:
        verify the report, conduct field survey, collect multi-point samples,
        perform root cause analysis, and verify corrective action.
        """,

        "Hygiene Evaluation": """
        Hygiene programs should be verified through cleaning records, chemical handling checks,
        PPE use, waste management assessment, and microbiological surface swabbing.
        """,

        "Digital Inspection Transformation": """
        Digital inspection platforms support mobile checklists, photo evidence,
        GPS-stamped inspection records, dashboards, automated reports,
        and risk-based inspection planning.
        """
    }

    st.info(knowledge[topic])

    st.subheader("Mini Quiz")

    answer = st.radio(
        "Which result requires immediate closure and re-testing?",
        [
            "Low turbidity",
            "E. coli detection",
            "Complete maintenance log",
            "Acceptable pH"
        ]
    )

    if st.button("Check Answer"):
        if answer == "E. coli detection":
            st.success("Correct. E. coli detection requires immediate corrective action and re-testing.")
        else:
            st.error("Incorrect. The correct answer is E. coli detection.")