import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import os

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
    
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'invoice_data' not in st.session_state:
    st.session_state.invoice_data = {}
if 'sessions' not in st.session_state:
    st.session_state.sessions = [{'description': '60 Mins Physiotherapy Session', 'qty': 1, 'per_session_cost': 500}]

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
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-card">
            <div style="margin-bottom: 1rem;">
                <img src="{logo_src}" width="100" height="100" style="object-fit: contain;">
            </div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Invoice Generator</div>
            <div style="color: #666; font-size: 1rem; margin-bottom: 1.5rem;">Create professional invoices for your physiotherapy sessions quickly and easily</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("+ Create New Invoice", use_container_width=True):
            st.session_state.page = 'form'
            st.rerun()
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 3rem; color: #27ae60; margin-bottom: 1rem;">⭐</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Professional</div>
            <div style="color: #666;">Medical-grade invoice templates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 3rem; color: #f39c12; margin-bottom: 1rem;">⚡</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Fast</div>
            <div style="color: #666;">Generate invoices in seconds</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 3rem; color: #0a2a43; margin-bottom: 1rem;">🔒</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Secure</div>
            <div style="color: #666;">Patient data protection</div>
        </div>
        """, unsafe_allow_html=True)

def show_form():
    """Invoice form page"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #0a2a43;">Create New Invoice</h1>
            <p style="color: #666;">Fill in the patient and session details below</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Invoice Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        invoice_no = st.text_input("Invoice No", value="PAL-PT-2025-001")
    with col2:
        invoice_date = st.date_input("Date", value=datetime.now().date())
    
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Patient Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Patient Name", placeholder="Enter patient's full name")
        patient_sex = st.selectbox("Patient Sex", options=["Male", "Female", "Others"])
    with col2:
        patient_age = st.text_input("Patient Age", placeholder="Enter patient's age")
        patient_phone = st.text_input("Patient Phone No", value="+91 ")
    
    col1, col2 = st.columns(2)
    with col1:
        problem_desc = st.text_area("Problem Description", placeholder="Problem Description...", height=100)
        mode_of_treatment = st.selectbox("Mode of Treatment", options=["Clinic visit", "Home Visit", "Online Treatment"])
    with col2:
        treatment_notes = st.text_area("Treatment Notes", placeholder="Treatment provided...", height=100)
    
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Session Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session start and end dates
    col1, col2 = st.columns(2)
    with col1:
        session_start_date = st.date_input("Session Start Date", value=datetime.now().date())
    with col2:
        session_end_date = st.date_input("Session End Date", value=datetime.now().date())
    
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
        if st.button("Generate Invoice Preview", use_container_width=True):
            if not patient_name.strip():
                st.error("Please enter patient name")
                return
            if not patient_age.strip():
                st.error("Please enter patient age")
                return
            
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
                'session_end_date': session_end_date
            }
            st.session_state.page = 'preview'
            st.rerun()

def generate_invoice_html(data, sessions, total_amount):
    """Generate complete HTML for the professional invoice"""
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
                            <p><strong>Phone:</strong> +91 8639398229</p>
                            <p><strong>Doctor:</strong> Dr. Bhuvana</p>
                            <p><strong>Address:</strong> Plot No. 1-89/A/3/15, Vittal Rao Nagar,<br>
                            Madhapur, Hyderabad, Telangana 500081</p>
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
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #0a2a43;">Invoice Preview</h1>
            <p style="color: #666;">Review your invoice before downloading</p>
        </div>
        """, unsafe_allow_html=True)
    
    data = st.session_state.invoice_data
    total_amount = sum(session['qty'] * session['per_session_cost'] for session in st.session_state.sessions)
    
    patient_name = data['patient_name'].strip().replace(' ', '_')
    clean_filename = ''.join(c for c in patient_name if c.isalnum() or c == '_').lower()
    html_filename = f"PAL_Invoice_{clean_filename}_{data['invoice_date'].strftime('%Y%m%d')}.html"
    
    html_content = generate_invoice_html(data, st.session_state.sessions, total_amount)
    
    st.markdown("---")
    st.components.v1.html(html_content, height=1400, scrolling=True)
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #0a2a43; margin: 20px 0;'>Download Invoice</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col2:
        st.download_button(
            label="📥 Download HTML Invoice",
            data=html_content,
            file_name=html_filename,
            mime="text/html",
            use_container_width=True,
            type="primary"
        )
        st.success("✅ Ready to download! Click the button above to save the HTML file.")
        
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
            <p style="margin: 5px 0; color: #666;"><strong>Sessions:</strong> {len(st.session_state.sessions)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #0a2a43; padding: 20px; border-radius: 8px; color: white;">
            <h4 style="color: white; margin: 0 0 10px 0;">💰 Total Amount</h4>
            <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">₹{total_amount:,.2f}</p>
            <p style="margin: 5px 0; font-size: 12px; opacity: 0.9;">Tax: Nil</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px; background: linear-gradient(135deg, #30b392 0%, #27ae60 100%); border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin: 0 0 10px 0;">🏥 PAL Physiotherapy</h3>
            <p style="margin: 0; font-size: 14px;">Invoice Generator v2.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        **Quick Guide:**
        1. Fill patient details
        2. Add treatment sessions
        3. Generate preview
        4. Download HTML file
        
        **Features:**
        - Print-ready HTML invoices
        - Professional medical template
        - Embedded images (no dependencies)
        - Easy to share and archive
        
        **Contact:**
        📞 +91 8639398229
        📍 Madhapur, Hyderabad
        
        ---
        © 2025 PAL Physiotherapy
        """)
    
    if st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'form':
        show_form()
    elif st.session_state.page == 'preview':
        show_preview()

if __name__ == "__main__":
    main()