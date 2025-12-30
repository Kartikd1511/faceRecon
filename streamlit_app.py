import streamlit as st
import requests

API_BASE = "http://100.48.90.23/api"

st.set_page_config(layout="wide", page_icon="🛡️", page_title="Employee Safety & Face Recognition")

# --- Custom Header ---
st.markdown(
    """
    <div style='display: flex; align-items: center; justify-content: space-between; background: #f0f2f6; padding: 1.2rem 2rem; border-radius: 10px; margin-bottom: 1.5rem;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size:2.5rem; margin-right: 1rem;'>🛡️</span>
            <span style='font-size:2rem; font-weight: 700; color: #1a237e;'>Employee Safety & Face Recognition</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# --- Modal-like Enrollment Form ---
if "show_enroll" not in st.session_state:
    st.session_state.show_enroll = False

def open_enroll():
    st.session_state.show_enroll = True

def close_enroll():
    st.session_state.show_enroll = False

# Button to open the "modal"
enroll_col, main_col = st.columns([1, 5])
with enroll_col:
    if st.button("➕ Employee Face Enrollment", use_container_width=True):
        open_enroll()

# Simulated modal: show form in main area if triggered
if st.session_state.show_enroll:
    st.markdown("#### Enroll New Employee")
    with st.form("enroll_form", clear_on_submit=True):
        name = st.text_input("Name")
        empid = st.text_input("Employee ID")
        phone = st.text_input("Phone Number")
        image = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])
        col1, col3 = st.columns([3,36])
        with col1:
            submitted = st.form_submit_button("✅ Enroll")
        with col3:
            cancel = st.form_submit_button("❌ Cancel")
        if cancel:
            close_enroll()
        if submitted and image and name and empid and phone:
            files = {"image": image}
            data = {"name": name, "empid": empid, "phone_num": phone}
            try:
                with st.spinner("Enrolling employee, please wait..."):
                    #resp = requests.post("/api/enroll/", files=files, data=data)
                    resp = requests.post(f"{API_BASE}/enroll/", files=files, data=data)
                if resp.status_code == 200:
                    st.success(resp.json().get("message", "Enrolled!"))
                    close_enroll()
                elif resp.status_code == 409:
                    st.error(resp.json().get("message", "Employee already exists!"))
                else:
                    st.error("Enrollment failed. Please try again.")
            except Exception as e:
                st.error(f"Error: {e}")
    st.markdown("---")

# Main page for safety check

st.header("👷 Employee Safety Check")
uploaded_file = st.file_uploader("Upload Full Body Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    if st.button("🔍 Check Safety & Recognize Face"):
        files = {"image": uploaded_file}
        try:
            with st.spinner("Recognizing face and checking safety gear, please wait..."):
                #resp = requests.post("/api/recognize_and_safety/", files=files)
                resp = requests.post(f"{API_BASE}/recognize_and_safety/", files=files)
                result = resp.json()
            st.subheader("👤 Employee Details")
            details = result.get("details")
            if details and isinstance(details, list) and len(details) == 3:
                st.markdown(f"<span style='font-size:1.1rem'><b>Name:</b> {details[0]}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-size:1.1rem'><b>Employee ID:</b> {details[1]}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-size:1.1rem'><b>Phone No.:</b> {details[2]}</span>", unsafe_allow_html=True)
            else:
                st.info("No employee details found.")
            st.subheader("🦺 Safety Check")
            safety = result.get("safety")
            if isinstance(safety, list):
                for person in safety:
                    helmet_html = (
                        '<span style="color:green;font-weight:bold;">✅</span>'
                        if person.get('helmet_detected')
                        else '<span style="color:red;font-weight:bold;">❌</span>'
                    )
                    gloves_html = (
                        '<span style="color:green;font-weight:bold;">✅</span>'
                        if person.get('gloves_detected')
                        else '<span style="color:red;font-weight:bold;">❌</span>'
                    )
                    face_cover_html = (
                        '<span style="color:green;font-weight:bold;">✅</span>'
                        if person.get('face_cover_detected')
                        else '<span style="color:red;font-weight:bold;">❌</span>'
                    )
                    st.markdown(
                        f"""
                        <div style='background:#fffde7; border-radius:8px; padding:1rem; margin-bottom:0.5rem;'>
                            <b>Person {person['person']}</b><br>
                            Helmet detected: {helmet_html}<br>
                            Gloves detected: {gloves_html}<br>
                            Face Cover detected: {face_cover_html}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info(safety)
        except Exception as e:
            st.error(f"Error: {e}")