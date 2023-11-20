import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import json
import os

# Load Azure Form Recognizer credentials from JSON file
credentials_path = '/Users/jonathanhofmann/Desktop/programming/financial-data-streamlit/credentials.json'
credentials = json.load(open(credentials_path))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']

def extract_text_from_document(document_path):
    document_analysis = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

    with open(document_path, 'rb') as f:
        poller = document_analysis.begin_analyze_document("prebuilt-document", f.read())
        result = poller.result()

        extracted_text = " "

        for page in result.pages:
            for line in page.lines:
                extracted_text += line.content + " "

        return extracted_text.strip()

def main():
    st.title("Azure Form Recognizer OCR App")

    # Upload PDF file through Streamlit
    uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

    if uploaded_file is not None:
        # Display the uploaded PDF file
        st.write("Uploaded PDF file:", uploaded_file.name)

        # Perform OCR using Azure Form Recognizer
        st.write("Running OCR...")

        # Save the uploaded file temporarily
        temp_file_path = "/tmp/uploaded_pdf.pdf"
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(uploaded_file.read())

        # Extract and format text from the document
        extracted_text = extract_text_from_document(temp_file_path)

        # Display the extracted text
        st.subheader("Extracted Text:")
        st.text_area("Text", extracted_text)

        # Remove the temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()
