#!/usr/bin/env python3
"""
Demo script for the Vendor Evaluation Tool.
This script demonstrates the application interface using mock data.
"""

import streamlit as st
import pandas as pd
import os
from typing import List, Dict

# Mock data for demonstration
MOCK_RFP_TEXT = """
REQUEST FOR PROPOSAL: ENTERPRISE SOFTWARE SOLUTION

We are seeking proposals for an enterprise software solution that meets the following requirements:

Technical Requirements:
- Must support single sign-on (SSO) with SAML 2.0
- Must provide REST API for integration
- Must support multi-tenant architecture
- Must be deployable on-premise or in the cloud
- Must provide real-time data synchronization

Security Requirements:
- Data must be encrypted at rest using AES-256
- Must support role-based access control (RBAC)
- Must provide audit logging for all user actions
- Must comply with SOC 2 Type II standards

Support Requirements:
- Must provide 24/7 technical support via phone and email
- Must offer training and documentation
- Must provide implementation services
- Must offer maintenance and updates

Performance Requirements:
- Must support at least 1000 concurrent users
- Must have 99.9% uptime SLA
- Must provide response times under 2 seconds
"""

MOCK_REQUIREMENTS = [
    "Must support single sign-on (SSO) with SAML 2.0",
    "Must provide REST API for integration",
    "Must support multi-tenant architecture",
    "Must be deployable on-premise or in the cloud",
    "Must provide real-time data synchronization",
    "Data must be encrypted at rest using AES-256",
    "Must support role-based access control (RBAC)",
    "Must provide audit logging for all user actions",
    "Must comply with SOC 2 Type II standards",
    "Must provide 24/7 technical support via phone and email",
    "Must offer training and documentation",
    "Must provide implementation services",
    "Must offer maintenance and updates",
    "Must support at least 1000 concurrent users",
    "Must have 99.9% uptime SLA",
    "Must provide response times under 2 seconds"
]

MOCK_VENDOR_A_EVALUATIONS = {
    "Must support single sign-on (SSO) with SAML 2.0": "Yes",
    "Must provide REST API for integration": "Yes",
    "Must support multi-tenant architecture": "Yes",
    "Must be deployable on-premise or in the cloud": "Yes",
    "Must provide real-time data synchronization": "Yes",
    "Data must be encrypted at rest using AES-256": "Yes",
    "Must support role-based access control (RBAC)": "Yes",
    "Must provide audit logging for all user actions": "Yes",
    "Must comply with SOC 2 Type II standards": "Yes",
    "Must provide 24/7 technical support via phone and email": "Yes",
    "Must offer training and documentation": "Yes",
    "Must provide implementation services": "Yes",
    "Must offer maintenance and updates": "Yes",
    "Must support at least 1000 concurrent users": "Yes",
    "Must have 99.9% uptime SLA": "Yes",
    "Must provide response times under 2 seconds": "Yes"
}

MOCK_VENDOR_B_EVALUATIONS = {
    "Must support single sign-on (SSO) with SAML 2.0": "Yes",
    "Must provide REST API for integration": "Yes",
    "Must support multi-tenant architecture": "Yes",
    "Must be deployable on-premise or in the cloud": "No",
    "Must provide real-time data synchronization": "No",
    "Data must be encrypted at rest using AES-256": "Yes",
    "Must support role-based access control (RBAC)": "Yes",
    "Must provide audit logging for all user actions": "No",
    "Must comply with SOC 2 Type II standards": "No",
    "Must provide 24/7 technical support via phone and email": "No",
    "Must offer training and documentation": "Yes",
    "Must provide implementation services": "No",
    "Must offer maintenance and updates": "Yes",
    "Must support at least 1000 concurrent users": "No",
    "Must have 99.9% uptime SLA": "No",
    "Must provide response times under 2 seconds": "No"
}

def create_mock_evaluation_matrix():
    """Create a mock evaluation matrix for demonstration."""
    df = pd.DataFrame({"Requirements": MOCK_REQUIREMENTS})
    df["Vendor A"] = df['Requirements'].map(MOCK_VENDOR_A_EVALUATIONS)
    df["Vendor B"] = df['Requirements'].map(MOCK_VENDOR_B_EVALUATIONS)
    return df

def main():
    st.set_page_config(
        page_title="Vendor Evaluation Tool - Demo",
        page_icon="csu.svg",
        layout="wide"
    )
    
    # Apply Pantone red theme to demo
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
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Vendor Evaluation Tool - Demo Mode")
    st.markdown("**This is a demonstration of the vendor evaluation tool using mock data.**")
    st.warning("This is running in demo mode. For full functionality, configure AWS credentials and run `streamlit run main.py`")
    
    # Sidebar for navigation
    st.sidebar.markdown("# Request For Proposal's Made Simple")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")
    workflow = st.sidebar.radio(
        "Select Workflow:",
        ["Workflow 1: RFP Analysis", "Workflow 2: Vendor Proposal Scoring"]
    )
    
    if workflow == "Workflow 1: RFP Analysis":
        st.header("Workflow 1: RFP Analysis & Evaluation Matrix Creation")
        
        st.markdown("""
        **Instructions:**
        1. Upload your Request for Proposal (RFP) PDF file
        2. The system will analyze the document and extract all requirements
        3. An evaluation matrix will be created as a CSV file
        """)
        
        # Demo file uploader
        uploaded_rfp = st.file_uploader(
            "Upload RFP Document (PDF)",
            type=['pdf'],
            help="Upload a single PDF file containing the RFP"
        )
        
        if uploaded_rfp is not None:
            st.success("PDF uploaded successfully! (Demo mode)")
            
            # Show mock extracted text
            with st.expander("View extracted text (first 500 characters)"):
                st.text(MOCK_RFP_TEXT[:500] + "...")
            
            st.info("Analyzing RFP and extracting requirements... (Demo mode)")
            
            # Display mock requirements
            st.success(f"Successfully extracted {len(MOCK_REQUIREMENTS)} requirements!")
            
            st.subheader("Extracted Requirements:")
            for i, req in enumerate(MOCK_REQUIREMENTS, 1):
                st.write(f"{i}. {req}")
            
            # Create evaluation matrix
            if st.button("Create Evaluation Matrix"):
                df = pd.DataFrame({"Requirements": MOCK_REQUIREMENTS})
                df.to_csv("evaluation_matrix.csv", index=False)
                st.success(f"Evaluation matrix created with {len(MOCK_REQUIREMENTS)} requirements!")
                
                # Show the created matrix
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
            st.info("Please upload an RFP PDF file to begin analysis.")
    
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
        if not os.path.exists("evaluation_matrix.csv"):
            st.error("No evaluation matrix found! Please complete Workflow 1 first to create the evaluation matrix.")
            st.info("For demo purposes, you can create a sample matrix:")
            if st.button("Create Sample Evaluation Matrix"):
                df = pd.DataFrame({"Requirements": MOCK_REQUIREMENTS})
                df.to_csv("evaluation_matrix.csv", index=False)
                st.success("Sample evaluation matrix created!")
        
        # Load current evaluation matrix
        if os.path.exists("evaluation_matrix.csv"):
            current_matrix = pd.read_csv("evaluation_matrix.csv")
            st.subheader("Current Evaluation Matrix:")
            st.dataframe(current_matrix)
        else:
            current_matrix = pd.DataFrame()
        
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
            st.success("Proposal uploaded successfully! (Demo mode)")
            
            # Check if vendor already exists in matrix
            if not current_matrix.empty and vendor_name in current_matrix.columns:
                st.warning(f"Vendor '{vendor_name}' already exists in the evaluation matrix. The scores will be updated.")
            
            if st.button("Evaluate Vendor Proposal"):
                st.info("Processing vendor proposal... (Demo mode)")
                
                # Use mock evaluations based on vendor name
                if vendor_name.lower() == "vendor a":
                    vendor_evaluations = MOCK_VENDOR_A_EVALUATIONS
                elif vendor_name.lower() == "vendor b":
                    vendor_evaluations = MOCK_VENDOR_B_EVALUATIONS
                else:
                    # Generate random evaluations for demo
                    import random
                    vendor_evaluations = {req: random.choice(["Yes", "No"]) for req in MOCK_REQUIREMENTS}
                
                # Display evaluation results
                st.subheader(f"Evaluation Results for {vendor_name}:")
                results_df = pd.DataFrame({
                    'Requirement': list(vendor_evaluations.keys()),
                    'Score': list(vendor_evaluations.values())
                })
                st.dataframe(results_df)
                
                # Update evaluation matrix
                if not current_matrix.empty:
                    current_matrix[vendor_name] = current_matrix['Requirements'].map(vendor_evaluations)
                    current_matrix.to_csv("evaluation_matrix.csv", index=False)
                    st.success(f"Evaluation matrix updated with {vendor_name} scores!")
                    
                    # Show updated matrix
                    st.subheader("Updated Evaluation Matrix:")
                    st.dataframe(current_matrix)
                    
                    # Download button
                    csv = current_matrix.to_csv(index=False)
                    st.download_button(
                        label="Download Updated Evaluation Matrix (CSV)",
                        data=csv,
                        file_name="evaluation_matrix.csv",
                        mime="text/csv"
                    )
    
    # Show sample final matrix
    st.sidebar.markdown("---")
    st.sidebar.subheader("Sample Final Matrix")
    sample_matrix = create_mock_evaluation_matrix()
    st.sidebar.dataframe(sample_matrix, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Note:** This is a demo version. For full functionality with Amazon Bedrock LLM, configure AWS credentials and run `streamlit run main.py`")

if __name__ == "__main__":
    main() 