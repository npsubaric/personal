import os
import pdfplumber
import pandas as pd

def extract_transactions(pdf_path):
    data = []  # List to store all transactions
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                if line.strip() and '/' in line[:5]:
                    parts = line.split()  # Split line into parts
                    date = parts[0]
                    description = ' '.join(parts[1:-2])  # Combine all parts except the last two as description
                    amount = parts[-2]
                    balance = parts[-1]
                    data.append([date, description, amount, balance])

    df = pd.DataFrame(data, columns=['Date', 'Description', 'Amount', 'Balance'])
    return df

def main():
    # Prompt user for folder containing PDF files
    folder_path = input("Enter the path to the folder containing PDF files: ")

    # List PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    # Create an empty list to store DataFrames from each PDF file
    dfs = []

    for pdf_file in pdf_files:
        # Construct full path to PDF file
        pdf_path = os.path.join(folder_path, pdf_file)

        # Extract transactions from PDF file
        df_transactions = extract_transactions(pdf_path)
        
        # Append DataFrame to list
        dfs.append(df_transactions)

    # Concatenate DataFrames
    df_combined = pd.concat(dfs, ignore_index=True)

    # Default output Excel file path
    excel_path = os.path.join(folder_path, "combined_transactions.xlsx")

    # Save the combined DataFrame to an Excel file
    df_combined.to_excel(excel_path, index=False)

    print(f"Data saved to Excel successfully at {excel_path}!")

if __name__ == "__main__":
    main()
