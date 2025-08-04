# 🚌 Voigts Student Data Processing Suite

A comprehensive web application for managing student transportation data workflow, featuring Word to PDF conversion, AI-powered PDF data extraction, and data validation capabilities.

## 🌟 Features

- **📄 Word to PDF Conversion**: Convert Word documents to professional PDF format
- **🤖 AI PDF Data Extraction**: Extract student data from PDF forms using Azure AI Document Intelligence
- **📊 Data Validation**: Compare extracted data with district databases
- **🎨 Modern UI**: Glass morphism design with Voigts branding
- **☁️ Cloud Ready**: Optimized for Streamlit Cloud deployment

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd voigts-student-data-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Azure credentials**
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
   - Add your Azure AI Document Intelligence credentials

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

### Cloud Deployment (Streamlit Cloud)

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push this code to the repository

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path to `streamlit_app.py`

3. **Configure Secrets**
   - In Streamlit Cloud app settings, add these secrets:
   ```toml
   [azure]
   endpoint = "your-azure-endpoint"
   api_key = "your-azure-api-key"
   
   [app]
   title = "Voigts Student Opt-In Data Management Suite"
   description = "Professional transportation data processing for school districts"
   ```

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Azure AI Document Intelligence subscription
- pandas, openpyxl for data processing
- python-docx, reportlab for document processing

## 🏗️ Architecture

```
voigts-student-data-app/
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── secrets.toml         # Configuration secrets
├── Voigts Bus Service Logo.png  # Company logo
└── README.md                # This file
```

## 🎨 Features Detail

### Word to PDF Converter
- Upload .docx files
- Convert to professional PDF format
- Maintains document formatting
- Download converted PDFs

### AI PDF Data Extraction
- Powered by Azure AI Document Intelligence
- Batch processing of multiple PDFs
- Structured data extraction
- Export to CSV/Excel formats

### Data Validation
- Compare AI-extracted data with district databases
- Support for Excel and CSV files
- Data quality metrics
- Export validation results

## 🔧 Configuration

### Azure AI Setup
1. Create an Azure AI Document Intelligence resource
2. Get your endpoint URL and API key
3. Add credentials to Streamlit Cloud secrets

### Streamlit Cloud Secrets
```toml
[azure]
endpoint = "https://your-resource.cognitiveservices.azure.com/"
api_key = "your-32-character-api-key"

[app]
title = "Your App Title"
description = "Your app description"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and questions:
- **Technical Issues**: Create a GitHub issue
- **Business Inquiries**: Contact Voigt's Bus Companies
- **Development**: Contact Chayton Creations Co.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏆 Acknowledgments

- **Voigt's Bus Companies** - Transportation expertise and requirements
- **Chayton Creations Co.** - Development and technical implementation
- **Azure AI** - Document Intelligence capabilities
- **Streamlit** - Web application framework

---

Made with 💙 for **Sauk Rapids-Rice** | **ROCORI** | **Stride Academy** | **Math & Science Academy**
