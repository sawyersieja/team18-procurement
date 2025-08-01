import streamlit as st
import boto3
import json
import pandas as pd
import PyPDF2
import io
import os
from typing import List, Dict
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - load from environment variables
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-west-2")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")

class BedrockLLM:
    def __init__(self, region_name: str = AWS_REGION, model_id: str = MODEL_ID):
        # Create session with credentials from environment variables
        self.session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),  # Handle session token
            region_name=region_name
        )
        self.client = self.session.client("bedrock-runtime", region_name=region_name)
        self.model_id = model_id

    def call_model(self, message: str, max_tokens: int = 4000) -> str:
        """Call the Bedrock model with a given message."""
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": message}],
        }
        
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(payload)
            )
            response_body = json.loads(response["body"].read())
            return response_body["content"][0]["text"]
        except Exception as e:
            st.error(f"Error calling Bedrock model: {str(e)}")
            return ""

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """Extract text content from a PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""

class VendorEvaluator:
    def __init__(self):
        self.llm = BedrockLLM()
        self.pdf_processor = PDFProcessor()
        self.evaluation_matrix_file = "evaluation_matrix.csv"
    
    def analyze_rfp(self, rfp_text: str) -> List[str]:
        """Analyze RFP and extract requirements using Bedrock LLM."""
        prompt = f"""
        You are an expert RFP analyst. Please analyze the following Request for Proposal (RFP) document and extract ALL technical and non-technical requirements.

        RFP Content:
        {rfp_text}

        Please provide a comprehensive list of requirements. Each requirement should be:
        1. Specific and clear
        2. Actionable and measurable
        3. Cover both technical and non-technical aspects

        Format your response as a simple list, with each requirement on a new line starting with a dash (-).
        Focus on extracting requirements that vendors would need to address in their proposals.
        """
        
        response = self.llm.call_model(prompt)
        
        # Parse the response to extract requirements
        requirements = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                # Remove the bullet point and clean up
                requirement = line[1:].strip()
                if requirement:
                    requirements.append(requirement)
            elif line and not line.startswith('Requirements') and not line.startswith('Here'):
                # If no bullet point but it looks like a requirement
                if len(line) > 10 and not line.startswith('Please'):
                    requirements.append(line)

        return requirements
    
    def evaluate_vendor_proposal(self, vendor_text: str, requirements: List[str], vendor_name: str) -> Dict[str, str]:
        """Evaluate a vendor proposal against the requirements."""
        requirements_text = "\n".join([f"{i+1}. {req}" for i, req in enumerate(requirements)])
        
        prompt = f"""
        You are evaluating a vendor proposal against specific requirements from an RFP.

        Requirements to evaluate against:
        {requirements_text}

        Vendor Proposal Content:
        {vendor_text}

        For each requirement, determine if the vendor's proposal addresses it. Respond with only "Yes" or "No" for each requirement, separated by commas.

        Example format: Yes,No,Yes,No,Yes

        Be strict in your evaluation. Only answer "Yes" if the proposal clearly and specifically addresses the requirement. Answer "No" if:
        - The requirement is not mentioned
        - The proposal is vague or unclear about the requirement
        - The proposal doesn't provide sufficient detail
        """
        
        response = self.llm.call_model(prompt)
        
        # Parse the response
        evaluations = []
        lines = response.strip().split('\n')
        for line in lines:
            if ',' in line:
                parts = [part.strip() for part in line.split(',')]
                evaluations.extend(parts)
            elif line.strip().upper() in ['YES', 'NO']:
                evaluations.append(line.strip().upper())
        
        # Ensure we have the right number of evaluations
        while len(evaluations) < len(requirements):
            evaluations.append("No")
        
        # Create a dictionary mapping requirements to evaluations
        result = {}
        for i, req in enumerate(requirements):
            if i < len(evaluations):
                result[req] = evaluations[i]
            else:
                result[req] = "No"
        
        return result
    
    def create_evaluation_matrix(self, requirements: List[str]):
        """Create the initial evaluation matrix CSV file."""
        df = pd.DataFrame({"Requirements": requirements})
        df.to_csv(self.evaluation_matrix_file, index=False)
        st.success(f"Evaluation matrix created with {len(requirements)} requirements!")
    
    def update_evaluation_matrix(self, vendor_evaluations: Dict[str, str], vendor_name: str):
        """Update the evaluation matrix with vendor scores."""
        try:
            df = pd.read_csv(self.evaluation_matrix_file)
            
            # Add new vendor column
            df[vendor_name] = df['Requirements'].map(vendor_evaluations)
            
            # Save updated matrix
            df.to_csv(self.evaluation_matrix_file, index=False)
            st.success(f"Evaluation matrix updated with {vendor_name} scores!")
            
        except Exception as e:
            st.error(f"Error updating evaluation matrix: {str(e)}")
    
    def get_evaluation_matrix(self) -> pd.DataFrame:
        """Get the current evaluation matrix."""
        try:
            return pd.read_csv(self.evaluation_matrix_file)
        except FileNotFoundError:
            return pd.DataFrame()

def check_aws_credentials():
    """Check if AWS credentials are properly configured."""
    try:
        # Check if .env file exists
        if not os.path.exists('.env'):
            return False, ".env file not found"
        
        # Load environment variables
        load_dotenv()
        
        # Check if required credentials are present
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        session_token = os.getenv("AWS_SESSION_TOKEN")
        
        if not access_key or not secret_key:
            return False, "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required in .env file"
        
        # Create session with credentials from .env
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
            region_name=AWS_REGION
        )

        # Test basic AWS access
        sts = session.client('sts')
        identity = sts.get_caller_identity()

        # Test Bedrock access
        bedrock = session.client('bedrock', region_name=AWS_REGION)
        models = bedrock.list_foundation_models()

        return True, f"AWS credentials valid - User: {identity.get('Arn', 'Unknown')}"
        
    except Exception as e:
        return False, f"Error checking AWS credentials: {str(e)}"

def main():
    st.set_page_config(
        page_title="Vendor Evaluation Tool",
        page_icon="csu.svg",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': None,
            'About': '# Vendor Evaluation Tool\nBuilt with Streamlit and Amazon Bedrock'
        }
    )
    
    # Apply Pantone Red theme with white background
    st.markdown("""
    <style>
    /* Force sidebar to be Pantone red */
    [data-testid="stSidebar"] {
        background-color: #E32636 !important;
    }
    
    [data-testid="stSidebar"] > div {
        background-color: #E32636 !important;
    }
    
    /* Force sidebar text to be white */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
    }
    
    /* Force sidebar radio buttons to be white text */
    [data-testid="stSidebar"] .stRadio > label {
        color: #FFFFFF !important;
    }
    
    /* Main background white */
    .main {
        background-color: #FFFFFF !important;
    }
    
    /* Text color black on white */
    .stMarkdown {
        color: #000000 !important;
    }
    
    h1, h2, h3 {
        color: #000000 !important;
    }
    
    /* Buttons Pantone red */
    .stButton > button {
        background-color: #E32636 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
    }
    
    .stButton > button:hover {
        background-color: #B91C1C !important;
    }
    
    /* File uploader Pantone red border */
    .stFileUploader {
        border: 2px dashed #E32636 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }
    
    /* Download button green */
    .stDownloadButton > button {
        background-color: #059669 !important;
        color: #FFFFFF !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #047857 !important;
    }
    
    /* Success message green */
    .stSuccess {
        background-color: #D1FAE5 !important;
        border-color: #A7F3D0 !important;
        color: #065F46 !important;
    }
    
    /* Error message red */
    .stError {
        background-color: #FEE2E2 !important;
        border-color: #FECACA !important;
        color: #991B1B !important;
    }
    
    /* Info message blue */
    .stInfo {
        background-color: #DBEAFE !important;
        border-color: #BFDBFE !important;
        color: #1E40AF !important;
    }
    
    /* Links Pantone red */
    a {
        color: #E32636 !important;
    }
    
    a:hover {
        color: #B91C1C !important;
    }
    
    /* Custom larger font for sidebar headline */
    [data-testid="stSidebar"] h1 {
        font-size: 2.5rem !important;
        font-weight: bold !important;
        line-height: 1.2 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Vendor Evaluation Tool")
    st.markdown("Analyze RFPs and evaluate vendor proposals using Amazon Bedrock LLM")
    
    # Check AWS credentials
    credentials_ok, credentials_message = check_aws_credentials()
    
    if not credentials_ok:
        st.error(f"⚠️ {credentials_message}")
        st.markdown("""
        **To use this application, you need to configure AWS credentials in a `.env` file:**
        
        Create a file named `.env` in this directory with the following content:
        ```
        AWS_ACCESS_KEY_ID=your_access_key_here
        AWS_SECRET_ACCESS_KEY=your_secret_key_here
        AWS_SESSION_TOKEN=your_session_token_here
        AWS_DEFAULT_REGION=us-west-2
        ```
        
        **Note:** The session token is optional for long-term credentials but required for temporary credentials.
        
        After creating the `.env` file, restart the application.
        """)
        return
    
    # Initialize the evaluator
    evaluator = VendorEvaluator()
    
    # Sidebar for navigation
    st.sidebar.markdown("# Request For Proposal's Made Simple")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")
    workflow = st.sidebar.radio(
        "Select Workflow:",
        ["Workflow 1: RFP Analysis", "Workflow 2: Vendor Proposal Scoring"]
    )
    
    if workflow == "Workflow 1: RFP Analysis":
        st.header(" Workflow 1: RFP Analysis & Evaluation Matrix Creation")
        
        st.markdown("""
        **Instructions:**
        1. Upload your Request for Proposal (RFP) PDF file
        2. The system will analyze the document and extract all requirements
        3. An evaluation matrix will be created as a CSV file
        """)
        
        uploaded_rfp = st.file_uploader(
            "Upload RFP Document (PDF)",
            type=['pdf'],
            help="Upload a single PDF file containing the RFP"
        )
        
        if uploaded_rfp is not None:
            with st.spinner("Processing RFP document..."):
                # Extract text from PDF
                rfp_text = evaluator.pdf_processor.extract_text_from_pdf(uploaded_rfp)
                
                if rfp_text:
                    st.success("PDF text extracted successfully!")
                    
                    # Show extracted text preview
                    with st.expander("View extracted text (first 500 characters)"):
                        st.text(rfp_text[:500] + "..." if len(rfp_text) > 500 else rfp_text)
                    
                    # Analyze RFP and extract requirements
                    st.info("Analyzing RFP and extracting requirements using Amazon Bedrock...")
                    requirements = evaluator.analyze_rfp(rfp_text)
                    
                    if requirements:
                        st.success(f"Successfully extracted {len(requirements)} requirements!")
                        
                        # Display requirements
                        st.subheader("Extracted Requirements:")
                        for i, req in enumerate(requirements, 1):
                            st.write(f"{i}. {req}")
                        
                        # Create evaluation matrix
                        if st.button("Create Evaluation Matrix"):
                            evaluator.create_evaluation_matrix(requirements)
                            
                            # Show the created matrix
                            df = evaluator.get_evaluation_matrix()
                            if not df.empty:
                                st.subheader("Evaluation Matrix Created:")
                                st.dataframe(df)
                                
                                # Download button
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="Download Evaluation Matrix (CSV)",
                                    data=csv,
                                    file_name="evaluation_matrix.csv",
                                    mime="text/csv"
                                )
                    else:
                        st.error("No requirements could be extracted from the RFP.")
                else:
                    st.error("Could not extract text from the uploaded PDF.")
    
    elif workflow == "Workflow 2: Vendor Proposal Scoring":
        st.header("Workflow 2: Vendor Proposal Scoring")
        
        st.markdown("""
        **Instructions:**
        1. Upload vendor proposal PDF files (one at a time)
        2. Provide the vendor name for each proposal
        3. The system will evaluate the proposal against the existing requirements
        4. The evaluation matrix will be updated with vendor scores
        """)
        
        # Check if evaluation matrix exists
        if not os.path.exists(evaluator.evaluation_matrix_file):
            st.error("No evaluation matrix found! Please complete Workflow 1 first to create the evaluation matrix.")
            return
        
        # Load current evaluation matrix
        current_matrix = evaluator.get_evaluation_matrix()
        if not current_matrix.empty:
            st.subheader("Current Evaluation Matrix:")
            st.dataframe(current_matrix)
        
        # Vendor proposal upload
        uploaded_proposal = st.file_uploader(
            "Upload Vendor Proposal (PDF)",
            type=['pdf'],
            help="Upload a vendor proposal PDF file"
        )
        
        vendor_name = st.text_input(
            "Vendor Name",
            help="Enter the name of the vendor (this will be used as the column header in the matrix)"
        )
        
        if uploaded_proposal is not None and vendor_name:
            # Check if vendor already exists in matrix
            if not current_matrix.empty and vendor_name in current_matrix.columns:
                st.warning(f"Vendor '{vendor_name}' already exists in the evaluation matrix. The scores will be updated.")
            
            if st.button("Evaluate Vendor Proposal"):
                with st.spinner("Processing vendor proposal..."):
                    # Extract text from PDF
                    proposal_text = evaluator.pdf_processor.extract_text_from_pdf(uploaded_proposal)
                    
                    if proposal_text:
                        st.success("Proposal text extracted successfully!")
                        
                        # Get requirements from current matrix
                        requirements = current_matrix['Requirements'].tolist()
                        
                        # Evaluate proposal
                        st.info("Evaluating proposal against requirements using Amazon Bedrock...")
                        vendor_evaluations = evaluator.evaluate_vendor_proposal(
                            proposal_text, requirements, vendor_name
                        )
                        
                        # Display evaluation results
                        st.subheader(f"Evaluation Results for {vendor_name}:")
                        results_df = pd.DataFrame({
                            'Requirement': list(vendor_evaluations.keys()),
                            'Score': list(vendor_evaluations.values())
                        })
                        st.dataframe(results_df)
                        
                        # Update evaluation matrix
                        evaluator.update_evaluation_matrix(vendor_evaluations, vendor_name)
                        
                        # Show updated matrix
                        updated_matrix = evaluator.get_evaluation_matrix()
                        st.subheader("Updated Evaluation Matrix:")
                        st.dataframe(updated_matrix)
                        
                        # Download button
                        csv = updated_matrix.to_csv(index=False)
                        st.download_button(
                            label="Download Updated Evaluation Matrix (CSV)",
                            data=csv,
                            file_name="evaluation_matrix.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error("Could not extract text from the uploaded PDF.")
    
    # AWS credentials status at the bottom
    st.markdown("---")
    st.success(f"✅ {credentials_message}")
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** This application uses Amazon Bedrock LLM for document analysis and evaluation.")

if __name__ == "__main__":
    main()

