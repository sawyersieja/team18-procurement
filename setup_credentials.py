#!/usr/bin/env python3
"""
Helper script to set up AWS credentials for the Vendor Evaluation Tool.
"""

import os
import sys

def create_env_file():
    """Create a .env file with AWS credentials."""
    print("Setting up AWS credentials for the Vendor Evaluation Tool")
    print("=" * 60)
    
    # Check if .env file already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
    
    print("\nPlease enter your AWS credentials:")
    print("(You can find these in your AWS Console under IAM → Users → Security credentials)")
    print("\nNote: If you're using temporary credentials (from AWS SSO, STS, etc.),")
    print("you'll also need to provide a session token.")
    
    # Get credentials from user
    access_key = input("\nAWS Access Key ID: ").strip()
    secret_key = input("AWS Secret Access Key: ").strip()
    
    # Ask about session token
    print("\nDo you have a session token? (y/N): ", end="")
    has_session_token = input().strip().lower() == 'y'
    
    session_token = ""
    if has_session_token:
        session_token = input("AWS Session Token: ").strip()
    
    region = input("AWS Region (default: us-west-2): ").strip() or "us-west-2"
    
    # Validate inputs
    if not access_key or not secret_key:
        print("❌ Access Key ID and Secret Access Key are required!")
        return False
    
    # Create .env file content
    env_content = f"""# AWS Credentials for Vendor Evaluation Tool
AWS_ACCESS_KEY_ID={access_key}
AWS_SECRET_ACCESS_KEY={secret_key}"""
    
    if session_token:
        env_content += f"\nAWS_SESSION_TOKEN={session_token}"
    
    env_content += f"""
AWS_DEFAULT_REGION={region}

# Optional: Bedrock Model Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
"""
    
    try:
        # Write .env file
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")
        
        # Test credentials
        print("\n🔍 Testing AWS credentials...")
        test_result = test_credentials(access_key, secret_key, session_token, region)
        
        if test_result:
            print("✅ AWS credentials are valid!")
            print("\n🎉 Setup complete! You can now run the application:")
            print("   streamlit run main.py")
        else:
            print("❌ AWS credentials test failed. Please check your credentials.")
            print("   Make sure you have access to Amazon Bedrock in your AWS account.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_credentials(access_key, secret_key, session_token, region):
    """Test if the AWS credentials are valid."""
    try:
        import boto3
        
        # Create a session with the provided credentials
        session_kwargs = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'region_name': region
        }
        
        if session_token:
            session_kwargs['aws_session_token'] = session_token
        
        session = boto3.Session(**session_kwargs)
        
        # Test basic AWS access
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"   ✅ Authenticated as: {identity.get('Arn', 'Unknown')}")
        
        # Test Bedrock access
        bedrock = session.client('bedrock', region_name=region)
        models = bedrock.list_foundation_models()
        print(f"   ✅ Bedrock access confirmed - {len(models.get('modelSummaries', []))} models available")
        
        return True
        
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    """Main function."""
    print("Vendor Evaluation Tool - AWS Credentials Setup")
    print("=" * 60)
    
    # Check if python-dotenv is installed
    try:
        import dotenv
    except ImportError:
        print("❌ python-dotenv is not installed!")
        print("Please install it first:")
        print("   pip install python-dotenv")
        return 1
    
    # Check if boto3 is installed
    try:
        import boto3
    except ImportError:
        print("❌ boto3 is not installed!")
        print("Please install it first:")
        print("   pip install boto3")
        return 1
    
    # Create .env file
    success = create_env_file()
    
    if success:
        print("\n📋 Next steps:")
        print("1. Make sure you have access to Amazon Bedrock in your AWS account")
        print("2. Run: streamlit run main.py")
        print("3. Upload your RFP and vendor proposal PDF files")
        return 0
    else:
        print("\n❌ Setup failed. Please try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 