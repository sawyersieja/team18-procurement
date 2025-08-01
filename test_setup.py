#!/usr/bin/env python3
"""
Test script to verify the vendor evaluation tool setup.
This script checks dependencies and AWS configuration.
"""

import sys
import importlib
import os
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported."""
    required_packages = [
        'streamlit',
        'boto3',
        'pandas',
        'PyPDF2',
        'json',
        'os',
        'io',
        'dotenv'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please install missing packages using: pip install -r requirements.txt")
        return False
    else:
        print("\nAll packages imported successfully!")
        return True

def test_aws_configuration():
    """Test AWS configuration and Bedrock access."""
    try:
        import boto3
        
        print("\nTesting AWS configuration...")
        
        # Check if .env file exists
        if not os.path.exists('.env'):
            print("✗ .env file not found")
            print("Please create a .env file with your AWS credentials or run: python setup_credentials.py")
            return False
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Get credentials from environment variables
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        session_token = os.getenv("AWS_SESSION_TOKEN")
        region = os.getenv("AWS_DEFAULT_REGION", "us-west-2")
        
        if not access_key or not secret_key:
            print("✗ AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required in .env file")
            print("Please create a .env file with your AWS credentials or run: python setup_credentials.py")
            return False
        
        print("✓ .env file found and loaded")
        
        # Create session with credentials from environment variables
        session_kwargs = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'region_name': region
        }
        
        if session_token:
            session_kwargs['aws_session_token'] = session_token
            print("✓ Session token found")
        
        session = boto3.Session(**session_kwargs)
        
        # Test basic AWS access
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"✓ AWS credentials valid - User: {identity.get('Arn', 'Unknown')}")
        
        # Test Bedrock client creation
        bedrock_client = session.client('bedrock-runtime', region_name=region)
        print("✓ Bedrock client created successfully")
        
        # Test if we can list models (this requires Bedrock access)
        try:
            bedrock_models = session.client('bedrock', region_name=region)
            models = bedrock_models.list_foundation_models()
            print(f"✓ Bedrock access confirmed - {len(models.get('modelSummaries', []))} models available")
            return True
        except Exception as e:
            print(f"✗ Bedrock access test failed: {e}")
            print("Please ensure your AWS account has access to Amazon Bedrock")
            return False
            
    except Exception as e:
        print(f"✗ AWS configuration test failed: {e}")
        return False

def test_pdf_processing():
    """Test PDF processing capabilities."""
    try:
        import PyPDF2
        print("\nTesting PDF processing...")
        print("✓ PyPDF2 imported successfully")
        return True
    except Exception as e:
        print(f"✗ PDF processing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Vendor Evaluation Tool - Setup Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test AWS configuration
    aws_ok = test_aws_configuration()
    
    # Test PDF processing
    pdf_ok = test_pdf_processing()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Package Imports: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"AWS Configuration: {'✓ PASS' if aws_ok else '✗ FAIL'}")
    print(f"PDF Processing: {'✓ PASS' if pdf_ok else '✗ FAIL'}")
    
    if all([imports_ok, aws_ok, pdf_ok]):
        print("\n🎉 All tests passed! You're ready to run the vendor evaluation tool.")
        print("Run: streamlit run main.py --server.port 8501")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above before running the application.")
        if not aws_ok:
            print("\n💡 To set up AWS credentials, create a .env file or run:")
            print("python setup_credentials.py")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 