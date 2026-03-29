import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import os
import re
import json

# Page configuration
st.set_page_config(
    page_title="PAL Physiotherapy Invoice Generator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    :root {
        --pal-blue: #0a2a43;
        --pal-green: #27ae60;
        --pal-teal: #30b392;
        --pal-orange: #f39c12;
    }
    
    .pal-header {
        background: linear-gradient(135deg, #0a2a43 0%, #27ae60 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .pal-logo {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .pal-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .dashboard-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
        text-align: center;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .form-section {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #27ae60;
    }
    
    .section-title {
        color: #0a2a43;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        border-bottom: 2px solid #27ae60;
        padding-bottom: 0.5rem;
    }
    
    .upload-section {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #f39c12;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #27ae60 0%, #30b392 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(39, 174, 96, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
        background: linear-gradient(135deg, #219a52 0%, #2ba085 100%);
    }
    
    .upload-info {
        background: #e8f5e8;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #c3e6c3;
    }
    
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Clinic address configurations - UPDATED WITH CORRECT ADDRESSES
CLINIC_ADDRESSES = {
    "Vittal Rao Nagar, Madhapur": {
        "display_name": "Vittal Rao Nagar, Madhapur",
        "full_address": "Plot No. 1-89/A/3/15, beside Siddarth Fitness gym,\nnear Gowra Tulips, Vittal Rao Nagar, Madhapur,\nGafoornagar, Hyderabad, Telangana 500081",
        "short_address": "Plot No. 1-89/A/3/15, beside Siddarth Fitness gym, near Gowra Tulips, Vittal Rao Nagar, Madhapur, Gafoornagar, Hyderabad 500081"
    },
    "Sri Ramnagar, Kondapur": {
        "display_name": "Sri Ramnagar, Kondapur",
        "full_address": "Street Number 5, beside Charminar Biriyani Shop,\nKondapur, Sri Ramnagar - Block C,\nHyderabad, Telangana 500084",
        "short_address": "Street Number 5, beside Charminar Biriyani Shop, Kondapur, Sri Ramnagar - Block C, Hyderabad 500084"
    }
}

# Initialize session state with proper form data preservation
def initialize_session_state():
    """Initialize all session state variables with proper defaults"""
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    if 'invoice_data' not in st.session_state:
        st.session_state.invoice_data = {}
    if 'sessions' not in st.session_state:
        st.session_state.sessions = [{'description': '60 Mins Physiotherapy Session', 'qty': 1, 'per_session_cost': 500}]
    if 'uploaded_invoice_data' not in st.session_state:
        st.session_state.uploaded_invoice_data = None
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    # Form data preservation - FIXED INVOICE YEAR TO 2026
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'invoice_no': "PAL-PT-2026-001",  # Changed from 2025 to 2026
            'invoice_date': datetime.now().date(),
            'clinic_location': "Vittal Rao Nagar, Madhapur",
            'patient_name': "",
            'patient_sex': "Male",
            'patient_age': "",
            'patient_phone': "+91 ",
            'problem_desc': "",
            'mode_of_treatment': "Clinic visit",
            'treatment_notes': "",
            'session_start_date': datetime.now().date(),
            'session_end_date': datetime.now().date()
        }

def extract_text_from_uploaded_pdf(uploaded_file):
    """Extract text content from uploaded PDF file"""
    try:
        import PyPDF2
        from io import BytesIO
        
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        text_content = ""
        
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
        
        return text_content
    except ImportError:
        st.error("PyPDF2 library not available. PDF text extraction disabled.")
        return None
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def parse_invoice_data_from_text(text_content):
    """Parse invoice data from extracted PDF text"""
    if not text_content:
        return None
    
    try:
        # Initialize parsed data dictionary
        parsed_data = {
            'invoice_no': "",
            'invoice_date': datetime.now().date(),
            'clinic_location': "Vittal Rao Nagar, Madhapur",
            'patient_name': "",
            'patient_sex': "Male",
            'patient_age': "",
            'patient_phone': "+91 ",
            'problem_desc': "",
            'mode_of_treatment': "Clinic visit",
            'treatment_notes': "",
            'session_start_date': datetime.now().date(),
            'session_end_date': datetime.now().date()
        }
        
        parsed_sessions = []
        
        # Extract invoice number
        invoice_match = re.search(r'Invoice number:\s*(PAL-PT-\d{4}-\d{3})', text_content)
        if invoice_match:
            parsed_data['invoice_no'] = invoice_match.group(1)
        
        # Extract patient name
        name_match = re.search(r'Name:\s*([^\n]+)', text_content)
        if name_match:
            parsed_data['patient_name'] = name_match.group(1).strip()
        
        # Extract patient age
        age_match = re.search(r'Age:\s*([^\n]+)', text_content)
        if age_match:
            parsed_data['patient_age'] = age_match.group(1).strip()
        
        # Extract patient sex
        sex_match = re.search(r'Sex:\s*(Male|Female|Others)', text_content)
        if sex_match:
            parsed_data['patient_sex'] = sex_match.group(1)
        
        # Extract phone number
        phone_match = re.search(r'Phone:\s*([^\n]+)', text_content)
        if phone_match:
            parsed_data['patient_phone'] = phone_match.group(1).strip()
        
        # Extract problem description
        problem_match = re.search(r'Problem Description:\s*([^\n]+)', text_content)
        if problem_match:
            parsed_data['problem_desc'] = problem_match.group(1).strip()
        
        # Extract treatment notes
        treatment_match = re.search(r'Treatment Notes:\s*([^\n]+)', text_content)
        if treatment_match:
            parsed_data['treatment_notes'] = treatment_match.group(1).strip()
        
        # Extract mode of treatment
        mode_match = re.search(r'Mode of Treatment:\s*(Clinic visit|Home Visit|Online Treatment)', text_content)
        if mode_match:
            parsed_data['mode_of_treatment'] = mode_match.group(1)
        
        # Extract clinic location
        if "Sri Ramnagar" in text_content:
            parsed_data['clinic_location'] = "Sri Ramnagar, Kondapur"
        elif "Vittal Rao Nagar" in text_content:
            parsed_data['clinic_location'] = "Vittal Rao Nagar, Madhapur"
        
        # Extract dates
        date_match = re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})', text_content)
        if date_match:
            try:
                parsed_data['invoice_date'] = datetime.strptime(date_match.group(1), '%d/%m/%Y').date()
            except:
                pass
        
        # Extract session dates
        session_start_match = re.search(r'Session Start Date:\s*(\d{2}/\d{2}/\d{4})', text_content)
        if session_start_match:
            try:
                parsed_data['session_start_date'] = datetime.strptime(session_start_match.group(1), '%d/%m/%Y').date()
            except:
                pass
        
        session_end_match = re.search(r'Session End Date:\s*(\d{2}/\d{2}/\d{4})', text_content)
        if session_end_match:
            try:
                parsed_data['session_end_date'] = datetime.strptime(session_end_match.group(1), '%d/%m/%Y').date()
            except:
                pass
        
        # Extract session details from table
        # This is a simplified approach - might need refinement based on actual PDF structure
        session_pattern = r'(\d+)\s+([^\d]+?)\s+(\d+)\s+₹([\d,]+\.\d{2})\s+₹([\d,]+\.\d{2})'
        session_matches = re.findall(session_pattern, text_content)
        
        for match in session_matches:
            try:
                session = {
                    'description': match[1].strip(),
                    'qty': int(match[2]),
                    'per_session_cost': float(match[3].replace(',', ''))
                }
                parsed_sessions.append(session)
            except:
                continue
        
        # If no sessions found, add default
        if not parsed_sessions:
            parsed_sessions = [{'description': '60 Mins Physiotherapy Session', 'qty': 1, 'per_session_cost': 500}]
        
        return {'form_data': parsed_data, 'sessions': parsed_sessions}
        
    except Exception as e:
        st.error(f"Error parsing invoice data: {str(e)}")
        return None

def load_logo_as_base64():
    """Load logo and convert to base64"""
    logo_paths = [
        "pal_logo.png",
        "pal_logo_full.png", 
        "assets/pal_logo.png",
        "images/pal_logo.png"
    ]
    
    for path in logo_paths:
        try:
            if os.path.exists(path):
                with open(path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        except:
            continue
    return None

def load_watermark_as_base64():
    """Load watermark image and convert to base64"""
    watermark_paths = [
        "pal_logo_icon.png",
        "watermark_logo.png",
        "pal_pal_logo_icon.png",
        "assets/pal_logo_icon.png",
        "images/pal_logo_icon.png"
    ]
    
    for path in watermark_paths:
        try:
            if os.path.exists(path):
                with open(path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        except:
            continue
    return None

def get_fallback_logo():
    """SVG fallback logo"""
    svg_logo = """
    <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#30b392;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#27ae60;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="100" cy="100" r="80" fill="url(#grad1)"/>
        <path d="M 70 100 L 90 120 L 130 70" stroke="white" stroke-width="12" fill="none" stroke-linecap="round"/>
        <text x="100" y="180" text-anchor="middle" fill="white" font-size="24" font-weight="bold">PAL</text>
    </svg>
    """
    return f"data:image/svg+xml;base64,{base64.b64encode(svg_logo.encode()).decode()}"

def load_signature_as_base64():
    """Load signature image and convert to base64"""
    signature_paths = [
        "dr_bhuvana_signature.png",
        "signature.png",
        "assets/signature.png",
        "images/signature.png"
    ]
    
    for path in signature_paths:
        try:
            if os.path.exists(path):
                with open(path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        except:
            continue
    return None

def show_dashboard():
    """Main dashboard page"""
    logo_b64 = load_logo_as_base64()
    
    if logo_b64:
        logo_src = f"data:image/png;base64,{logo_b64}"
    else:
        logo_src = get_fallback_logo()
    
    st.markdown(f"""
    <div class="pal-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
            <img src="{logo_src}" style="max-width: 250px; height: auto; object-fit: contain;">
            <div>
                <div class="pal-logo">PAL PHYSIOTHERAPY & SPORTS REHAB</div>
                <div class="pal-subtitle">Professional Healthcare Sessions</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main action cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 4rem; color: #27ae60; margin-bottom: 1rem;">📄</div>
            </div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Create New Invoice</div>
            <div style="color: #666; font-size: 1rem; margin-bottom: 1.5rem;">Start fresh with a new patient invoice</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("+ Create New Invoice", use_container_width=True):
            st.session_state.edit_mode = False
            st.session_state.uploaded_invoice_data = None
            st.session_state.page = 'form'
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-card">
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 4rem; color: #f39c12; margin-bottom: 1rem;">📤</div>
            </div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Edit Existing Invoice</div>
            <div style="color: #666; font-size: 1rem; margin-bottom: 1.5rem;">Upload a previous invoice PDF to edit</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📤 Upload & Edit Invoice", use_container_width=True):
            st.session_state.edit_mode = True
            st.session_state.page = 'upload'
            st.rerun()
    
    st.markdown("---")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 3rem; color: #27ae60; margin-bottom: 1rem;">⭐</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Professional</div>
            <div style="color: #666;">Medical-grade invoice templates with refund policy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 3rem; color: #f39c12; margin-bottom: 1rem;">⚡</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Fast & Editable</div>
            <div style="color: #666;">Generate new or edit existing invoices in seconds</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 3rem; color: #0a2a43; margin-bottom: 1rem;">🔒</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Secure</div>
            <div style="color: #666;">Patient data protection & privacy</div>
        </div>
        """, unsafe_allow_html=True)

def show_upload_page():
    """PDF upload page for editing existing invoices"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #0a2a43;">Upload Previous Invoice</h1>
            <p style="color: #666;">Upload a PDF of your previous PAL Physiotherapy invoice to edit it</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="upload-section">
        <div class="section-title">📤 Upload Invoice PDF</div>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PAL Physiotherapy invoice PDF file",
        type=['pdf'],
        help="Upload a previously generated PAL Physiotherapy invoice to edit its content"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Show file details
        file_details = {
            "File Name": uploaded_file.name,
            "File Size": f"{uploaded_file.size / 1024:.2f} KB",
            "File Type": uploaded_file.type
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            for key, value in file_details.items():
                st.info(f"**{key}:** {value}")
        
        st.markdown("---")
        
        # Process the uploaded PDF
        with st.spinner("🔄 Extracting invoice data from PDF..."):
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                
                # Extract text from PDF
                text_content = extract_text_from_uploaded_pdf(uploaded_file)
                
                if text_content:
                    # Parse the invoice data
                    parsed_data = parse_invoice_data_from_text(text_content)
                    
                    if parsed_data:
                        st.success("✅ Invoice data extracted successfully!")
                        
                        # Store the parsed data in session state
                        st.session_state.uploaded_invoice_data = parsed_data
                        
                        # Show preview of extracted data
                        with st.expander("👁️ Preview of Extracted Data", expanded=True):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("### Patient Information:")
                                st.write(f"**Name:** {parsed_data['form_data']['patient_name']}")
                                st.write(f"**Age:** {parsed_data['form_data']['patient_age']}")
                                st.write(f"**Sex:** {parsed_data['form_data']['patient_sex']}")
                                st.write(f"**Phone:** {parsed_data['form_data']['patient_phone']}")
                            
                            with col2:
                                st.markdown("### Invoice Details:")
                                st.write(f"**Invoice No:** {parsed_data['form_data']['invoice_no']}")
                                st.write(f"**Clinic:** {parsed_data['form_data']['clinic_location']}")
                                st.write(f"**Sessions:** {len(parsed_data['sessions'])}")
                                
                                total = sum(s['qty'] * s['per_session_cost'] for s in parsed_data['sessions'])
                                st.write(f"**Total Amount:** ₹{total:,.2f}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns([2, 2, 2])
                        
                        with col1:
                            if st.button("✏️ Edit This Invoice", use_container_width=True):
                                # Load the parsed data into form_data and sessions
                                st.session_state.form_data.update(parsed_data['form_data'])
                                st.session_state.sessions = parsed_data['sessions']
                                st.session_state.edit_mode = True
                                st.session_state.page = 'form'
                                st.rerun()
                        
                        with col2:
                            if st.button("🔄 Try Different PDF", use_container_width=True):
                                st.session_state.uploaded_invoice_data = None
                                st.rerun()
                    else:
                        st.error("❌ Could not parse invoice data from the PDF. Please ensure it's a PAL Physiotherapy invoice.")
                        st.info("💡 **Tip:** Make sure you're uploading a PDF generated by this PAL Invoice Generator.")
                else:
                    st.error("❌ Could not extract text from the PDF. Please try a different file.")
                    
            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")
                st.info("💡 **Note:** PDF processing requires the PyPDF2 library. Some PDF formats may not be supported.")
    
    else:
        # Show upload instructions
        st.markdown("""
        <div class="upload-info">
            <h4 style="color: #0a2a43; margin-bottom: 1rem;">📋 Upload Instructions:</h4>
            <ol style="color: #666; line-height: 1.6;">
                <li><strong>Select a PDF file</strong> - Only PDF files are supported</li>
                <li><strong>PAL Invoice PDFs work best</strong> - Upload invoices generated by this system</li>
                <li><strong>File size limit</strong> - Keep files under 200MB for best performance</li>
                <li><strong>Data extraction</strong> - The system will automatically extract patient and invoice details</li>
                <li><strong>Edit and regenerate</strong> - Modify any details and create an updated invoice</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔍 **Supported Data:** Patient details, invoice numbers, clinic information, session details, pricing, and dates will be automatically extracted from PAL Physiotherapy invoice PDFs.")

def show_form():
    """Invoice form page with session state preservation and edit mode"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back"):
            # Save current form data before going back
            save_form_data()
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with col2:
        if st.session_state.edit_mode:
            st.markdown("""
            <div style="text-align: center;">
                <h1 style="color: #0a2a43;">✏️ Edit Invoice</h1>
                <p style="color: #666;">Modify the invoice details below and regenerate</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center;">
                <h1 style="color: #0a2a43;">Create New Invoice</h1>
                <p style="color: #666;">Fill in the patient and session details below</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show edit mode indicator
    if st.session_state.edit_mode:
        st.success("📝 **Edit Mode**: You're editing a previously uploaded invoice. All fields have been pre-filled with the extracted data.")
    
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Invoice Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        invoice_no = st.text_input("Invoice No", value=st.session_state.form_data['invoice_no'])
    with col2:
        invoice_date = st.date_input("Date", value=st.session_state.form_data['invoice_date'])
    
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Clinic Location</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clinic address selection with preserved state
    clinic_location_index = list(CLINIC_ADDRESSES.keys()).index(st.session_state.form_data['clinic_location'])
    clinic_location = st.selectbox(
        "Select Clinic Location",
        options=list(CLINIC_ADDRESSES.keys()),
        index=clinic_location_index,
        format_func=lambda x: CLINIC_ADDRESSES[x]['display_name'],
        help="Choose the clinic location for this invoice"
    )
    
    # Display selected address details
    selected_address = CLINIC_ADDRESSES[clinic_location]
    st.info(f"📍 **Selected Address:** {selected_address['short_address']}")
    
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Patient Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Patient Name", value=st.session_state.form_data['patient_name'], placeholder="Enter patient's full name")
        patient_sex_index = ["Male", "Female", "Others"].index(st.session_state.form_data['patient_sex'])
        patient_sex = st.selectbox("Patient Sex", options=["Male", "Female", "Others"], index=patient_sex_index)
    with col2:
        patient_age = st.text_input("Patient Age", value=st.session_state.form_data['patient_age'], placeholder="Enter patient's age")
        patient_phone = st.text_input("Patient Phone No", value=st.session_state.form_data['patient_phone'])
    
    col1, col2 = st.columns(2)
    with col1:
        problem_desc = st.text_area("Problem Description", value=st.session_state.form_data['problem_desc'], placeholder="Problem Description...", height=100)
        mode_of_treatment_index = ["Clinic visit", "Home Visit", "Online Treatment"].index(st.session_state.form_data['mode_of_treatment'])
        mode_of_treatment = st.selectbox("Mode of Treatment", options=["Clinic visit", "Home Visit", "Online Treatment"], index=mode_of_treatment_index)
    with col2:
        treatment_notes = st.text_area("Treatment Notes", value=st.session_state.form_data['treatment_notes'], placeholder="Treatment provided...", height=100)
    
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Session Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session start and end dates with preserved state
    col1, col2 = st.columns(2)
    with col1:
        session_start_date = st.date_input("Session Start Date", value=st.session_state.form_data['session_start_date'])
    with col2:
        session_end_date = st.date_input("Session End Date", value=st.session_state.form_data['session_end_date'])
    
    if st.button("+ Add Session"):
        st.session_state.sessions.append({
            'description': '60 Mins Physiotherapy Session',
            'qty': 1,
            'per_session_cost': 500
        })
        st.rerun()
    
    # Display headers for the session inputs
    if st.session_state.sessions:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
        with col1:
            st.markdown("**Description of Services**")
        with col2:
            st.markdown("**QTY**")
        with col3:
            st.markdown("**Per Session Cost**")
        with col4:
            st.markdown("**Action**")
    
    for i, session in enumerate(st.session_state.sessions):
        st.markdown(f"**Session {i+1}**")
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
        
        with col1:
            st.session_state.sessions[i]['description'] = st.text_input(
                "Description of Services",
                value=session['description'],
                key=f"session_desc_{i}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.session_state.sessions[i]['qty'] = st.number_input(
                "QTY",
                min_value=1,
                value=session['qty'],
                key=f"session_qty_{i}",
                label_visibility="collapsed"
            )
        
        with col3:
            st.session_state.sessions[i]['per_session_cost'] = st.number_input(
                "Per Session Cost (₹)",
                min_value=0,
                value=session['per_session_cost'],
                key=f"session_cost_{i}",
                label_visibility="collapsed"
            )
        
        with col4:
            if len(st.session_state.sessions) > 1:
                if st.button("🗑️", key=f"remove_session_{i}"):
                    st.session_state.sessions.pop(i)
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        button_text = "Update Invoice Preview" if st.session_state.edit_mode else "Generate Invoice Preview"
        if st.button(button_text, use_container_width=True):
            if not patient_name.strip():
                st.error("Please enter patient name")
                return
            if not patient_age.strip():
                st.error("Please enter patient age")
                return
            
            # Save form data to session state
            st.session_state.form_data.update({
                'invoice_no': invoice_no,
                'invoice_date': invoice_date,
                'clinic_location': clinic_location,
                'patient_name': patient_name,
                'patient_sex': patient_sex,
                'patient_age': patient_age,
                'patient_phone': patient_phone,
                'problem_desc': problem_desc,
                'treatment_notes': treatment_notes,
                'mode_of_treatment': mode_of_treatment,
                'session_start_date': session_start_date,
                'session_end_date': session_end_date
            })
            
            st.session_state.invoice_data = {
                'invoice_no': invoice_no,
                'invoice_date': invoice_date,
                'patient_name': patient_name,
                'patient_age': patient_age,
                'patient_sex': patient_sex,
                'patient_phone': patient_phone,
                'problem_desc': problem_desc if problem_desc else "General consultation",
                'treatment_notes': treatment_notes if treatment_notes else "As per treatment plan",
                'mode_of_treatment': mode_of_treatment,
                'session_start_date': session_start_date,
                'session_end_date': session_end_date,
                'clinic_location': clinic_location,
                'clinic_address': selected_address
            }
            st.session_state.page = 'preview'
            st.rerun()

def save_form_data():
    """Save current form data to session state for preservation"""
    # This function can be expanded to save additional form data if needed
    # Currently, the form data is already being saved in the form itself
    pass

def generate_invoice_html(data, sessions, total_amount):
    """Generate complete HTML for the professional invoice with refund policy"""
    logo_b64 = load_logo_as_base64()
    watermark_b64 = load_watermark_as_base64()
    signature_b64 = load_signature_as_base64()
    
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Clinic Logo">'
    else:
        logo_html = f'<img src="{get_fallback_logo()}" alt="Clinic Logo">'

    if watermark_b64:
        watermark_html = f'<img src="data:image/png;base64,{watermark_b64}" style="width: 400px; height: 400px; opacity: 0.05;">'
    elif logo_b64:
        watermark_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 400px; height: 400px; opacity: 0.05;">'
    else:
        watermark_html = f'<img src="{get_fallback_logo()}" style="width: 400px; height: 400px; opacity: 0.05;">'
    
    if signature_b64:
        signature_html = f'<img src="data:image/png;base64,{signature_b64}" style="max-width: 150px; max-height: 60px; object-fit: contain;">'
    else:
        signature_html = '<div style="font-family: cursive; font-size: 24px; color: #333; margin-bottom: 5px;">Dr. Bhuvana</div>'
    
    # Get clinic address information
    clinic_info = data['clinic_address']
    
    sessions_rows = ""
    for i, session in enumerate(sessions):
        row_bg = '#ffffff' if i % 2 == 0 else '#f8f9fa'
        session_total = session['qty'] * session['per_session_cost']
        sessions_rows += f"""
        <tr style="background: {row_bg};">
            <td style="padding: 10px 8px; border: 1px solid #ddd; color: #333; font-size: 14px;">{i+1}</td>
            <td style="padding: 10px 8px; border: 1px solid #ddd; color: #333; font-size: 14px;">{session['description']}</td>
            <td style="padding: 10px 8px; border: 1px solid #ddd; text-align: center; color: #333; font-size: 14px;">{session['qty']}</td>
            <td style="padding: 10px 8px; border: 1px solid #ddd; text-align: right; color: #333; font-size: 14px;">₹{session['per_session_cost']:,.2f}</td>
            <td style="padding: 10px 8px; border: 1px solid #ddd; text-align: right; color: #333; font-weight: 600; font-size: 14px;">₹{session_total:,.2f}</td>
        </tr>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>PAL Physiotherapy Invoice</title>
        <style>
            @page {{
                size: A4;
                margin: 0.5in;
            }}
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: Arial, sans-serif;
                background: white;
                color: #333;
                line-height: 1.4;
                font-size: 14px;
            }}
            
            .invoice-container {{
                width: 100%;
                margin: 0 auto;
                background: white;
                position: relative;
                padding: 30px;
                min-height: 100vh;
            }}
            
            .watermark {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 0;
                pointer-events: none;
            }}
            
            .invoice-content {{
                position: relative;
                z-index: 1;
            }}
            
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 3px solid #30b392;
            }}
            
            .logo-section img {{
                width: 300px;
                height: auto;
                object-fit: contain;
            }}
            
            .invoice-header {{
                text-align: right;
            }}
            
            .invoice-title {{
                font-size: 28px;
                font-weight: 700;
                color: #0a2a43;
                margin-bottom: 8px;
            }}
            
            .invoice-meta {{
                font-size: 14px;
                color: #666;
            }}
            
            .invoice-number {{
                color: #f39c12;
                font-weight: 600;
                font-size: 16px;
            }}
            
            .patient-clinic-row {{
                display: flex;
                width: 100%;
                margin: 15px 0;
            }}
            
            .patient-section, .clinic-section {{
                width: 50%;
                padding-right: 20px;
            }}
            
            .clinic-section {{
                padding-right: 0;
                padding-left: 20px;
            }}
            
            .section-title {{
                font-size: 14px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 8px;
                padding-bottom: 5px;
                border-bottom: 2px solid #30b392;
            }}
            
            .section-content p {{
                margin: 3px 0;
                font-size: 14px;
                color: #333;
                line-height: 1.3;
            }}
            
            .section-content strong {{
                font-weight: 600;
            }}
            
            .medical-details {{
                background: #f8f9fa;
                border-left: 3px solid #30b392;
                padding: 12px;
                margin: 15px 0;
                border-radius: 0 4px 4px 0;
            }}
            
            .medical-details h4 {{
                font-size: 14px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 6px;
            }}
            
            .medical-details p {{
                font-size: 14px;
                color: #333;
                margin: 3px 0;
                line-height: 1.3;
            }}
            
            .sessions-section {{
                margin: 15px 0;
            }}
            
            .sessions-title {{
                font-size: 14px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 8px;
                border-bottom: 1px solid #30b392;
                padding-bottom: 5px;
            }}
            
            .session-dates {{
                margin: 8px 0;
                font-size: 14px;
                color: #333;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 8px;
            }}
            
            th {{
                background: #0a2a43;
                color: white;
                padding: 10px 8px;
                text-align: left;
                font-size: 14px;
                font-weight: 600;
                border: 1px solid #ddd;
            }}
            
            th:last-child {{
                text-align: right;
            }}
            
            td {{
                border: 1px solid #ddd;
                padding: 8px;
                font-size: 14px;
            }}
            
            .totals-section {{
                margin: 15px 0;
                display: flex;
                justify-content: flex-end;
            }}
            
            .subtotal-box {{
                width: 200px;
                padding: 8px;
                background: #f8f9fa;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
            }}
            
            .subtotal-row {{
                display: flex;
                justify-content: space-between;
                margin: 3px 0;
            }}
            
            .total-box {{
                width: 200px;
                margin-top: 6px;
                padding: 10px;
                background: #27ae60;
                color: white;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 16px;
                font-weight: 600;
            }}
            
            .signature-section {{
                margin: 20px 0 15px;
                text-align: right;
            }}
            
            .signature-wrapper {{
                display: inline-block;
                text-align: center;
            }}
            
            .signature-line {{
                border-bottom: 1px solid #0a2a43;
                width: 200px;
                margin: 8px auto 4px;
            }}
            
            .signature-label {{
                font-size: 12px;
                color: #666;
                font-weight: 500;
            }}
            
            .terms-section {{
                margin-top: 40px;
                padding: 12px;
                background: #f8f9fa;
                border-radius: 4px;
                border: 1px solid #e0e0e0;
                page-break-before: always;
                page-break-inside: avoid;
            }}
            
            .terms-title {{
                font-size: 12px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 6px;
            }}
            
            .terms-content {{
                font-size: 10px;
                color: #666;
                line-height: 1.3;
            }}
            
            .terms-content li {{
                margin: 3px 0;
                list-style-position: inside;
            }}
            
            .refund-policy {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 8px;
                margin-top: 8px;
                text-align: center;
            }}
            
            .refund-policy strong {{
                color: #856404;
                font-size: 11px;
                font-weight: 700;
            }}
            
            @media print {{
                body {{ 
                    margin: 0; 
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }}
                .invoice-container {{ 
                    padding: 20px;
                    min-height: auto;
                }}
                .watermark {{
                    position: fixed !important;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="invoice-container">
            <div class="watermark">
                {watermark_html}
            </div>
            
            <div class="invoice-content">
                <div class="header">
                    <div class="logo-section">
                        {logo_html}
                    </div>
                    <div class="invoice-header">
                        <div class="invoice-title">INVOICE</div>
                        <div class="invoice-meta">
                            Invoice number: <span class="invoice-number">{data['invoice_no']}</span><br>
                            Date: <strong>{data['invoice_date'].strftime('%d/%m/%Y')}</strong>
                        </div>
                    </div>
                </div>
                
                <div class="patient-clinic-row">
                    <div class="patient-section">
                        <div class="section-title">Patient Details:</div>
                        <div class="section-content">
                            <p><strong>Name:</strong> {data['patient_name']}</p>
                            <p><strong>Age:</strong> {data['patient_age']}</p>
                            <p><strong>Sex:</strong> {data['patient_sex']}</p>
                            <p><strong>Phone:</strong> {data['patient_phone']}</p>
                        </div>
                    </div>
                    <div class="clinic-section">
                        <div class="section-title">Clinic Details:</div>
                        <div class="section-content">
                            <p><strong>PAL Physiotherapy & Sports Rehab</strong></p>
                            <p><strong>Location:</strong> {clinic_info['display_name']}</p>
                            <p><strong>Address:</strong> {clinic_info['full_address']}</p>
                            <p><strong>Phone:</strong> +91 8639398229</p>
                            <p><strong>Doctor:</strong> Dr. Bhuvana</p>
                            <p><strong>Registration:</strong> UDYAM-TS-09-0137821</p>
                        </div>
                    </div>
                </div>
                
                <div class="medical-details">
                    <h4>Medical Details:</h4>
                    <p><strong>Problem Description:</strong><br>{data['problem_desc']}</p>
                    <p><strong>Treatment Notes:</strong><br>{data['treatment_notes']}</p>
                    <p><strong>Mode of Treatment:</strong> {data['mode_of_treatment']}</p>
                </div>
                
                <div class="sessions-section">
                    <div class="sessions-title">Session Details</div>
                    <div class="session-dates">
                        <strong>Session Start Date:</strong> {data['session_start_date'].strftime('%d/%m/%Y')} | 
                        <strong>Session End Date:</strong> {data['session_end_date'].strftime('%d/%m/%Y')}
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 60px;">S.No</th>
                                <th>Description of Services</th>
                                <th style="width: 80px;">QTY</th>
                                <th style="width: 120px;">Per Session Cost</th>
                                <th style="width: 120px;">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sessions_rows}
                        </tbody>
                    </table>
                </div>
                
                <div class="totals-section">
                    <div>
                        <div class="subtotal-box">
                            <div class="subtotal-row">
                                <span>Subtotal</span>
                                <span>₹{total_amount:,.2f}</span>
                            </div>
                        </div>
                        <div class="total-box">
                            <span>Total</span>
                            <span>₹{total_amount:,.2f}</span>
                        </div>
                    </div>
                </div>
                
                <p style="text-align: right; font-size: 12px; color: #666; margin: 8px 0;">
                    Sales Tax: <strong>Nil</strong>
                </p>
                
                <div class="signature-section">
                    <div class="signature-wrapper">
                        {signature_html}
                        <div class="signature-line"></div>
                        <div class="signature-label">Authorized Signature</div>
                    </div>
                </div>
                
                <div class="terms-section">
                    <div class="terms-title">Terms & Conditions</div>
                    <div class="terms-content">
                        <ol>
                            <li>The clinic is not responsible for severe reactions during prescribed medical treatment unless due to office personnel without proper supervision.</li>
                            <li>Clients are required to disclose any pre-existing medical conditions, injuries, or medications before starting therapy.</li>
                            <li>The clinic shall not be held liable for complications arising from undisclosed medical conditions.</li>
                            <li>All pending sessions should agree to the treatment plan and appointment fee associated procedures.</li>
                            <li>In case of disputes, efforts will be made to resolve them amicably. Jurisdiction for any legal matters will be Hyderabad, Telangana.</li>
                        </ol>
                    </div>
                    
                    <div class="refund-policy">
                        <strong>Kindly note - The amount which you pay in package is not refundable.</strong>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def show_preview():
    """Invoice preview and download page"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.page = 'form'
            st.rerun()
    
    with col2:
        if st.session_state.edit_mode:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #0a2a43;">Updated Invoice Preview</h1>
                <p style="color: #666;">Review your edited invoice before downloading</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #0a2a43;">Invoice Preview</h1>
                <p style="color: #666;">Review your invoice before downloading</p>
            </div>
            """, unsafe_allow_html=True)
    
    data = st.session_state.invoice_data
    total_amount = sum(session['qty'] * session['per_session_cost'] for session in st.session_state.sessions)
    
    patient_name = data['patient_name'].strip().replace(' ', '_')
    clinic_name = data['clinic_location'].replace(' ', '_').replace(',', '')
    clean_filename = ''.join(c for c in patient_name if c.isalnum() or c == '_').lower()
    
    # Add edit indicator to filename
    edit_suffix = "_EDITED" if st.session_state.edit_mode else ""
    html_filename = f"PAL_Invoice_{clean_filename}_{clinic_name}_{data['invoice_date'].strftime('%Y%m%d')}{edit_suffix}.html"
    
    html_content = generate_invoice_html(data, st.session_state.sessions, total_amount)
    
    st.markdown("---")
    st.components.v1.html(html_content, height=1400, scrolling=True)
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #0a2a43; margin: 20px 0;'>Download Invoice</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col2:
        download_label = "📥 Download Updated Invoice" if st.session_state.edit_mode else "📥 Download HTML Invoice"
        st.download_button(
            label=download_label,
            data=html_content,
            file_name=html_filename,
            mime="text/html",
            use_container_width=True,
            type="primary"
        )
        
        success_message = "✅ Updated invoice ready to download!" if st.session_state.edit_mode else "✅ Ready to download! Click the button above to save the HTML file."
        st.success(success_message)
        
    with st.expander("💡 How to Use the HTML Invoice"):
        st.markdown("""
        ### After downloading the HTML file:
        
        **For Printing:**
        1. Double-click the downloaded HTML file to open in your browser
        2. Press `Ctrl+P` (or `Cmd+P` on Mac) to print
        3. In print settings:
           - **Paper Size:** A4
           - **Orientation:** Portrait  
           - **Margins:** Default or Minimum
           - **Background graphics:** Enabled (to show colors and logo)
        4. Choose "Save as PDF" if you want a PDF copy
        
        **For Converting to PDF (Best Results):**
        
        **Recommended Online Tools:**
        - **PDF24.org** - Often maintains layouts well
        - **SmallPDF.com** - Good for simple conversions
        - **HTMLtoPDF.com** - Specialized for HTML conversion
        
        **Browser-based PDF (Most Reliable):**
        1. Open HTML file in **Google Chrome** or **Microsoft Edge**
        2. Press `Ctrl+P` (Print)
        3. Select "Save as PDF" as destination
        4. Set margins to "Minimum" for best layout
        5. Enable "Background graphics"
        
        **Tips for Better PDF Conversion:**
        - Use **Chrome** or **Edge** browsers for HTML viewing before conversion
        - Avoid tools that strip CSS styling
        - If layout breaks, try "Print to PDF" from browser instead
        - Some online converters work better with larger page margins
        
        **For Sharing:**
        - Email the HTML file directly (works offline)
        - Convert to PDF using browser print function
        - The file contains all images embedded
        
        **For Editing:**
        - Open with any text editor to modify
        - All styling and images are embedded in the file
        - No external dependencies required
        """)
        
        st.info("**Pro Tip:** For the most reliable PDF with perfect layout, use your browser's 'Print to PDF' feature instead of online converters!")

    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #0a2a43; margin: 20px 0;'>Invoice Summary</h3>", unsafe_allow_html=True)
    
    # Show edit mode indicator in summary
    if st.session_state.edit_mode:
        st.info("📝 **This is an edited invoice** - Updated from previously uploaded PDF")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #30b392;">
            <h4 style="color: #0a2a43; margin: 0 0 10px 0;">📋 Patient Info</h4>
            <p style="margin: 5px 0; color: #666;"><strong>Name:</strong> {data['patient_name']}</p>
            <p style="margin: 5px 0; color: #666;"><strong>Age/Sex:</strong> {data['patient_age']}/{data['patient_sex']}</p>
            <p style="margin: 5px 0; color: #666;"><strong>Phone:</strong> {data['patient_phone']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #f39c12;">
            <h4 style="color: #0a2a43; margin: 0 0 10px 0;">📅 Invoice Details</h4>
            <p style="margin: 5px 0; color: #666;"><strong>Invoice No:</strong> {data['invoice_no']}</p>
            <p style="margin: 5px 0; color: #666;"><strong>Date:</strong> {data['invoice_date'].strftime('%d/%m/%Y')}</p>
            <p style="margin: 5px 0; color: #666;"><strong>Location:</strong> {data['clinic_address']['display_name']}</p>
            <p style="margin: 5px 0; color: #666;"><strong>Sessions:</strong> {len(st.session_state.sessions)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #0a2a43; padding: 20px; border-radius: 8px; color: white;">
            <h4 style="color: white; margin: 0 0 10px 0;">💰 Total Amount</h4>
            <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">₹{total_amount:,.2f}</p>
            <p style="margin: 5px 0; font-size: 12px; opacity: 0.9;">Tax: Nil | Refund: Not Available</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state at the start
    initialize_session_state()
    
    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px; background: linear-gradient(135deg, #30b392 0%, #27ae60 100%); border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin: 0 0 10px 0;">🏥 PAL Physiotherapy</h3>
            <p style="margin: 0; font-size: 14px;">Invoice Generator v2.3</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Show available clinic locations
        st.markdown("### 🏢 Clinic Locations:")
        for location_key, location_data in CLINIC_ADDRESSES.items():
            st.markdown(f"📍 **{location_data['display_name']}**")
            st.markdown(f"<small>{location_data['short_address']}</small>", unsafe_allow_html=True)
            st.markdown("---")
        
        st.markdown("""
        **Quick Guide:**
        1. Create new invoice OR upload existing PDF
        2. Fill/edit patient details
        3. Add/modify treatment sessions
        4. Generate preview
        5. Download HTML file
        
        **New Features v2.3:**
        - ✅ Upload & edit existing invoices
        - ✅ Refund policy in terms
        - ✅ PDF data extraction
        - ✅ Form data preservation
        - ✅ Edit mode indicators
                
        **Features:**
        - Multiple clinic locations
        - Print-ready HTML invoices
        - Professional medical template
        - Embedded images (no dependencies)
        - Easy to share and archive
        
        **Contact:**
        📞 +91 8639398229
        📍 Multiple Locations in Hyderabad
        
        ---
        © 2026 PAL Physiotherapy
        """)
    
    if st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'upload':
        show_upload_page()
    elif st.session_state.page == 'form':
        show_form()
    elif st.session_state.page == 'preview':
        show_preview()

if __name__ == "__main__":
    main()
