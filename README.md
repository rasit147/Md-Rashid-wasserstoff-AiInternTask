# Domain-Specific PDF Summarization and Keyword Extraction
This project processes PDFs from URLs, which is stored in json folder.Categorizes them by length (short, medium, long), generates concise summaries, and extracts domain-specific keywords. The results are stored in a MongoDB database. The application is built using Python and provides a user interface through Streamlit for ease of use.

## Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Setup Instructions](#setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Explanation of the Solution](#explanation-of-the-solution)
- [Output](#output)

Features
PDF Text Extraction: Extract text from PDF files provided via URLs.
PDF Categorization: Automatically categorize PDFs into short, medium, or long based on the number of pages.
Summarization: Generate summaries based on the length of the document using TF-IDF-based sentence ranking.
Keyword Extraction: Extract domain-specific keywords using the TF-IDF technique.
MongoDB Integration: Store the processed data (summaries, keywords,page number,category etc.) in MongoDB for easy retrieval.
System Requirements
Ensure your system has the following prerequisites:

Python 3.10.5
MongoDB: Ensure that you have a MongoDB instance running, either locally or through a service such as MongoDB Atlas.
Internet Connection: Required to fetch PDF files from URLs.
Python Dependencies:
The required Python libraries are specified in the requirements.txt file. These libraries include:

requests
PyPDF2
pymongo
streamlit
scikit-learn
