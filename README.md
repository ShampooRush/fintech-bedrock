# Financial Transaction Analyzer

A Streamlit application that analyzes financial transactions and detects suspicious activity using AWS Bedrock with Claude Sonnet 4.

## Features

- 📤 **CSV Upload**: Upload transaction files with date, amount, merchant, and category data
- 📊 **Data Display**: View all transactions in an organized table
- 📈 **Statistics**: Calculate total, average, and category distribution
- 🤖 **AI Analysis**: Detect suspicious transactions using Claude Sonnet 4 via AWS Bedrock

## Requirements

- Python 3.8+
- AWS account with Bedrock access
- AWS credentials configured

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials (one of the following):
   - Set environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - Use AWS CLI: `aws configure`
   - Use IAM role (if running on EC2/ECS)

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown (typically http://localhost:8501)

3. Upload a CSV file with the following columns:
   - `date`: Transaction date
   - `montant`: Transaction amount
   - `marchand`: Merchant name
   - `categorie`: Transaction category

4. View statistics and click "Analyze Transactions with Claude" for AI-powered fraud detection

## Sample Data

A sample CSV file (`sample_transactions.csv`) is included with 20 transactions, including 3 obvious anomalies:
- Unusually high amount from suspicious merchant
- Transfer to suspicious foreign entity
- High-risk gambling/casino transaction

## AWS Bedrock Configuration

- **Region**: us-east-1
- **Model**: Claude Sonnet 4 (anthropic.claude-sonnet-4-20250514-v1:0)
- **Service**: bedrock-runtime

Make sure your AWS account has access to Claude Sonnet 4 in the us-east-1 region.

## File Structure

```
.
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── sample_transactions.csv     # Sample data with anomalies
└── README.md                   # This file
```

## Error Handling

The app handles various error conditions:
- Missing required CSV columns
- Invalid or expired AWS credentials
- Bedrock API failures
- Empty or malformed data files

## License

MIT License - feel free to use and modify as needed.
