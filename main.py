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
        You are an expert procurement analyst. Your task is to analyze the following Request for Proposal (RFP) document and extract high-level, generalized evaluation criteria that can be used to fairly compare multiple vendor proposals.

        **IMPORTANT:** Focus on broad, general requirements rather than specific implementation details. The goal is to create evaluation criteria that multiple vendors can reasonably be expected to address, not to create overly specific technical specifications.

        RFP Content:
        {rfp_text}

        Please structure your analysis using the following categories. For each category, identify 2-5 high-level, generalized requirements that capture the essential needs without being overly specific.

        **Categories to Use:**

        * **Functional Requirements:** (What the system must do - focus on capabilities, not specific features)
        * **Technical Requirements:** (How the system must be built - focus on architecture and integration needs, not specific technologies)
        * **Security & Compliance:** (Security and regulatory requirements - focus on standards and certifications, not specific implementations)
        * **Support & Service Level Agreements (SLAs):** (Support and service requirements - focus on availability and response times)
        * **Project Management & Implementation:** (Implementation process requirements - focus on methodology and timeline)
        * **Pricing & Contractual Terms:** (Pricing and contract requirements - focus on structure and terms)

        **Guidelines for Requirements:**
        - Make requirements **general and flexible** enough that multiple vendors can address them
        - Focus on **what** needs to be accomplished, not **how** it should be done
        - Avoid overly specific technical details, brand names, or implementation specifics
        - Use broad, inclusive language that allows for different approaches
        - Focus on **outcomes and capabilities** rather than specific features

        **Examples of Good vs Bad Requirements:**

        ❌ **Too Specific:** "Must use Oracle Database 19c with Real Application Clusters"
        ✅ **Generalized:** "Must provide enterprise-grade database capabilities with high availability"

        ❌ **Too Specific:** "Must integrate with SAP ERP version 4.0"
        ✅ **Generalized:** "Must integrate with existing enterprise resource planning systems"

        ❌ **Too Specific:** "Must provide 99.99% uptime with 15-minute response time"
        ✅ **Generalized:** "Must provide high availability with defined service level agreements"

        **Output Format:**
        Provide the list in a clear, nested format with generalized requirements.

        Example:
        **Functional Requirements**
        - Must provide comprehensive user management and access control capabilities
        - Must support automated workflow and approval processes
        - Must offer reporting and analytics functionality

        **Technical Requirements**
        - Must integrate with existing enterprise systems and databases
        - Must provide secure, scalable architecture suitable for enterprise deployment
        - Must support web-based access with mobile compatibility

        Focus on requirements that are broad enough for fair vendor comparison while still being specific enough to evaluate meaningfully.
        """
        
        response = self.llm.call_model(prompt)
        
        # Parse the response to extract requirements organized by category
        requirements = []
        lines = response.split('\n')
        current_category = None
        category_requirements = {}
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Check if this is a category header
            if line.startswith('**') and line.endswith('**'):
                current_category = line.strip('*').strip()
                category_requirements[current_category] = []
                continue
            
            # Check if this is a requirement (starts with dash or bullet)
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                # Remove the bullet point and clean up
                requirement = line[1:].strip()
                if requirement and len(requirement) > 10:
                    if current_category:
                        category_requirements[current_category].append(requirement)
            elif line and not line.startswith('**') and not line.startswith('Example:') and not line.startswith('Focus on'):
                # If no bullet point but it looks like a requirement (long enough and not a header)
                if len(line) > 15 and not line.startswith('Please') and not line.startswith('Provide'):
                    if current_category:
                        category_requirements[current_category].append(line)
        
        # Convert to flat list with category headers
        for category, reqs in category_requirements.items():
            if reqs:  # Only add category if it has requirements
                # Add category header
                requirements.append(f"**{category}**")
                # Add each requirement
                for req in reqs:
                    requirements.append(req)
        
        return requirements
    
    def evaluate_vendor_proposal(self, vendor_text: str, requirements: List[str], vendor_name: str) -> tuple[Dict[str, str], str]:
        """Evaluate a vendor proposal against the requirements."""
        # Filter out category headers and summary text for evaluation
        actual_requirements = []
        for req in requirements:
            if (not req.startswith('**') and 
                not req.endswith('**') and 
                not req.startswith('---') and 
                not req.endswith('---') and
                not 'These requirements represent' in req and
                not 'core evaluation criteria' in req and
                len(req.strip()) > 10):
                actual_requirements.append(req)
        
        requirements_text = "\n".join([f"{i+1}. {req}" for i, req in enumerate(actual_requirements)])
        
        prompt = f"""
        You are an expert procurement analyst. Your task is to conduct a detailed evaluation of a vendor's proposal against a provided list of RFP requirements. You must be strict, objective, and avoid making assumptions. If information is not present, you must say so.

        Requirements to evaluate against:
        {requirements_text}

        Vendor Proposal Content:
        {vendor_text}

        For each requirement, provide a detailed evaluation with the following format:

        **Evaluation Format:**
        For each requirement, respond with:
        1. **Assessment**: "Yes", "No", or "Not Sure"
        2. **Explanation**: 2-3 sentences explaining your assessment

        **Assessment Criteria:**
        - **Yes**: The proposal clearly and specifically addresses the requirement with sufficient detail
        - **No**: The requirement is not mentioned, is vague, or lacks sufficient detail
        - **Not Sure**: The proposal mentions something related but it's unclear if it fully meets the requirement

        **Important Guidelines:**
        - Be strict and objective - do not make assumptions
        - If information is not present, say "Not Sure" and explain why
        - Do not create or infer information that is not explicitly stated
        - Provide specific evidence from the proposal to support your assessment
        - Keep explanations concise but informative (2-3 sentences max)

        **Response Format:**
        Provide your evaluation in this exact format:

        Requirement 1: [Yes/No/Not Sure] - [2-3 sentence explanation]
        Requirement 2: [Yes/No/Not Sure] - [2-3 sentence explanation]
        ...and so on for each requirement

        **Price Information:**
        After your evaluations, extract and provide pricing information from the proposal:
        - Look for total project cost, implementation cost, annual fees, or any pricing details
        - If multiple pricing options are provided, include all relevant pricing information
        - If no pricing information is found, state "No pricing information found in proposal"
        - Format: "Total Project Cost: [amount]" or "Implementation Cost: [amount], Annual Fee: [amount]" etc.

        **Scoring Information:**
        After your evaluations, provide a summary:
        - Total Yes responses: [count]
        - Total No responses: [count] 
        - Total Not Sure responses: [count]
        - Score: [Yes count × 1 + Not Sure count × 0.5] out of [total requirements]
        """
        
        response = self.llm.call_model(prompt)
        
        # Parse the response to extract evaluations and scoring
        evaluations = {}
        yes_count = 0
        no_count = 0
        not_sure_count = 0
        total_requirements = len(actual_requirements)
        price_info = "No pricing information found in proposal"
        
        lines = response.strip().split('\n')
        current_requirement_index = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for evaluation lines - be more flexible with format
            if ('Requirement' in line or 'requirement' in line) and ':' in line:
                # Try to extract assessment and explanation
                if ' - ' in line:
                    # Format: "Requirement X: Assessment - Explanation"
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        requirement_part = parts[0].strip()
                        explanation = parts[1].strip()
                        
                        # Extract assessment from requirement part
                        if ':' in requirement_part:
                            assessment_part = requirement_part.split(':', 1)[1].strip()
                            assessment = assessment_part.upper()
                            
                            if current_requirement_index < len(actual_requirements):
                                req = actual_requirements[current_requirement_index]
                                
                                # Count assessments
                                if assessment == 'YES':
                                    yes_count += 1
                                    evaluations[req] = f"Yes - {explanation}"
                                elif assessment == 'NO':
                                    no_count += 1
                                    evaluations[req] = f"No - {explanation}"
                                elif assessment == 'NOT SURE':
                                    not_sure_count += 1
                                    evaluations[req] = f"Not Sure - {explanation}"
                                else:
                                    # Try to extract assessment from the text
                                    if 'yes' in assessment.lower():
                                        yes_count += 1
                                        evaluations[req] = f"Yes - {explanation}"
                                    elif 'no' in assessment.lower():
                                        no_count += 1
                                        evaluations[req] = f"No - {explanation}"
                                    else:
                                        not_sure_count += 1
                                        evaluations[req] = f"Not Sure - {explanation}"
                                
                                current_requirement_index += 1
            
            # Look for price information - be more specific
            elif any(keyword in line.lower() for keyword in ['total project cost:', 'implementation cost:', 'annual fee:', 'total cost:', 'project cost:', 'price:', 'quote:', 'amount:']):
                if not any(keyword in line.lower() for keyword in ['requirement', 'assessment', 'scoring', 'total yes', 'total no']):
                    price_info = line.strip()
            
            # Look for scoring summary
            elif 'Total Yes responses:' in line:
                try:
                    yes_count = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'Total No responses:' in line:
                try:
                    no_count = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'Total Not Sure responses:' in line:
                try:
                    not_sure_count = int(line.split(':')[1].strip())
                except:
                    pass
        
        # If we didn't get any evaluations, try a simpler parsing approach
        if not evaluations and actual_requirements:
            # Try to find Yes/No/Not Sure patterns in the response
            response_lower = response.lower()
            for i, req in enumerate(actual_requirements):
                # Look for patterns around this requirement
                req_lower = req.lower()
                if req_lower in response_lower:
                    # Find the section around this requirement
                    req_index = response_lower.find(req_lower)
                    if req_index != -1:
                        # Look for assessment keywords in the surrounding text
                        surrounding_text = response[max(0, req_index-200):req_index+200].lower()
                        
                        if 'yes' in surrounding_text and 'no' not in surrounding_text:
                            yes_count += 1
                            evaluations[req] = "Yes - Requirement clearly addressed in proposal"
                        elif 'no' in surrounding_text:
                            no_count += 1
                            evaluations[req] = "No - Requirement not found or insufficiently addressed"
                        else:
                            not_sure_count += 1
                            evaluations[req] = "Not Sure - Unable to determine from proposal content"
                else:
                    not_sure_count += 1
                    evaluations[req] = "Not Sure - Requirement not found in proposal"
        
        # Create final result including category headers
        result = {}
        for req in requirements:
            if req.startswith('**') and req.endswith('**'):
                # Category header - no evaluation needed
                result[req] = "N/A"
            elif req.startswith('---') and req.endswith('---'):
                # Category header - no evaluation needed
                result[req] = "N/A"
            elif 'These requirements represent' in req or 'core evaluation criteria' in req:
                # Summary text - no evaluation needed
                result[req] = "N/A"
            elif req in evaluations:
                result[req] = evaluations[req]
            else:
                # If no evaluation was provided by the LLM, it means no information was found
                # This should be marked as "No" rather than "Not Sure"
                result[req] = "No - No information found in proposal"
        
        # Calculate scores by counting from the final result (more reliable than parsing LLM response)
        yes_count = sum(1 for val in result.values() if val.startswith('Yes -'))
        no_count = sum(1 for val in result.values() if val.startswith('No -'))
        not_sure_count = sum(1 for val in result.values() if val.startswith('Not Sure -'))
        
        # Calculate score
        score = yes_count * 1 + not_sure_count * 0.5
        total_possible = yes_count + no_count + not_sure_count
        
        # Add price information to evaluations
        evaluations["--- PRICE INFORMATION ---"] = price_info
        
        # Add scoring summary to evaluations
        evaluations["--- SCORING SUMMARY ---"] = f"Score: {score}/{total_possible} (Yes: {yes_count}, No: {no_count}, Not Sure: {not_sure_count})"
        
        # Add price and scoring information to the final result
        result["--- PRICE INFORMATION ---"] = evaluations["--- PRICE INFORMATION ---"]
        result["--- SCORING SUMMARY ---"] = evaluations["--- SCORING SUMMARY ---"]
        
        return result, response
    
    def create_evaluation_matrix(self, requirements: List[str]):
        """Create the initial evaluation matrix CSV file."""
        # Process requirements to handle category headers
        processed_requirements = []
        for req in requirements:
            if req.startswith('**') and req.endswith('**'):
                # This is a category header - make it stand out
                processed_requirements.append(f"--- {req.strip('*')} ---")
            else:
                # This is a regular requirement
                processed_requirements.append(req)
        
        df = pd.DataFrame({"Requirements": processed_requirements})
        df.to_csv(self.evaluation_matrix_file, index=False)
        st.success(f"Evaluation matrix created with {len(processed_requirements)} items (including category headers)!")
    
    def update_evaluation_matrix(self, vendor_evaluations: Dict[str, str], vendor_name: str):
        """Update the evaluation matrix with vendor scores."""
        try:
            df = pd.read_csv(self.evaluation_matrix_file)
            
            # Add new vendor column
            df[vendor_name] = df['Requirements'].map(vendor_evaluations)
            
            # Handle any new rows that might have been added (like price info and scoring)
            for req, evaluation in vendor_evaluations.items():
                if req not in df['Requirements'].values:
                    # Add new row for this requirement
                    new_row = pd.DataFrame({'Requirements': [req], vendor_name: [evaluation]})
                    df = pd.concat([df, new_row], ignore_index=True)
            
            # Ensure price and scoring information are at the bottom
            # Move price and scoring rows to the end if they exist
            price_rows = df[df['Requirements'].str.contains('PRICE INFORMATION', na=False)]
            scoring_rows = df[df['Requirements'].str.contains('SCORING SUMMARY', na=False)]
            
            # Remove price and scoring rows from their current positions
            df = df[~df['Requirements'].str.contains('PRICE INFORMATION|SCORING SUMMARY', na=False)]
            
            # Add them back at the end
            if not price_rows.empty:
                df = pd.concat([df, price_rows], ignore_index=True)
            if not scoring_rows.empty:
                df = pd.concat([df, scoring_rows], ignore_index=True)
            
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
    
    def calculate_scores_from_csv(self, vendor_name: str) -> Dict[str, any]:
        """Calculate scores directly from the CSV file for a specific vendor."""
        try:
            df = pd.read_csv(self.evaluation_matrix_file)
            
            if vendor_name not in df.columns:
                return {"error": f"Vendor {vendor_name} not found in matrix"}
            
            # Filter out category headers and summary rows
            evaluations = df[df[vendor_name] != "N/A"][vendor_name].tolist()
            
            # Count assessments
            yes_count = sum(1 for val in evaluations if val.startswith('Yes -'))
            no_count = sum(1 for val in evaluations if val.startswith('No -'))
            not_sure_count = sum(1 for val in evaluations if val.startswith('Not Sure -'))
            
            # Calculate score
            score = yes_count * 1 + not_sure_count * 0.5
            total_possible = yes_count + no_count + not_sure_count
            
            return {
                "vendor": vendor_name,
                "yes_count": yes_count,
                "no_count": no_count,
                "not_sure_count": not_sure_count,
                "score": score,
                "total_possible": total_possible,
                "score_percentage": (score / total_possible * 100) if total_possible > 0 else 0
            }
            
        except Exception as e:
            return {"error": f"Error calculating scores: {str(e)}"}

def check_aws_credentials():
    """Check if AWS credentials are properly configured."""
    try:
        # Check if .env file exists
        if not os.path.exists('.env'):
            return False, ".env file not found. Please create a .env file with your AWS credentials."
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Check if required credentials are present
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        session_token = os.getenv("AWS_SESSION_TOKEN")
        
        if not access_key or not secret_key:
            return False, "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required in .env file"
        
        # Create session with credentials from environment variables
        session_kwargs = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'region_name': AWS_REGION
        }
        
        if session_token:
            session_kwargs['aws_session_token'] = session_token
        
        session = boto3.Session(**session_kwargs)
        
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
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Vendor Evaluation Tool")
    st.markdown("Analyze RFPs and evaluate vendor proposals using Amazon Bedrock LLM")
    
    # Check AWS credentials
    credentials_ok, credentials_message = check_aws_credentials()
    
    if not credentials_ok:
        st.error(f"⚠️ {credentials_message}")
        st.markdown("""
        **To use this application, you need to create a .env file with your AWS credentials:**
        
        **Create a .env file in the project directory with these contents:**
        ```
        AWS_ACCESS_KEY_ID=your_access_key_here
        AWS_SECRET_ACCESS_KEY=your_secret_key_here
        AWS_SESSION_TOKEN=your_session_token_here
        AWS_DEFAULT_REGION=us-west-2
        ```
        
        **Or run the setup script:**
        ```bash
        python setup_credentials.py
        ```
        
        **Then restart the application:**
        ```bash
        streamlit run main.py --server.port 8501
        ```
        
        **Note:** The session token is optional for long-term credentials but required for temporary credentials.
        """)
        return
    
    st.success(f"✅ {credentials_message}")
    
    # Initialize the evaluator
    evaluator = VendorEvaluator()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    workflow = st.sidebar.radio(
        "Select Workflow:",
        ["Workflow 1: RFP Analysis", "Workflow 2: Vendor Proposal Scoring"]
    )
    
    if workflow == "Workflow 1: RFP Analysis":
        st.header("📋 Workflow 1: RFP Analysis & Evaluation Matrix Creation")
        
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
                        for req in requirements:
                            if req.startswith('**') and req.endswith('**'):
                                # This is a category header - display in bold
                                st.markdown(f"**{req.strip('*')}**")
                            else:
                                # This is a requirement - display with bullet
                                st.markdown(f"• {req}")
                        
                        # Create evaluation matrix (include category headers)
                        if st.button("Create Evaluation Matrix"):
                            # Include category headers in the matrix for better organization
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
        st.header("🏢 Workflow 2: Vendor Proposal Scoring")
        
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
                        vendor_evaluations, response = evaluator.evaluate_vendor_proposal(
                            proposal_text, requirements, vendor_name
                        )
                        
                        # Add price information to evaluations
                        if "--- PRICE INFORMATION ---" in vendor_evaluations:
                            price_info = vendor_evaluations["--- PRICE INFORMATION ---"]
                            st.success(f"📊 **Price Information:** {price_info}")
                        
                        # Debug: Show the raw LLM response
                        with st.expander("Debug: Raw LLM Response"):
                            st.text(response)
                        
                        # Display evaluation results
                        st.subheader(f"Evaluation Results for {vendor_name}:")
                        
                        # Create a more compact display
                        for req, evaluation in vendor_evaluations.items():
                            if req.startswith('---') and req.endswith('---'):
                                # This is a header or scoring summary
                                if 'SCORING SUMMARY' in req:
                                    st.markdown(f"**{evaluation}**")
                                elif 'PRICE INFORMATION' in req:
                                    st.markdown(f"**{evaluation}**")
                                else:
                                    # Category header - make it stand out but not too much spacing
                                    st.markdown(f"**{req}**")
                            elif evaluation == "N/A":
                                # Category header - just show the category name
                                st.markdown(f"**{req}**")
                            else:
                                # Regular requirement with evaluation - compact format
                                st.markdown(f"**{req}**")
                                st.markdown(f"*{evaluation}*")
                                st.markdown("")  # Just one line break instead of separator
                        
                        # Show scoring summary in a nice format
                        if "--- SCORING SUMMARY ---" in vendor_evaluations:
                            score_info = vendor_evaluations["--- SCORING SUMMARY ---"]
                            st.success(f"📊 **Final Score:** {score_info}")
                        
                        # Update evaluation matrix
                        evaluator.update_evaluation_matrix(vendor_evaluations, vendor_name)
                        
                        # Verify scores by calculating from CSV
                        csv_scores = evaluator.calculate_scores_from_csv(vendor_name)
                        if "error" not in csv_scores:
                            st.info(f"📊 **CSV Verification:** Score: {csv_scores['score']}/{csv_scores['total_possible']} (Yes: {csv_scores['yes_count']}, No: {csv_scores['no_count']}, Not Sure: {csv_scores['not_sure_count']}) - {csv_scores['score_percentage']:.1f}%")
                        
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
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** This application uses Amazon Bedrock LLM for document analysis and evaluation.")

if __name__ == "__main__":
    main()

