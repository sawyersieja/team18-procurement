# Vendor Evaluation Tool - Setup Guide

This guide will help you set up and run the Vendor Evaluation Tool, a Python web application that uses Amazon Bedrock LLM to analyze RFPs and evaluate vendor proposals.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

You need AWS credentials with access to Amazon Bedrock. Configure them using one of these methods:

**Option A: AWS CLI (Recommended)**
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-west-2`
- Default output format: `json`

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2
```

### 3. Test Your Setup

```bash
python test_setup.py
```

This will verify that all dependencies are installed and AWS credentials are configured correctly.

### 4. Run the Application

**Full Application (requires AWS credentials):**
```bash
streamlit run main.py
```

**Demo Mode (no AWS credentials required):**
```bash
streamlit run demo.py
```

The application will open in your browser at `http://localhost:8501`.

## Detailed Setup Instructions

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access
- PDF files for testing (RFP and vendor proposals)

### AWS Bedrock Access

1. **Enable Bedrock in your AWS account:**
   - Go to AWS Console → Amazon Bedrock
   - Request access to the required models
   - The application uses `anthropic.claude-3-5-sonnet-20241022-v2:0`

2. **Create IAM User (if needed):**
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "bedrock:InvokeModel",
                   "bedrock:ListFoundationModels"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

### File Structure

```
compare-vendors/
├── main.py                 # Main Streamlit application
├── demo.py                 # Demo version (no AWS required)
├── test_setup.py           # Setup verification script
├── example_usage.py        # Programmatic usage example
├── requirements.txt        # Python dependencies
├── README.md              # Main documentation
├── SETUP_GUIDE.md         # This file
├── .gitignore             # Git ignore rules
└── evaluation_matrix.csv  # Generated evaluation matrix
```

## Usage Workflows

### Workflow 1: RFP Analysis

1. **Upload RFP PDF**: Use the file uploader to upload your RFP document
2. **Text Extraction**: The system extracts text from the PDF
3. **Requirement Analysis**: Bedrock LLM analyzes the document and extracts requirements
4. **Matrix Creation**: Creates an evaluation matrix CSV file
5. **Download**: Download the initial evaluation matrix

### Workflow 2: Vendor Proposal Scoring

1. **Upload Proposal**: Upload a vendor's proposal PDF
2. **Enter Vendor Name**: Provide the vendor's name
3. **Evaluation**: System evaluates the proposal against requirements
4. **Matrix Update**: Updates the evaluation matrix with vendor scores
5. **Download**: Download the updated evaluation matrix

## Configuration Options

### Model Configuration

Edit `main.py` to change the AWS region or model:

```python
# Configuration
AWS_REGION = "us-west-2"  # Change to your preferred region
MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"  # Change model if needed
```

### Available Models

- `anthropic.claude-3-5-sonnet-20241022-v2:0` (default)
- `anthropic.claude-3-5-haiku-20241022-v1:0` (faster, cheaper)
- `anthropic.claude-3-opus-20240229-v1:0` (most capable)

## Troubleshooting

### Common Issues

1. **"AWS credentials not found"**
   - Run `aws configure` or set environment variables
   - Verify credentials are in the correct region

2. **"Bedrock access test failed"**
   - Ensure Bedrock is enabled in your AWS account
   - Check IAM permissions for Bedrock access
   - Verify the model is available in your region

3. **"Could not extract text from PDF"**
   - Ensure PDF is not password-protected
   - Check if PDF contains extractable text (not just images)
   - Try a different PDF file

4. **"No evaluation matrix found"**
   - Complete Workflow 1 first to create the matrix
   - Check if `evaluation_matrix.csv` exists in the current directory

### Error Messages

- **Import errors**: Run `pip install -r requirements.txt`
- **Permission errors**: Check AWS IAM permissions
- **Model errors**: Verify model availability in your region

## Testing

### Run Tests

```bash
# Test setup
python test_setup.py

# Run example
python example_usage.py

# Test demo
streamlit run demo.py
```

### Sample Data

The demo includes sample RFP and vendor proposal data to test the functionality without real documents.

## Security Considerations

- Store AWS credentials securely
- Use IAM roles for production deployments
- Don't commit credentials to version control
- Consider using AWS Secrets Manager for production

## Performance Tips

- Use smaller models (Haiku) for faster processing
- Process large PDFs in chunks if needed
- Monitor AWS Bedrock usage and costs
- Consider caching results for repeated evaluations

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review AWS Bedrock documentation
3. Verify your setup with `python test_setup.py`
4. Try the demo mode first: `streamlit run demo.py`

## Next Steps

After successful setup:
1. Test with sample PDF files
2. Customize prompts in `main.py` if needed
3. Deploy to production environment
4. Set up monitoring and logging
5. Consider adding authentication and user management 