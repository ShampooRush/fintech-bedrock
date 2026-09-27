import streamlit as st
import pandas as pd
import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError

# Page configuration
st.set_page_config(
    page_title="Financial Transaction Analyzer",
    page_icon="💰",
    layout="wide"
)

# Initialize Bedrock client
@st.cache_resource
def get_bedrock_client():
    """Initialize and return the AWS Bedrock client"""
    try:
        client = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'
        )
        return client
    except NoCredentialsError:
        st.error("❌ AWS credentials not found. Please configure your AWS credentials.")
        return None
    except Exception as e:
        st.error(f"❌ Failed to initialize Bedrock client: {str(e)}")
        return None

def analyze_transactions_with_claude(df, bedrock_client):
    """Send transaction data to Claude via Bedrock for analysis"""
    
    if bedrock_client is None:
        return "Cannot analyze transactions - Bedrock client not initialized."
    
    # Prepare transaction summary for Claude
    transaction_summary = df.to_string(index=False)
    
    # Create the prompt for Claude
    prompt = f"""Analyze the following financial transactions and identify any suspicious or unusual transactions.

Transaction Data:
{transaction_summary}

Please:
1. Identify any transactions that appear suspicious or unusual
2. Explain in English why each flagged transaction is suspicious (e.g., unusually high amount, suspicious merchant name, unusual category)
3. If no suspicious transactions are found, state that clearly

Provide your analysis in a clear, structured format."""

    # Prepare the request body for Claude Sonnet 5
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        # Invoke Claude Sonnet 5 via Bedrock
        response = bedrock_client.invoke_model(
            modelId='global.anthropic.claude-sonnet-5',
            body=json.dumps(request_body)
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        analysis = response_body['content'][0]['text']
        
        return analysis
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return f"❌ Bedrock API error ({error_code}): {error_message}"
    except Exception as e:
        return f"❌ Error analyzing transactions: {str(e)}"

def calculate_statistics(df):
    """Calculate summary statistics from transaction data"""
    
    if df.empty:
        return {
            'total': 0.00,
            'average': 0.00,
            'by_category': pd.DataFrame(columns=['Category', 'Count', 'Total Amount'])
        }
    
    # Handle missing categories
    df['categorie'] = df['categorie'].fillna('Uncategorized')
    
    # Calculate statistics
    total = round(df['montant'].sum(), 2)
    average = round(df['montant'].mean(), 2)
    
    # Group by category
    category_stats = df.groupby('categorie').agg(
        Count=('categorie', 'count'),
        Total_Amount=('montant', lambda x: round(x.sum(), 2))
    ).reset_index()
    category_stats.columns = ['Category', 'Count', 'Total Amount']
    
    return {
        'total': total,
        'average': average,
        'by_category': category_stats
    }

def validate_csv(df):
    """Validate that the CSV has required columns"""
    required_columns = ['date', 'montant', 'marchand', 'categorie']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, missing_columns
    return True, []

# Main app
def main():
    st.title("💰 Financial Transaction Analyzer")
    st.markdown("### Analyze your transactions and detect suspicious activity using AI")
    
    # Initialize Bedrock client
    bedrock_client = get_bedrock_client()
    
    st.markdown("---")
    
    # File upload section
    st.header("📤 Upload Transaction Data")
    st.markdown("Upload a CSV file with columns: **date**, **montant**, **marchand**, **categorie**")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read and parse the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Validate the CSV structure
            is_valid, missing_cols = validate_csv(df)
            
            if not is_valid:
                st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                st.stop()
            
            # Filter out rows with missing required values
            original_count = len(df)
            df = df.dropna(subset=['date', 'montant', 'marchand', 'categorie'])
            filtered_count = original_count - len(df)
            
            if filtered_count > 0:
                st.warning(f"⚠️ Excluded {filtered_count} transaction(s) with missing data")
            
            st.success("✅ File uploaded and parsed successfully!")
            
            # Display transaction data
            st.markdown("---")
            st.header("📊 Transaction Data")
            
            if df.empty:
                st.info("No valid transactions found in the file")
                st.dataframe(pd.DataFrame(columns=['date', 'montant', 'marchand', 'categorie']))
            else:
                st.dataframe(df, use_container_width=True)
            
            # Calculate and display statistics
            st.markdown("---")
            st.header("📈 Statistics")
            
            stats = calculate_statistics(df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Amount", f"${stats['total']:,.2f}")
            with col2:
                st.metric("Average Transaction", f"${stats['average']:,.2f}")
            
            st.subheader("Distribution by Category")
            if not stats['by_category'].empty:
                st.dataframe(stats['by_category'], use_container_width=True)
            else:
                st.info("No transactions to display")
            
            # AI Analysis section
            st.markdown("---")
            st.header("🤖 AI Fraud Detection")
            
            if not df.empty:
                if st.button("🔍 Analyze Transactions with Claude", type="primary"):
                    with st.spinner("Analyzing transactions with Claude..."):
                        analysis = analyze_transactions_with_claude(df, bedrock_client)
                        st.markdown("### Analysis Results")
                        st.markdown(analysis)
            else:
                st.info("No transactions available for analysis")
                
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
    else:
        st.info("👆 Please upload a CSV file to begin analysis")

if __name__ == "__main__":
    main()
