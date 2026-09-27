# Requirements Document

## Introduction

This document specifies the requirements for a Streamlit-based financial transaction analysis application. The application allows users to upload CSV files containing synthetic financial transaction data, displays transaction statistics, and leverages Amazon Bedrock with Claude Sonnet 3.5 to identify suspicious or unusual transactions with explanations.

## Glossary

- **Application**: The Streamlit web application for transaction analysis
- **Transaction_File**: A CSV file containing financial transaction data with columns: date, montant, marchand, categorie
- **Transaction_Data**: The parsed data structure containing all transactions from the uploaded file
- **Statistics_Display**: The component showing calculated metrics (total, average, category distribution)
- **Bedrock_Client**: The AWS boto3 bedrock-runtime client for invoking Claude
- **Suspicion_Analysis**: The AI-generated report identifying unusual transactions with explanations
- **Sample_File**: The example CSV file with 20 synthetic transactions including 2-3 anomalies

## Requirements

### Requirement 1: CSV File Upload

**User Story:** As a user, I want to upload a CSV file of financial transactions, so that I can analyze the transaction data.

#### Acceptance Criteria

1. THE Application SHALL provide a file upload widget that accepts .csv files
2. WHEN a CSV file is uploaded, THE Application SHALL parse the file expecting columns: date, montant, marchand, categorie
3. IF the uploaded file is missing required columns, THEN THE Application SHALL display an error message indicating which columns are missing
4. WHEN a valid CSV file is parsed, THE Application SHALL store the Transaction_Data in memory for further processing

### Requirement 2: Transaction Display

**User Story:** As a user, I want to view all transactions in a table, so that I can review the raw data.

#### Acceptance Criteria

1. WHEN a CSV file containing transaction data has been successfully uploaded and parsed, THE Application SHALL display all valid transactions in a tabular format
2. WHEN displaying transactions, THE Application SHALL display the columns: date, montant, marchand, categorie for each transaction
3. WHEN displaying transactions, THE Application SHALL preserve the original order of transactions from the uploaded file
4. IF the uploaded file contains zero transactions, THEN THE Application SHALL display an empty table with column headers
5. IF a transaction record is missing required column values (date, montant, marchand, or categorie), THEN THE Application SHALL exclude that transaction from the display

### Requirement 3: Statistics Calculation

**User Story:** As a user, I want to see summary statistics of my transactions, so that I can understand spending patterns.

#### Acceptance Criteria

1. WHEN Transaction_Data contains at least one transaction, THE Statistics_Display SHALL calculate the total sum of all montant values rounded to 2 decimal places
2. WHEN Transaction_Data contains at least one transaction, THE Statistics_Display SHALL calculate the average of all montant values rounded to 2 decimal places
3. WHEN Transaction_Data contains at least one transaction, THE Statistics_Display SHALL calculate the count of transactions grouped by categorie
4. WHEN Transaction_Data contains at least one transaction, THE Statistics_Display SHALL calculate the total montant per categorie rounded to 2 decimal places
5. IF Transaction_Data contains zero transactions, THEN THE Statistics_Display SHALL display a total sum of 0.00
6. IF Transaction_Data contains zero transactions, THEN THE Statistics_Display SHALL display an average of 0.00
7. IF Transaction_Data contains zero transactions, THEN THE Statistics_Display SHALL display zero transactions for all categories
8. IF a transaction has a null or missing categorie value, THEN THE Statistics_Display SHALL group it under an "Uncategorized" category

### Requirement 4: AWS Bedrock Integration

**User Story:** As a developer, I want to configure AWS Bedrock client correctly, so that the application can communicate with Claude.

#### Acceptance Criteria

1. WHEN THE Application starts, THE Bedrock_Client SHALL be initialized using boto3 with service name bedrock-runtime
2. THE Bedrock_Client SHALL be configured to use region us-east-1
3. THE Bedrock_Client SHALL use model identifier anthropic.claude-3-5-sonnet-20241022-v2:0
4. IF AWS credentials are missing, THEN THE Application SHALL display an error message indicating authentication failure
5. IF AWS credentials are invalid or expired, THEN THE Application SHALL display an error message indicating authentication failure
6. IF Bedrock_Client initialization fails, THEN THE Application SHALL display an error message indicating configuration failure

### Requirement 5: Suspicious Transaction Detection

**User Story:** As a user, I want Claude to analyze my transactions and identify suspicious ones, so that I can detect potential fraud or anomalies.

#### Acceptance Criteria

1. WHEN Transaction_Data is available, THE Application SHALL generate a summary of all transactions formatted for Claude analysis
2. THE Application SHALL send the transaction summary to Claude via the Bedrock_Client
3. THE Application SHALL request Claude to identify suspicious or unusual transactions
4. THE Application SHALL request Claude to explain in English why each flagged transaction is suspicious
5. WHEN Claude returns the Suspicion_Analysis, THE Application SHALL display the analysis results to the user
6. IF the Bedrock API call fails, THEN THE Application SHALL display an error message with the failure reason

### Requirement 6: Sample Data Generation

**User Story:** As a user, I want an example CSV file to test the application, so that I can see how it works without creating my own data.

#### Acceptance Criteria

1. THE Sample_File SHALL contain exactly 20 synthetic financial transactions
2. THE Sample_File SHALL include columns: date, montant, marchand, categorie in the header row
3. THE Sample_File SHALL include 2 to 3 transactions with obvious anomalies for testing detection
4. THE Sample_File SHALL include anomalies such as unusually high montant values or suspicious marchand names
5. THE Sample_File SHALL use realistic date formats, merchant names, and category values for normal transactions

### Requirement 7: Dependencies Management

**User Story:** As a developer, I want a requirements file listing all dependencies, so that I can install the necessary packages.

#### Acceptance Criteria

1. THE Application SHALL provide a requirements.txt file in the project root directory
2. THE requirements.txt file SHALL include streamlit as a dependency
3. THE requirements.txt file SHALL include boto3 as a dependency
4. THE requirements.txt file SHALL include pandas as a dependency
5. THE requirements.txt file SHALL specify version constraints for streamlit, boto3, and pandas using valid pip version specifier syntax (==, >=, ~=, or compatible release notation)
6. THE requirements.txt file SHALL use standard pip requirements file format with one dependency per line

### Requirement 8: User Interface Layout

**User Story:** As a user, I want a clear and organized interface, so that I can easily navigate the application features.

#### Acceptance Criteria

1. THE Application SHALL display a title describing the application purpose
2. THE Application SHALL organize the interface into logical sections: upload, data display, statistics, and AI analysis
3. WHEN no file is uploaded, THE Application SHALL display instructions for uploading a Transaction_File
4. WHEN Transaction_Data is available, THE Application SHALL display all sections in a logical reading order

