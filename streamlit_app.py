import json
import streamlit as st

from graph.state import GrantState
from graph.workflow import graph

st.set_page_config(
    page_title="GrantGuard",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ GrantGuard")
st.caption("Multi-Agent AI Grant Review System")

# -----------------------------------------------------
# Default Sample Application
# -----------------------------------------------------

default_application = {
    "organization": "Helping Hands Foundation",
    "registration_number": "NGO/2018/45821",
    "year_established": 2018,
    "years_operating": 8,

    "contact_person": "Anita Sharma",
    "designation": "Executive Director",
    "email": "info@helpinghands.org",
    "phone": "+91-9876543210",

    "project_title": "Community Health & Nutrition Initiative",
    "grant_category": "Healthcare",

    # Keep below medium NGO threshold
    "requested_amount": 1400000,

    "project_description": """
Project Objectives
Improve access to primary healthcare for underserved rural communities through
preventive healthcare, maternal health awareness, child nutrition monitoring,
and regular medical outreach.

Community Problem
The five target villages have limited access to qualified healthcare
professionals, increasing cases of preventable illness and poor maternal and
child health outcomes.

Implementation Strategy
The organization will conduct monthly medical camps, distribute essential
medicines, organize nutrition awareness sessions, train 40 community health
volunteers, and coordinate with local government health workers.

Timeline
The project will run for 12 months with monthly milestones, quarterly reviews,
and a final impact .

Beneficiaries
Approximately 2,500 direct beneficiaries, including women, children, and
elderly residents across five rural villages.

Monitoring and Evaluation
Progress will be monitored through monthly reports, attendance records,
beneficiary surveys, health screening data, financial tracking, and quarterly
review meetings.

Expected Outcomes
• 2,500 beneficiaries receive healthcare services.
• 40 trained community health volunteers.
• Increased maternal and child health awareness.
• Improved nutrition screening coverage.
• Improved access to preventive healthcare.

Sustainability
After grant completion, trained volunteers will continue awareness campaigns
with support from the District Health Department and local primary health
centres. Educational materials developed during the project will remain with
community organizations.

Partnerships
Implementation will be carried out in partnership with the District Health
Department, local Primary Health Centres, village councils, and two community
NGOs that will assist with beneficiary mobilization and volunteer coordination.
""",

    "beneficiaries": 2500,

    "timeline": "12 months",

    "budget": {
        "medical_camps": 500000,
        "medicines_supplies": 280000,
        "training_workshops": 180000,
        "travel_logistics": 160000,
        "administration": 180000,
        "contingency": 100000,
    },

    "documents": [
        "Grant Proposal",
        "Registration Certificate",
        "Budget",
        "Project Timeline",
        "Bank Statement (Last 6 Months)",
        "Bank Details",
        "Beneficiary Information",
        "PAN Card",
        "Audited Financial Statements (Last 3 Years)",
        "Board Resolution",
        "Annual Report 2025",
        "Letters of Partnership",
    ],

    "declaration_signed": True,
}

# -----------------------------------------------------
# Input
# -----------------------------------------------------

st.subheader("Grant Application")

if "application" not in st.session_state:
    st.session_state.application = default_application.copy()

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("📄 Load Sample Application"):
        st.session_state.application = default_application.copy()
        st.rerun()

app = st.session_state.application

with st.form("grant_form"):

    st.markdown("## Organization Information")

    organization = st.text_input(
        "Organization Name",
        value=app["organization"]
    )

    registration_number = st.text_input(
        "Registration Number",
        value=app["registration_number"]
    )

    col1, col2 = st.columns(2)

    with col1:
        year_established = st.number_input(
            "Year Established",
            value=app["year_established"],
            step=1
        )

    with col2:
        years_operating = st.number_input(
            "Years Operating",
            value=app["years_operating"],
            step=1
        )

    st.divider()

    st.markdown("## Contact Information")

    contact_person = st.text_input(
        "Contact Person",
        value=app["contact_person"]
    )

    designation = st.text_input(
        "Designation",
        value=app["designation"]
    )

    email = st.text_input(
        "Email",
        value=app["email"]
    )

    phone = st.text_input(
        "Phone",
        value=app["phone"]
    )

    st.divider()

    st.markdown("## Project Information")

    project_title = st.text_input(
        "Project Title",
        value=app["project_title"]
    )

    grant_category = st.selectbox(
        "Grant Category",
        [
            "Healthcare",
            "Education",
            "Environment",
            "Women Empowerment",
            "Agriculture",
            "Sports",
            "Technology",
        ],
        index=[
            "Healthcare",
            "Education",
            "Environment",
            "Women Empowerment",
            "Agriculture",
            "Sports",
            "Technology",
        ].index(app["grant_category"])
    )

    requested_amount = st.number_input(
        "Requested Amount",
        value=app["requested_amount"],
        step=10000
    )

    beneficiaries = st.number_input(
        "Beneficiaries",
        value=app["beneficiaries"],
        step=1
    )

    timeline = st.text_input(
        "Timeline",
        value=app["timeline"]
    )

    project_description = st.text_area(
        "Project Description",
        value=app["project_description"],
        height=300
    )

    st.divider()

    st.markdown("## Budget")

    budget = app["budget"]

    medical_camps = st.number_input(
        "Medical Camps",
        value=budget["medical_camps"]
    )

    medicines_supplies = st.number_input(
        "Medicines & Supplies",
        value=budget["medicines_supplies"]
    )

    training_workshops = st.number_input(
        "Training Workshops",
        value=budget["training_workshops"]
    )

    travel_logistics = st.number_input(
        "Travel & Logistics",
        value=budget["travel_logistics"]
    )

    administration = st.number_input(
        "Administration",
        value=budget["administration"]
    )

    contingency = st.number_input(
        "Contingency",
        value=budget["contingency"]
    )

    st.divider()

    st.markdown("## Documents")

    default_docs = app["documents"]

    document_options = [
        "Grant Proposal",
        "Registration Certificate",
        "Budget",
        "Project Timeline",
        "Bank Statement (Last 6 Months)",
        "Bank Details",
        "Beneficiary Information",
        "PAN Card",
        "Audited Financial Statements (Last 3 Years)",
        "Board Resolution",
        "Annual Report 2025",
        "Letters of Partnership",
    ]

    documents = st.multiselect(
        "Available Documents",
        document_options,
        default=default_docs,
    )

    declaration_signed = st.checkbox(
        "Declaration Signed",
        value=app["declaration_signed"]
    )

    submitted = st.form_submit_button(
        "🚀 Evaluate Application",
        use_container_width=True
    )

if submitted:

    application = {
        "organization": organization,
        "registration_number": registration_number,
        "year_established": year_established,
        "years_operating": years_operating,
        "contact_person": contact_person,
        "designation": designation,
        "email": email,
        "phone": phone,
        "project_title": project_title,
        "grant_category": grant_category,
        "requested_amount": requested_amount,
        "project_description": project_description,
        "beneficiaries": beneficiaries,
        "timeline": timeline,
        "budget": {
            "medical_camps": medical_camps,
            "medicines_supplies": medicines_supplies,
            "training_workshops": training_workshops,
            "travel_logistics": travel_logistics,
            "administration": administration,
            "contingency": contingency,
        },
        "documents": documents,
        "declaration_signed": declaration_signed,
    }

    state: GrantState = {
        "application": application,
        "plan": None,
        "tool_results": {},
        "review": None,
        "security_review": None,
        "worker_result": "",
        "final_decision": "",
    }

    with st.spinner("Running GrantGuard..."):
        result = graph.invoke(state)

    st.success("Evaluation Complete")

# -----------------------------------------------------
# Run
# -----------------------------------------------------

# if st.button("Evaluate Application", use_container_width=True):

#     try:
#         application = json.loads(application)

#     except Exception as e:
#         st.error(f"Invalid JSON\n\n{e}")
#         st.stop()

#     state: GrantState = {
#         "application": application,
#         "plan": None,
#         "tool_results": {},
#         "review": None,
#         "security_review": None,
#         "worker_result": "",
#         "final_decision": "",
#     }

#     with st.spinner("Running GrantGuard..."):

#         result = graph.invoke(state)

#     st.success("Evaluation Complete")

    # -------------------------------------------------
    # Planner
    # -------------------------------------------------

    st.header("Execution Plan")

    plan = result["plan"]

    if plan:

        for i, step in enumerate(plan.steps, start=1):

            with st.expander(f"Step {i}"):

                st.write(f"**Tool:** {step.tool}")
                st.write(f"**Required:** {step.required}")
                st.write(step.reason)

    # -------------------------------------------------
    # Tool Results
    # -------------------------------------------------

    st.header("Tool Results")

    for tool_name, tool in result["tool_results"].items():

        with st.expander(tool_name):

            st.write(f"Status: {tool.status}")
            st.write(f"Success: {tool.success}")
            st.write(f"Reason: {tool.reason}")

            st.json(tool.data)

    # -------------------------------------------------
    # Quality Review
    # -------------------------------------------------

    review = result["review"]

    st.header("Quality Review")

    col1, col2, col3 = st.columns(3)

    col1.metric("Coverage", review.coverage_score)
    col2.metric("Evidence", review.evidence_score)
    col3.metric("Confidence", review.confidence_score)

    st.write("### Summary")
    st.write(review.summary)

    st.write("### Strengths")
    st.write(review.strengths)

    st.write("### Weaknesses")
    st.write(review.weaknesses)

    # -------------------------------------------------
    # Security Review
    # -------------------------------------------------

    security = result["security_review"]

    st.header("Security Review")

    col1, col2 = st.columns(2)

    col1.metric("Security Score", security.security_score)
    col2.metric("Safe", str(security.safe))

    st.write("### Threats")
    st.write(security.threats)

    st.write("### Warnings")
    st.write(security.warnings)

    st.write("### Recommendations")
    st.write(security.recommendations)

    # -------------------------------------------------
    # Final Decision
    # -------------------------------------------------

    decision = result["final_decision"]

    st.markdown("---")
    st.header("🏁 Final Decision")

    # Decision Banner
    if decision.decision.upper() == "APPROVE":
        st.success("✅ APPLICATION APPROVED")
        decision_color = "green"
    elif decision.decision.upper() == "REJECT":
        st.error("❌ APPLICATION REJECTED")
        decision_color = "red"
    else:
        st.warning(f"⚠️ {decision.decision}")
        decision_color = "orange"

    # Summary Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Decision", decision.decision)

    with col2:
        st.metric("Confidence", f"{decision.confidence}%")

    st.markdown("### 📋 Executive Summary")

    st.info(decision.summary)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ❗ Reasons")

        for reason in decision.reasons:
            st.markdown(f"- {reason}")

    with col2:

        st.markdown("### 💡 Recommendations")

        for recommendation in decision.recommendations:
            st.markdown(f"- {recommendation}")