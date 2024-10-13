
import os
import requests
import PyPDF2
import pymongo
from pymongo import MongoClient
from io import BytesIO
import logging
import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
import time

# Set up logging to capture any errors during the processing
logging.basicConfig(filename='error_log.log', level=logging.ERROR)

def extract_text_from_pdf(url):
    """Extracted text from a PDF file accessed via a URL."""
    text = ""  # Initialized an empty string to store extracted text
    try:
        # Made a GET request to the provided URL to fetch the PDF
        response = requests.get(url)
        response.raise_for_status()  # Checked for any HTTP errors in the response
        with BytesIO(response.content) as file:
            # Read the PDF file from the response content
            reader = PyPDF2.PdfReader(file)
            for page in range(len(reader.pages)):
                # Extracted text from each page and added it to the text variable
                page_text = reader.pages[page].extract_text() or ''
                text += page_text
        if not text.strip():  # Checked if any text was extracted
            logging.error(f"No text extracted from {url}")  # Logged an error if no text was found
    except Exception as e:
        logging.error(f"Error reading PDF from {url}: {e}")  # Logged any exceptions encountered
        return "", 0  # Returned empty text and 0 pages in case of an error
    return text, len(reader.pages)  # Returned the extracted text and the number of pages

def categorize_pdf(page_count):
    """Categorized PDF based on the number of pages."""
    # Determined the category of the PDF based on its page count
    if page_count <= 10:
        return "short"  # Returned "short" if pages are 10 or less
    elif 10 < page_count <= 30:
        return "medium"  # Returned "medium" for pages between 11 and 30
    else:
        return "long"  # Returned "long" for pages greater than 30

def summarize_text(text, page_count):
    """Summarized text based on the document length."""
    if not text.strip():  # Checked if the text is empty
        logging.error("Cannot summarize empty text.")  # Logged an error if empty
        return ""  # Returned empty summary

    # Split the text into sentences for summarization
    sentences = text.split('. ')
    num_sentences = min(len(sentences), 3)  # Set a default of 3 sentences for summary

    # Adjusted the number of sentences for summary based on the document length
    if page_count <= 10:
        num_sentences = min(len(sentences), 3)  # Concise summary for short documents
    elif 10 < page_count <= 30:
        num_sentences = min(len(sentences), 5)  # Moderate detail for medium documents
    else:
        num_sentences = min(len(sentences), 7)  # Detailed summary for long documents

    # Used TF-IDF to rank sentences based on their importance
    vectorizer = TfidfVectorizer().fit_transform(sentences)  # Fitted the vectorizer on the sentences
    vectors = vectorizer.toarray()  # Converted the result to a dense array
    # Ranked sentences based on their TF-IDF scores and selected the top sentences for the summary
    ranked_sentences = [sentences[i] for i in vectors.sum(axis=1).argsort()[-num_sentences:]]

    # Returned the summary while maintaining the original sentence order
    return ' '.join(sorted(ranked_sentences, key=lambda x: sentences.index(x)))

def extract_keywords(text, num_keywords=5):
    """Extracted domain-specific keywords using TF-IDF."""
    # Created a TF-IDF vectorizer to identify keywords from the text
    vectorizer = TfidfVectorizer(stop_words='english', max_features=num_keywords)
    vectors = vectorizer.fit_transform([text])  # Fitted the vectorizer on the provided text
    keywords = vectorizer.get_feature_names_out().tolist()  # Obtained the keywords as a list

    # Filtered out generic or irrelevant keywords based on their length
    filtered_keywords = [kw for kw in keywords if len(kw) > 3]  # Ensured keywords have more than 3 characters
    return filtered_keywords  # Returned the filtered keywords

def process_pdf_from_url(url, mongodb_url, processing_time):
    """Processed a PDF from a URL and stored results in MongoDB."""
    client = MongoClient(mongodb_url)  # Connected to the MongoDB database using the provided URL
    db = client['pdf_database']  # Accessed the 'pdf_database'
    collection = db['pdf_documents']  # Accessed the 'pdf_documents' collection within the database

    text, page_count = extract_text_from_pdf(url)  # Extracted text and page count from the PDF
    if not text:  # Checked if no text was extracted
        logging.error(f"No text extracted for {url}. Skipping.")  # Logged the error and skipped processing
        return  # Exited the function if no text

    category = categorize_pdf(page_count)  # Categorized the PDF based on its page count
    summary = summarize_text(text, page_count)  # Summarized the extracted text
    keywords = extract_keywords(text)  # Extracted keywords from the text

    # Created a metadata dictionary to store all relevant information
    metadata = {
        "url": url,  # Stored the URL of the PDF
        "num_pages": page_count,  # Stored the number of pages
        "category": category,  # Stored the category of the PDF
        "summary": summary,  # Stored the generated summary
        "keywords": keywords,  # Stored the extracted keywords
        "processing_time": processing_time  # Stored the time taken for processing
    }

    collection.insert_one(metadata)  # Inserted the metadata into the MongoDB collection
    print(f"Processed and stored data for {url}")  # Printed confirmation of processing

def main():
    """Main function to run the pipeline."""
    st.title("Domain-Specific PDF Summarization and Keyword Extraction Pipeline")  # Set the title for the Streamlit web application

    # Input field for MongoDB connection URL
    mongodb_url = st.text_input("Enter your MongoDB connection URL")
    
    if mongodb_url:  # Checked if the user provided a MongoDB URL these is for the other user
        # Optional: Tested the MongoDB connection
        try:
            client = MongoClient(mongodb_url)  # Attempted to connect to MongoDB
            client.admin.command('ping')  # Simple ping command to check connection status
            st.success("MongoDB connection established for you.")  # Displayed success message if connection was successful
        except Exception as e:
            st.error(f"Error connecting to MongoDB: {e}")  # Displayed error message if connection failed
            return  # Exited the function on connection failure
    

        # User selects a JSON file from the local system
        json_file = st.file_uploader("Upload JSON File", type="json")
        
        
        if json_file is not None:  # Checked if a JSON file was uploaded
            pdf_links = json.load(json_file)  # Loaded the PDF links from the JSON file

            # Started processing the PDFs
            start_time = time.time()  # Recorded the start time of processing
            st.write("Processing PDFs... Please wait.")  
            for pdf_name, url in pdf_links.items():  # Iterated through each PDF name and URL in the JSON file
                process_pdf_from_url(url, mongodb_url, time.time() - start_time)  # Processed each PDF and passed the elapsed time

            processing_time = time.time() - start_time  # Calculated total processing time
            # Displayed a success message with the total processing time
            st.success(f"PDFs processed successfully in {processing_time:.2f} seconds. You can view the stored data in your MongoDB.")

if __name__ == "__main__":
    main()  # Called the main function to execute the script


