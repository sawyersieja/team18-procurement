#!/usr/bin/env python3
"""
Example usage of the Vendor Evaluation Tool classes.
This script demonstrates how to use the tool programmatically.
"""

import os
from main import BedrockLLM, PDFProcessor, VendorEvaluator

def example_rfp_analysis():
    """Example of analyzing an RFP document."""
    print("=== Example: RFP Analysis ===")
    
    # Initialize the evaluator
    evaluator = VendorEvaluator()
    
    # Example RFP text (in real usage, this would come from a PDF)
    example_rfp_text = """
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
    
    print("Analyzing RFP document...")
    requirements = evaluator.analyze_rfp(example_rfp_text)
    
    print(f"\nExtracted {len(requirements)} requirements:")
    for i, req in enumerate(requirements, 1):
        print(f"{i}. {req}")
    
    # Create evaluation matrix
    evaluator.create_evaluation_matrix(requirements)
    print(f"\nEvaluation matrix created: {evaluator.evaluation_matrix_file}")
    
    return requirements

def example_vendor_evaluation(requirements):
    """Example of evaluating vendor proposals."""
    print("\n=== Example: Vendor Proposal Evaluation ===")
    
    evaluator = VendorEvaluator()
    
    # Example vendor proposal text
    vendor_a_proposal = """
    VENDOR A PROPOSAL
    
    Technical Capabilities:
    - We provide comprehensive SSO support including SAML 2.0 integration
    - Our platform offers a complete REST API suite for seamless integration
    - Multi-tenant architecture is a core feature of our solution
    - We support both cloud and on-premise deployment options
    - Real-time data synchronization is available through our platform
    
    Security Features:
    - All data is encrypted using AES-256 encryption at rest
    - We implement comprehensive RBAC with granular permissions
    - Complete audit logging is provided for compliance
    - Our solution is SOC 2 Type II certified
    
    Support Services:
    - 24/7 technical support available via phone and email
    - Comprehensive training programs and documentation
    - Professional implementation services included
    - Regular maintenance and updates provided
    
    Performance:
    - Supports up to 2000 concurrent users
    - 99.95% uptime SLA guaranteed
    - Average response time of 1.5 seconds
    """
    
    vendor_b_proposal = """
    VENDOR B PROPOSAL
    
    Technical Capabilities:
    - SSO support with SAML 2.0 available
    - REST API provided for integrations
    - Multi-tenant architecture supported
    - Cloud deployment only (no on-premise option)
    - Batch data processing (not real-time)
    
    Security Features:
    - AES-256 encryption for data at rest
    - Basic role-based access control
    - Limited audit logging capabilities
    - Working towards SOC 2 compliance
    
    Support Services:
    - Business hours support only (8 AM - 6 PM EST)
    - Basic documentation provided
    - Self-service implementation
    - Quarterly updates
    
    Performance:
    - Supports up to 500 concurrent users
    - 99% uptime SLA
    - Response times vary (2-5 seconds)
    """
    
    # Evaluate Vendor A
    print("Evaluating Vendor A proposal...")
    vendor_a_evaluations = evaluator.evaluate_vendor_proposal(
        vendor_a_proposal, requirements, "Vendor A"
    )
    
    # Evaluate Vendor B
    print("Evaluating Vendor B proposal...")
    vendor_b_evaluations = evaluator.evaluate_vendor_proposal(
        vendor_b_proposal, requirements, "Vendor B"
    )
    
    # Update evaluation matrix
    evaluator.update_evaluation_matrix(vendor_a_evaluations, "Vendor A")
    evaluator.update_evaluation_matrix(vendor_b_evaluations, "Vendor B")
    
    # Display results
    final_matrix = evaluator.get_evaluation_matrix()
    print("\nFinal Evaluation Matrix:")
    print(final_matrix.to_string(index=False))
    
    return final_matrix

def main():
    """Run the example workflow."""
    print("Vendor Evaluation Tool - Example Usage")
    print("=" * 50)
    
    try:
        # Step 1: Analyze RFP
        requirements = example_rfp_analysis()
        
        # Step 2: Evaluate vendors
        final_matrix = example_vendor_evaluation(requirements)
        
        print("\n" + "=" * 50)
        print("Example completed successfully!")
        print(f"Evaluation matrix saved to: {evaluator.evaluation_matrix_file}")
        
        # Show summary
        if not final_matrix.empty:
            vendors = [col for col in final_matrix.columns if col != 'Requirements']
            print(f"\nSummary:")
            print(f"- Total requirements: {len(final_matrix)}")
            print(f"- Vendors evaluated: {len(vendors)}")
            
            for vendor in vendors:
                yes_count = (final_matrix[vendor] == 'Yes').sum()
                total = len(final_matrix)
                percentage = (yes_count / total) * 100
                print(f"- {vendor}: {yes_count}/{total} requirements met ({percentage:.1f}%)")
        
    except Exception as e:
        print(f"Error running example: {e}")
        print("Please ensure AWS credentials are configured and Bedrock access is available.")

if __name__ == "__main__":
    main() 