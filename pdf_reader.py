import pdfplumber
import csv
import openai
import os
import typer
from secret import OAI_KEY

# OpenAI API credentials
openai.api_key = OAI_KEY

app = typer.Typer()

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text





def extract_transactions_from_pdf(pdf_path):
    # Extract text from the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Send text to ChatGPT to extract transactions
    prompt_with_text = prompt + '\n\n' + text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_with_text,
        max_tokens=500,
        n=1,  # Specify the number of transactions to extract
        stop=None,
        temperature=0.7
    )

    # Parse the transactions
    transactions = []
    for choice in response.choices:
        transaction_text = choice.text.strip()
        transactions.append(transaction_text)

    return transactions

def save_transactions_to_csv(transactions, csv_path):
    # Write transactions to the CSV file
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Transaction'])
        writer.writerows([[transaction] for transaction in transactions])

# Provide the path to your PDF file
pdf_file_path = './example4.pdf'

# Provide the path where you want to save the CSV file
csv_file_path = './chatgptresult.csv'
#Promp for chatGPT
prompt = "Extract the Account transactions section from this bank statement, remove all text except transactions,"\
"ignore ballance summary section"\
"ignore Personal and Group Valuts transactions section"\
"ignore Investment transactions section"\
"arrange data in clear columns with comma separated, "\

# Delete transactions from CSV
def delete_text_from_csv(csv_path):
    # Clear the CSV file
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Text deleted '])
    typer.echo(f"Text deleted from {csv_path}.")

def show_available_options():
    typer.echo("Available options:")
    typer.echo("-r : Read multiple PDF files.")
    typer.echo("-d : Delete text from a CSV file.")
    typer.echo("-h : Show available options.")
    typer.echo()
    typer.echo("Usage examples:")
    typer.echo("  python pdf_reader.py -o -r")
    typer.echo(".\pdfs")
    typer.echo("  python pdf_reader.py -o -d")
    typer.echo(".\csvs\chatgptresult.csv")

    typer.echo("  python pdf_reader.py -o -h")

@app.command()
def process_pdf_files(
    option: str = typer.Option(None, "-o", "--option", help="Select an option: -r to read PDF files, -d to delete text from a CSV file, -h for help.")
):
    if option == '-r':
        directory = typer.prompt("Enter the directory path containing the PDF files:")
        pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory, pdf_file)
            text_transactions = extract_transactions_from_pdf(pdf_path)
            csv_file = os.path.splitext(pdf_file)[0] + ".csv"
            save_transactions_to_csv(text_transactions, csv_file)

    elif option == "-d":
        csv_file_path = typer.prompt("Enter the path to the CSV file:")
        #csv_file_path = pdf_path.replace(".pdf", ".csv")
        delete_text_from_csv(csv_file_path)

    elif option =="-h":
        show_available_options()
    else:
        typer.echo("Invalid option. Please select -r, -d, or -h.")
    


if __name__ == "__main__":
    app() 