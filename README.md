# Vendor Evaluation Tool

A Python web application built with Streamlit that serves as a vendor evaluation tool using Amazon Bedrock Large Language Model (LLM). The application analyzes Request for Proposal (RFP) documents and evaluates vendor proposals against extracted requirements.

## Features

- **Workflow 1: RFP Analysis** - Upload and analyze RFP documents to extract requirements
- **Workflow 2: Vendor Proposal Scoring** - Evaluate vendor proposals against requirements
- **Automated CSV Generation** - Create and update evaluation matrices
- **PDF Processing** - Extract text from PDF documents
- **LLM-Powered Analysis** - Use Amazon Bedrock for intelligent document analysis

## Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access
- AWS credentials configured (via AWS CLI, environment variables, or .env file)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your AWS credentials using one of these methods:

### Option 1: Interactive Setup (Recommended)
```bash
python setup_credentials.py
```
This will guide you through entering your AWS credentials and create a `.env` file automatically.

### Option 2: Manual .env File
Create a file named `.env` in the project directory:
```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-west-2
```

### Option 3: AWS CLI
```bash
aws configure
```

### Option 4: Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2
```

## Usage

### Starting the Application

Run the Streamlit application:

```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Demo Mode (No AWS Required)

If you want to test the interface without AWS credentials:

```bash
streamlit run demo.py
```

### Workflow 1: RFP Analysis

1. **Upload RFP Document**: Use the file uploader to upload your RFP PDF file
2. **Text Extraction**: The system will extract text from the PDF
3. **Requirement Analysis**: The Bedrock LLM will analyze the document and extract all technical and non-technical requirements
4. **Matrix Creation**: Click "Create Evaluation Matrix" to generate the initial CSV file
5. **Download**: Download the evaluation matrix for further use

### Workflow 2: Vendor Proposal Scoring

1. **Upload Vendor Proposal**: Upload a vendor's proposal PDF file
2. **Enter Vendor Name**: Provide the vendor's name (used as column header)
3. **Evaluation**: The system will evaluate the proposal against each requirement
4. **Matrix Update**: The evaluation matrix will be updated with vendor scores
5. **Download**: Download the updated evaluation matrix

## Configuration

The application uses the following configuration (defined in `main.py`):

- **AWS Region**: `us-west-2` (configurable via environment variables)
- **Model ID**: `anthropic.claude-3-5-sonnet-20241022-v2:0` (configurable via environment variables)

You can modify these settings by editing the `.env` file or setting environment variables.

## Output Format

The evaluation matrix CSV file will have the following structure:

```csv
Requirements,Vendor A,Vendor B
"Must support single sign-on (SSO) with SAML 2.0",Yes,Yes
"Must provide 24/7 technical support via phone",Yes,No
"Solution must be deployable on-premise",No,Yes
"Data must be encrypted at rest using AES-256",Yes,Yes
```

## File Structure

```
compare-vendors/
├── main.py                 # Main Streamlit application
├── demo.py                 # Demo version (no AWS required)
├── setup_credentials.py    # Interactive credential setup
├── test_setup.py           # Setup verification script
├── example_usage.py        # Programmatic usage example
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── SETUP_GUIDE.md         # Detailed setup guide
├── .gitignore             # Git ignore file
├── .env                   # AWS credentials (created by setup)
└── evaluation_matrix.csv  # Generated evaluation matrix (created after use)
```

## Dependencies

- **streamlit**: Web application framework
- **boto3**: AWS SDK for Python
- **pandas**: Data manipulation and CSV handling
- **PyPDF2**: PDF text extraction
- **python-dotenv**: Environment variable management

## Testing

### Test Your Setup
```bash
python test_setup.py
```

### Run Example
```bash
python example_usage.py
```

## Troubleshooting

### Common Issues

1. **AWS Credentials Error**: 
   - Run `python setup_credentials.py` to set up credentials interactively
   - Ensure your AWS credentials are properly configured
   - Verify you have access to Amazon Bedrock

2. **PDF Extraction Issues**: 
   - Make sure the PDF is not password-protected and contains extractable text
   - Try a different PDF file if extraction fails

3. **Bedrock Access**: 
   - Verify that your AWS account has access to Amazon Bedrock and the specified model
   - Check IAM permissions for Bedrock access

### Error Messages

- **"No evaluation matrix found"**: Complete Workflow 1 first to create the evaluation matrix
- **"Error calling Bedrock model"**: Check your AWS credentials and Bedrock access
- **"Could not extract text from PDF"**: The PDF may be image-based or corrupted

## Security Notes

- AWS credentials are stored in the `.env` file (which is gitignored)
- Do not commit credentials to version control
- Consider using AWS IAM roles for production deployments
- The `.env` file is automatically excluded from version control

## License

This project is provided as-is for educational and evaluation purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Run `python test_setup.py` to verify your setup
3. Try the demo mode first: `streamlit run demo.py`
4. Refer to the AWS Bedrock documentation 