#!/usr/bin/env python3
"""
🚌 Voigts Student Data Processing Suite - Complete Transportation Data Management
A comprehensive web interface for managing the entire student transportation data workflow.

Features:
- Word to PDF Conversion for transportation forms
- PDF Data Extraction with AI for student preferences
- Data Validation and Comparison with district databases  
- Modern, responsive UI with Voigts branding
"""

import streamlit as st
import pandas as pd
import io
import os
import tempfile
from datetime import datetime
import base64
from pathlib import Path

# Import Word to PDF functionality
try:
    from docx import Document
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from io import BytesIO
    DOCX_TO_PDF_AVAILABLE = True
except ImportError:
    DOCX_TO_PDF_AVAILABLE = False

# Import Azure AI functionality  
try:
    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential
    AZURE_AI_AVAILABLE = True
except ImportError:
    AZURE_AI_AVAILABLE = False

# Configure Streamlit page
st.set_page_config(
    page_title="Voigts Student Data Processing Suite",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Glass effect background */
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 25%, #60a5fa 50%, #fbbf24 75%, #f59e0b 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .emoji-icon {
        -webkit-text-fill-color: #1e3a8a !important;
        background: none !important;
        color: #1e3a8a !important;
        margin-right: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #1e3c72;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    .logo-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .logo-section h2 {
        color: #1e3c72;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .logo-section p {
        color: #1e3c72;
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
        opacity: 0.9;
    }
    
    .upload-section {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .upload-section:hover {
        background: rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(251, 191, 36, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }
    
    .results-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.9) 0%, rgba(251, 191, 36, 0.9) 100%);
        backdrop-filter: blur(10px);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #064e3b;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
    }
    
    .warning-box {
        background: rgba(251, 191, 36, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #92400e;
        box-shadow: 0 4px 16px rgba(251, 191, 36, 0.1);
    }
    
    /* Glass morphism styling for tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        padding: 0.5rem !important;
        gap: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #1e3c72 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 0 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #fbbf24 100%) !important;
        color: white !important;
        border: 1px solid rgba(251, 191, 36, 0.5) !important;
        box-shadow: 0 6px 25px rgba(30, 58, 138, 0.3) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 12px !important;
        border: 2px dashed rgba(251, 191, 36, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 2px dashed rgba(251, 191, 36, 0.8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stFileUploader button {
        background: linear-gradient(135deg, #1e3a8a 0%, #fbbf24 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3) !important;
    }
    
    .stFileUploader button:hover {
        background: linear-gradient(135deg, #1e40af 0%, #f59e0b 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

def show_header_and_logo():
    """Display the header with logo"""
    # Try to load the logo
    logo_path = "Voigts Bus Service Logo.png"
    
    if os.path.exists(logo_path):
        # Read image and encode as base64 for inline display
        with open(logo_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        
        # Use Streamlit columns for perfect centering
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown(f"""
            <div style="
                text-align: center !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                width: 100% !important;
            ">
                <img src="data:image/png;base64,{img_base64}" 
                     style="
                         width: 150px !important;
                         height: auto !important;
                         display: block !important;
                         margin: 0 auto !important;
                         object-fit: contain !important;
                     ">
            </div>
            """, unsafe_allow_html=True)
    else:
        # Use Streamlit columns for emoji fallback too
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("""
            <div style="
                text-align: center !important;
                font-size: 3rem;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                width: 100% !important;
            ">🚌</div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="logo-section" style="text-align: center; margin-bottom: 20px; margin-top: 5px;">
        <h2>Voigt's Bus Companies <span style="color: #1e3c72;">✕</span> Chayton Creations Co.</h2>
        <p style="color: #1e3c72; margin: 0; font-weight: 500;">Student Opt-In Data Management Solutions</p>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    """Main dashboard with all tools"""
    st.markdown('<h1 class="main-header">🚌 Student Data Processing Suite</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Complete transportation data management workflow</p>', unsafe_allow_html=True)

    # Tool selection tabs
    tab1, tab2, tab3 = st.tabs(["📄 Word to PDF", "🤖 AI PDF Extraction", "📊 Data Validation"])

    with tab1:
        show_word_to_pdf_tool()

    with tab2:
        show_pdf_extraction_tool()

    with tab3:
        show_data_validation_tool()

def show_word_to_pdf_tool():
    """Word to PDF conversion tool"""
    st.markdown("### 📄 Word to PDF Converter")
    st.markdown("Convert your Word documents to professional PDF format")
    
    if not DOCX_TO_PDF_AVAILABLE:
        st.warning("⚠️ Word to PDF conversion requires additional dependencies. Some features may be limited.")
    
    uploaded_file = st.file_uploader(
        "Upload Word Document",
        type=['docx'],
        help="Upload a .docx file to convert to PDF"
    )
    
    if uploaded_file is not None:
        try:
            # Read the document
            doc = Document(uploaded_file)
            
            # Create PDF using ReportLab
            buffer = BytesIO()
            pdf_doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                textColor=colors.HexColor('#1e3c72')
            )
            story.append(Paragraph(f"Document: {uploaded_file.name}", title_style))
            story.append(Spacer(1, 12))
            
            # Process paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    para = Paragraph(paragraph.text, styles['Normal'])
                    story.append(para)
                    story.append(Spacer(1, 12))
            
            # Build PDF
            pdf_doc.build(story)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            st.success("✅ PDF conversion completed!")
            
            # Download button
            st.download_button(
                label="📥 Download PDF",
                data=pdf_data,
                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"❌ Error converting file: {str(e)}")

def show_pdf_extraction_tool():
    """AI PDF extraction tool"""
    st.markdown("### 🤖 AI PDF Data Extraction")
    st.markdown("Extract student data from PDF forms using Azure AI")
    
    if not AZURE_AI_AVAILABLE:
        st.error("❌ Azure AI dependencies not available. Please install azure-ai-formrecognizer.")
        return
    
    # Check for Azure credentials
    try:
        endpoint = st.secrets["azure"]["endpoint"]
        api_key = st.secrets["azure"]["api_key"]
    except:
        st.error("❌ Azure credentials not configured. Please set up secrets in Streamlit Cloud.")
        st.info("Required secrets: azure.endpoint and azure.api_key")
        return
    
    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload PDF files containing student data"
    )
    
    if uploaded_files:
        if st.button("🚀 Extract Data", type="primary"):
            try:
                # Initialize Azure client
                client = DocumentAnalysisClient(
                    endpoint=endpoint,
                    credential=AzureKeyCredential(api_key)
                )
                
                all_extracted_data = []
                progress_bar = st.progress(0)
                
                for i, uploaded_file in enumerate(uploaded_files):
                    st.write(f"Processing: {uploaded_file.name}")
                    
                    # Analyze document
                    poller = client.begin_analyze_document(
                        "prebuilt-document", 
                        document=uploaded_file.read()
                    )
                    result = poller.result()
                    
                    # Extract data
                    extracted_data = {
                        'filename': uploaded_file.name,
                        'content': []
                    }
                    
                    for page in result.pages:
                        for line in page.lines:
                            extracted_data['content'].append(line.content)
                    
                    all_extracted_data.append(extracted_data)
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                # Create DataFrame for download
                df_data = []
                for doc in all_extracted_data:
                    for line in doc['content']:
                        df_data.append({
                            'Filename': doc['filename'],
                            'Extracted_Text': line
                        })
                
                df = pd.DataFrame(df_data)
                
                st.success(f"✅ Extracted data from {len(uploaded_files)} files!")
                st.dataframe(df)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Extracted Data (CSV)",
                    data=csv,
                    file_name=f"extracted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"❌ Error extracting data: {str(e)}")

def show_data_validation_tool():
    """Data validation and comparison tool"""
    st.markdown("### 📊 Data Validation & Comparison")
    st.markdown("Compare extracted student data with district databases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 AI Extracted Data")
        ai_file = st.file_uploader(
            "Upload AI Extracted Data",
            type=['xlsx', 'csv'],
            key="ai_data"
        )
    
    with col2:
        st.markdown("#### 🏫 District Database")
        district_file = st.file_uploader(
            "Upload District Data",
            type=['xlsx', 'csv'],
            key="district_data"
        )
    
    if ai_file and district_file:
        if st.button("🔍 Compare Data", type="primary"):
            try:
                # Read the files
                if ai_file.name.endswith('.csv'):
                    df_ai = pd.read_csv(ai_file)
                else:
                    df_ai = pd.read_excel(ai_file)
                
                if district_file.name.endswith('.csv'):
                    df_district = pd.read_csv(district_file)
                else:
                    df_district = pd.read_excel(district_file)
                
                st.success("✅ Files loaded successfully!")
                
                # Display basic info
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("AI Data Records", len(df_ai))
                with col2:
                    st.metric("District Data Records", len(df_district))
                
                # Show sample data
                st.markdown("#### AI Extracted Data Sample")
                st.dataframe(df_ai.head())
                
                st.markdown("#### District Data Sample")
                st.dataframe(df_district.head())
                
                # Basic comparison logic could be added here
                st.info("🔧 Advanced comparison features coming soon!")
                
            except Exception as e:
                st.error(f"❌ Error processing files: {str(e)}")

def show_footer():
    """Display footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #333; padding: 20px;'>
        <p><strong>Voigt's Bus Companies X Chayton Creations Co.</strong> | Student Opt-In Data Management</p>
        <p>Made with 💙 for | <strong>Sauk Rapids-Rice</strong> | <strong>ROCORI</strong> | <strong>Stride Academy</strong> | <strong>Math & Science Academy</strong></p>
        <p>🤖 Powered by advanced AI technology for seamless transportation data processing</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    show_header_and_logo()
    show_dashboard()
    show_footer()

if __name__ == "__main__":
    main()
