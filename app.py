import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import os

# Page configuration with custom icon
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
    
    /* Brand Colors */
    :root {
        --pal-blue: #0a2a43;
        --pal-green: #27ae60;
        --pal-teal: #30b392;
        --pal-orange: #f39c12;
    }
    
    /* Header styling */
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
    
    /* Dashboard cards */
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
    
    /* Form styling */
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
    
    /* Button styling */
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
    
    /* Hide streamlit elements */
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
    st.session_state.sessions = [{'date': 'Starts from 10/09/25', 'description': '60 Mins Physiotherapy Session', 'amount': 500}]

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

def show_dashboard():
    """Main dashboard page"""
    logo_b64 = load_logo_as_base64()
    
    # Header with logo
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
    
    # Main dashboard content
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
    
    # Feature cards
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
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
    
    with col4:
        st.markdown("""
        <div class="dashboard-card">
            <div style="font-size: 3rem; color: #30b392; margin-bottom: 1rem;">📱</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #0a2a43; margin-bottom: 0.5rem;">Responsive</div>
            <div style="color: #666;">Works on all devices</div>
        </div>
        """, unsafe_allow_html=True)

def show_form():
    """Invoice form page"""
    # Header with back button
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
    
    # Invoice Details Section
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
    
    # Patient Details Section
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
    
    # Problem and Treatment Section
    col1, col2 = st.columns(2)
    with col1:
        problem_desc = st.text_area("Medical Details", placeholder="Problem Description...", height=100)
    with col2:
        treatment_notes = st.text_area("Treatment Notes", placeholder="Treatment provided...", height=100)
    
    # Sessions Section
    st.markdown("""
    <div class="form-section">
        <div class="section-title">Sessions</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add session button
    if st.button("+ Add Session"):
        st.session_state.sessions.append({
            'date': 'Session date',
            'description': '60 Mins Physiotherapy Session',
            'amount': 500
        })
        st.rerun()
    
    # Display sessions
    for i, session in enumerate(st.session_state.sessions):
        st.markdown(f"**Session {i+1}**")
        col1, col2, col3, col4 = st.columns([3, 4, 2, 1])
        
        with col1:
            st.session_state.sessions[i]['date'] = st.text_input(
                "Session Date", 
                value=session['date'],
                placeholder="Session date",
                key=f"session_date_{i}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.session_state.sessions[i]['description'] = st.text_input(
                "Session Description",
                value=session['description'],
                key=f"session_desc_{i}",
                label_visibility="collapsed"
            )
        
        with col3:
            st.session_state.sessions[i]['amount'] = st.number_input(
                "Amount (₹)",
                min_value=0,
                value=session['amount'],
                key=f"session_amount_{i}",
                label_visibility="collapsed"
            )
        
        with col4:
            if len(st.session_state.sessions) > 1:
                if st.button("🗑️", key=f"remove_session_{i}"):
                    st.session_state.sessions.pop(i)
                    st.rerun()
    
    # Generate Invoice Button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        if st.button("Generate Invoice Preview", use_container_width=True):
            # Validation
            if not patient_name.strip():
                st.error("Please enter patient name")
                return
            if not patient_age.strip():
                st.error("Please enter patient age")
                return
            
            # Store all data in session state
            st.session_state.invoice_data = {
                'invoice_no': invoice_no,
                'invoice_date': invoice_date,
                'patient_name': patient_name,
                'patient_age': patient_age,
                'patient_sex': patient_sex,
                'patient_phone': patient_phone,
                'problem_desc': problem_desc if problem_desc else "General consultation",
                'treatment_notes': treatment_notes if treatment_notes else "As per treatment plan"
            }
            st.session_state.page = 'preview'
            st.rerun()

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

def generate_invoice_html(data, sessions, total_amount):
    """Generate complete HTML for the professional invoice with watermark and terms"""
    logo_b64 = load_logo_as_base64()
    watermark_b64 = load_watermark_as_base64()
    signature_b64 = load_signature_as_base64()
    
    # Use logo or fallback for header - make it bigger
    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Clinic Logo">'
    else:
        logo_html = f'<img src="{get_fallback_logo()}" alt="Clinic Logo">'

    # Use watermark image if available, otherwise use logo
    if watermark_b64:
        watermark_html = f'<img src="data:image/png;base64,{watermark_b64}" style="width: 400px; height: 400px; opacity: 0.05;">'
    elif logo_b64:
        watermark_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 400px; height: 400px; opacity: 0.05;">'
    else:
        watermark_html = f'<img src="{get_fallback_logo()}" style="width: 400px; height: 400px; opacity: 0.05;">'
    
    # Use signature image if available
    if signature_b64:
        signature_html = f'<img src="data:image/png;base64,{signature_b64}" style="max-width: 150px; max-height: 60px; object-fit: contain;">'
    else:
        signature_html = '<div style="font-family: cursive; font-size: 24px; color: #333; margin-bottom: 5px;">Dr. Bhuvana</div>'
    
    # Generate sessions table rows
    sessions_rows = ""
    for i, session in enumerate(sessions):
        row_bg = '#ffffff' if i % 2 == 0 else '#f8f9fa'
        sessions_rows += f"""
        <tr style="background: {row_bg};">
            <td style="padding: 15px; border: 1px solid #e0e0e0; color: #555; font-size: 22px;">{i+1}</td>
            <td style="padding: 15px; border: 1px solid #e0e0e0; color: #555; font-size: 22px;">{session['date']}</td>
            <td style="padding: 15px; border: 1px solid #e0e0e0; color: #555; font-size: 22px;">{session['description']}</td>
            <td style="padding: 15px; border: 1px solid #e0e0e0; text-align: right; color: #333; font-weight: 600; font-size: 22px;">₹{session['amount']:,.2f}</td>
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
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: white;
                color: #333;
                line-height: 1.6;
                font-size: 22px;
                
            }}
            .invoice-container {{
                width: 100%;
                max-width: 100%;   /* was 8.27in */
                min-height: 100%; /* was 11.69in */
                margin: 0 auto;
                background: white;
                position: relative;
                padding: 80px;      /* more padding */
                box-sizing: border-box;

            }}

            
            /* Watermark */
            .watermark {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 0;
                pointer-events: none;
            }}
            
            /* Content above watermark */
            .invoice-content {{
                position: relative;
                z-index: 1;
            }}
            
            /* Header */
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 50px;
                padding-bottom: 40px;
                border-bottom: 4px solid #30b392;
            }}
            
            .logo-section {{
                display: flex;
                align-items: center;
                justify-content: flex-start; /* left align */
                flex: none; /* don’t stretch */
            }}

            .logo-section img {{
                width: 270px;   /* adjust this to grow logo */
                height: auto;
                object-fit: contain;
            }}

            
            .invoice-header {{
                text-align: right;
                flex: 1;
            }}
            
            .invoice-title {{
                font-size: 42px;
                font-weight: 700;
                color: #0a2a43;
                margin-bottom: 10px;
            }}
            
            .invoice-meta {{
                font-size: 22px;
                color: #666;
            }}
            
            .invoice-number {{
                color: #f39c12;
                font-weight: 600;
                font-size: 24px;
            }}
            
            /* Info sections */
            .info-row {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 40px;
                margin: 40px 0;
            }}
            
            .info-section {{
                padding: 0;
            }}
            
            .info-title {{
                font-size: 22px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #30b392;
            }}
            
            .info-content p {{
                margin: 8px 0;
                font-size: 22px;
                color: #555;
            }}
            
            .info-content strong {{
                color: #333;
                font-weight: 600;
            }}
            
            /* Medical Details Box */
            .medical-details {{
                background: #f8f9fa;
                border-left: 4px solid #30b392;
                padding: 20px;
                margin: 30px 0;
                border-radius: 0 6px 6px 0;
            }}
            
            .medical-details h4 {{
                font-size: 22px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 15px;
            }}
            
            .medical-details p {{
                font-size: 22px;
                color: #555;
                margin: 8px 0;
            }}
            
            /* Sessions table */
            .sessions-section {{
                margin: 40px 0;
            }}
            
            .sessions-title {{
                font-size: 20px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 20px;
                border-bottom: 2px solid #30b392;
                padding-bottom: 10px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            
            th {{
                background: #0a2a43;
                color: white;
                padding: 18px 15px;
                text-align: left;
                font-size: 22px;
                font-weight: 600;
            }}
            
            th:last-child {{
                text-align: right;
            }}
            
            /* Totals */
            .totals-section {{
                margin: 40px 0;
                display: flex;
                justify-content: flex-end;
            }}
            
            .subtotal-box {{
                width: 300px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 6px;
                font-size: 20px;
                color: #555;
            }}
            
            .subtotal-row {{
                display: flex;
                justify-content: space-between;
                margin: 8px 0;
            }}
            
            .total-box {{
                width: 300px;
                margin-top: 15px;
                padding: 20px;
                background: #0a2a43;
                color: white;
                border-radius: 6px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 24px;
                font-weight: 600;
            }}
            
            /* Signature */
            .signature-section {{
                margin: 50px 0 40px;
                text-align: right;
            }}
            
            .signature-wrapper {{
                display: inline-block;
                text-align: center;
            }}
            
            .signature-line {{
                border-bottom: 2px solid #0a2a43;
                width: 250px;
                margin: 15px auto 8px;
            }}
            
            .signature-label {{
                font-size: 18px;
                color: #666;
                font-weight: 500;
            }}
            
            /* Terms */
            .terms-section {{
                margin-top: 50px;
                padding: 25px;
                background: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
            }}
            
            .terms-title {{
                font-size: 18px;
                font-weight: 600;
                color: #0a2a43;
                margin-bottom: 15px;
            }}
            
            .terms-content {{
                font-size: 20px;
                color: #666;
                line-height: 1.6;
            }}
            
            .terms-content li {{
                margin: 10px 0;
                list-style-position: inside;
            }}
            
            @media print {{
                body {{ margin: 0; }}
                .invoice-container {{ padding: 30px; }}
            }}
        </style>
    </head>
    <body>
        <div class="invoice-container">
            <!-- Watermark -->
            <div class="watermark">
                {watermark_html}
            </div>
            
            <!-- Invoice Content -->
            <div class="invoice-content">
                <!-- Header -->
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
                
                <!-- Patient and Clinic Info -->
                <div class="info-row">
                    <div class="info-section">
                        <div class="info-title">Patient Details:</div>
                        <div class="info-content">
                            <p><strong>Name:</strong> {data['patient_name']}</p>
                            <p><strong>Age:</strong> {data['patient_age']}</p>
                            <p><strong>Sex:</strong> {data['patient_sex']}</p>
                            <p><strong>Phone:</strong> {data['patient_phone']}</p>
                        </div>
                    </div>
                    <div class="info-section">
                        <div class="info-title">Clinic Details:</div>
                        <div class="info-content">
                            <p><strong>PAL Physiotherapy & Sports Rehab</strong></p>
                            <p><strong>Phone:</strong> +91 8639398229</p>
                            <p><strong>Doctor:</strong> Dr. Bhuvana</p>
                            <p><strong>Address:</strong> Plot No. 1-89/A/3/15, Vittal Rao Nagar,<br>
                            Madhapur, Hyderabad, Telangana 500081</p>
                            <p><strong>Registration:</strong> UDYAM-TS-09-0137821</p>
                        </div>
                    </div>
                </div>
                
                <!-- Medical Details -->
                <div class="medical-details">
                    <h4>Medical Details:</h4>
                    <p><strong>Problem Description:</strong><br>{data['problem_desc']}</p>
                    <p><strong>Treatment Notes:</strong><br>{data['treatment_notes']}</p>
                </div>
                
                <!-- Sessions Table -->
                <div class="sessions-section">
                    <div class="sessions-title">Sessions</div>
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 80px;">S.No</th>
                                <th style="width: 180px;">Session Date</th>
                                <th>Session Description</th>
                                <th style="width: 120px;">Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sessions_rows}
                        </tbody>
                    </table>
                </div>
                
                <!-- Totals -->
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
                
                <!-- Sales Tax Note -->
                <p style="text-align: right; font-size: 14px; color: #666; margin: 15px 0;">
                    Sales Tax: <strong>Nil</strong>
                </p>
                
                <!-- Signature -->
                <div class="signature-section">
                    <div class="signature-wrapper">
                        {signature_html}
                        <div class="signature-line"></div>
                        <div class="signature-label">Authorized Signature</div>
                    </div>
                </div>
                
                <!-- Terms & Conditions -->
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

def html_to_image_to_pdf(html_content):
    """Convert HTML to image, then image to PDF"""
    try:
        from html2image import Html2Image
        from PIL import Image
        import io
        import tempfile
        import uuid
        
        # Create a unique filename
        unique_name = f"invoice_{uuid.uuid4().hex[:8]}.png"
        
        # Initialize Html2Image with temporary directory
        temp_dir = tempfile.gettempdir()
        hti = Html2Image(output_path=temp_dir)
        
        # Set A4 dimensions at high DPI for quality - increased size for better A4 fit
        width = 2480  # Increased from 1654
        height = 3508  # Increased from 2339
        
        # Take screenshot
        hti.screenshot(
            html_str=html_content,
            save_as=unique_name,
            size=(width, height)
        )
        
        # Construct full path
        full_path = os.path.join(temp_dir, unique_name)
        
        # Check if file exists and convert to PDF
        if os.path.exists(full_path):
            try:
                # Open image
                img = Image.open(full_path)
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create PDF in memory
                pdf_buffer = io.BytesIO()
                
                # Save as PDF with A4 size
                img.save(
                    pdf_buffer, 
                    format='PDF',
                    resolution=300.0,  # Increased from 200
                    optimize=True
                )
                
                pdf_buffer.seek(0)
                pdf_bytes = pdf_buffer.getvalue()
                
                # Clean up temporary file
                try:
                    os.unlink(full_path)
                except:
                    pass
                
                return pdf_bytes
                
            except Exception as e:
                st.error(f"Error converting image to PDF: {str(e)}")
                try:
                    os.unlink(full_path)
                except:
                    pass
                return None
        else:
            st.error(f"Image file not created")
            return None
            
    except ImportError as e:
        missing_lib = []
        if "html2image" in str(e):
            missing_lib.append("html2image")
        if "PIL" in str(e) or "Pillow" in str(e):
            missing_lib.append("Pillow")
        
        st.error(f"""
        **Missing Libraries!**
        
        Please install the required libraries:
        ```bash
        pip install {" ".join(missing_lib) if missing_lib else "html2image Pillow"}
        ```
        
        These libraries are needed to convert HTML to high-quality PDF.
        """)
        return None
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

def show_preview():
    """Invoice preview and download page"""
    # Header with back button
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
    
    # Get data
    data = st.session_state.invoice_data
    total_amount = sum(session['amount'] for session in st.session_state.sessions)
    
    # Generate clean filename
    patient_name = data['patient_name'].strip().replace(' ', '_')
    clean_filename = ''.join(c for c in patient_name if c.isalnum() or c == '_').lower()
    pdf_filename = f"PAL_Invoice_{clean_filename}_{data['invoice_date'].strftime('%Y%m%d')}.pdf"
    
    # Generate HTML content
    html_content = generate_invoice_html(data, st.session_state.sessions, total_amount)
    
    # Display preview
    st.markdown("---")
    st.components.v1.html(html_content, height=1400, scrolling=True)
    
    # Download section with only PDF option
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #0a2a43; margin: 20px 0;'>Download Invoice</h3>", unsafe_allow_html=True)
    
    # Centered PDF download button
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col2:
        try:
            from html2image import Html2Image
            from PIL import Image
            
            if st.button("📥 Download PDF", use_container_width=True, type="primary"):
                with st.spinner("🔄 Generating high-quality PDF..."):
                    pdf_bytes = html_to_image_to_pdf(html_content)
                    if pdf_bytes:
                        # Immediate download
                        st.download_button(
                            label="📥 Click to Download",
                            data=pdf_bytes,
                            file_name=pdf_filename,
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                        st.success("✅ PDF generated! Click the button above to download.")
                    else:
                        st.error("Failed to generate PDF")
                        
        except ImportError:
            if st.button("📥 Download PDF", use_container_width=True, type="primary", disabled=True):
                pass
            st.caption("Install: `pip install html2image Pillow`")
    # Invoice summary cards
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
    
    # Instructions for print
    with st.expander("💡 How to Print Invoice"):
        st.markdown("""
        ### Direct PDF Download (Recommended)
        1. Click the **"Download PDF"** button above
        2. Wait for PDF generation (few seconds)
        3. The PDF will download automatically
        4. Open and print the downloaded PDF
        
        ### Print Settings for Best Quality:
        - **Paper Size:** A4
        - **Orientation:** Portrait
        - **Margins:** Default or Minimum
        - **Quality:** High/Best
        - **Scale:** 100% or Fit to page
        """)

def main():
    """Main application function"""
    # Sidebar with info
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
        4. Download PDF
        
        **Contact:**
        📞 +91 8639398229
        📍 Madhapur, Hyderabad
        
        ---
        © 2025 PAL Physiotherapy
        """)
    
    # Main page routing
    if st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'form':
        show_form()
    elif st.session_state.page == 'preview':
        show_preview()

if __name__ == "__main__":
    main()