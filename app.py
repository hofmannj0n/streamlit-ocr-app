from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import json

credentials = json.load(open('/Users/jonathanhofmann/Desktop/programming/financial-data-streamlit/credentials.json'))
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
                extracted_text+=line.content+" "

        return extracted_text.strip()


if __name__ == "__main__":
    document_path = "/Users/jonathanhofmann/Desktop/programming/financial-data-streamlit/research_form_filled_out_electronically.pdf"
    extracted_text = extract_text_from_document(document_path)
    print(extracted_text)


