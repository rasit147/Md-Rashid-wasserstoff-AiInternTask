# Domain-Specific PDF Summarization and Keyword Extraction
This project processes PDFs from URLs, which is stored in json folder.Categorizes them by length (short, medium, long), generates concise summaries, and extracts domain-specific keywords. The results are stored in a MongoDB database. The application is built using Python and provides a user interface through Streamlit for ease of use.

## Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Setup Instructions](#setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Explanation of the Solution](#explanation-of-the-solution)
- [Output](#output)


## Features
- **PDF Text Extraction**: Extract text from PDF files provided via URLs.
- **PDF Categorization**: Automatically categorize PDFs into short, medium, or long based on the number of pages.
- **Summarization**: Generate summaries using TF-IDF-based sentence ranking.
- **Keyword Extraction**: Extract domain-specific keywords using the TF-IDF technique.
- **MongoDB Integration**: Store processed data (summaries, keywords, etc.) in MongoDB for easy retrieval.

## System Requirements
Ensure your system has the following prerequisites:
- **Python**: 3.10.5

### Python Dependencies
The required Python libraries are specified in the `requirements.txt` file:
- requests
- PyPDF2
- pymongo
- streamlit
- scikit-learn
 
# Usage Instructions
MongoDB Connection: Enter your MongoDB connection URL into the provided input field in the Streamlit interface.

Note: Used MongoDB connection URL for which have access from anywhere and for active cluster.

Example for MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/mydatabase?retryWrites=true&w=majority
Upload JSON File: The app allows you to upload a JSON file containing URLs to PDFs you wish to process in this format:
For json folder pdf links will be in this format
{
  "document1": "https://example.com/pdf1.pdf",
  "document2": "https://example.com/pdf2.pdf"
}
# Explanation of the Solution
The solution implements a pipeline to process multiple PDFs using Python and MongoDB:

Extract Text from PDFs: Uses the PyPDF2 library to extract text from each PDF accessed via URLs.

#Categorization: Categorizes PDFs based on page count:

Short: ≤ 10 pages
Medium: 11 - 30 pages
Long: > 30 pages
Summarization: Utilizes TF-IDF to rank sentences and generate summaries, which may take between 130 to 210 seconds for the whole PDF processing. The processing time is stored in MongoDB documents for each individual PDF.

Keyword Extraction: Identifies important keywords using TF-IDF while excluding common stop words.

MongoDB Storage: Stores extracted text, summaries, keywords, and metadata for easy retrieval.

The project consists of five main functions, including the main function to handle the processing pipeline. I have avoided using pre-trained models like Hugging Face Transformers, instead relying on TfidfVectorizer and PyPDF2 for text extraction. For local MongoDB connections, PDF processing is efficient and fast, but for live server data storage, it may take a bit more time.

Output
![webinterfacepdf](https://github.com/user-attachments/assets/0783d0cd-d670-4c76-af1a-89de1cf1c649)
![IMG_20241014_033601](https://github.com/user-attachments/assets/47915c09-c1d3-4139-b1a6-0e5f3adc8a89)

Summaries: The generated summaries of PDFs, based on document length, are stored in MongoDB.
Keywords: Extracted domain-specific keywords are saved in the database.
MongoDB Storage: All processed data, including URLs, page counts, categories, summaries, keywords, and processing time, are saved in the MongoDB collection.

