import streamlit as st
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import PyPDF2

nltk.download('punkt')
nltk.download('stopwords')

# Function to check if a string contains numeric characters
def contains_numbers(s):
    return any(char.isdigit() for char in s)

# Function to check if a sentence resembles a table (basic check)
def resembles_table(sentence):
    # Check if the sentence contains a significant number of words or characters common in tables
    return len(word_tokenize(sentence)) > 20 or re.search(r'\b(?:\d+\s*){3,}', sentence) is not None

# Function to extract important sentences and tabular data from a PDF based on keywords
def extract_important_data_from_pdf(pdf_path, keywords):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize lists to store important sentences and tabular data
        important_sentences = []
        tabular_data = []
        
        # Iterate through each page in the PDF
        for page in pdf_reader.pages:
            # Extract text from the page
            page_text = page.extract_text()
            
            # Tokenize the page text into sentences
            sentences = sent_tokenize(page_text)
            
            # Tokenize the page text into words
            words = word_tokenize(page_text)
            
            # Remove stopwords from the words
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word.lower() not in stop_words]
            
            # Iterate through each sentence in the page
            for sentence in sentences:
                # Check if the sentence contains numbers (potential table)
                if contains_numbers(sentence):
                    # If the sentence resembles a table, add it to tabular_data
                    if resembles_table(sentence):
                        tabular_data.append(sentence)
                else:
                    # Check if any of the keywords are present in the sentence
                    if any(keyword.lower() in sentence.lower() for keyword in keywords):
                        # Add the sentence to important_sentences
                        important_sentences.append(sentence)
        
        # Join the important sentences and tabular data together
        important_sentences_text = '\n'.join(important_sentences)
        tabular_data_text = '\n'.join(tabular_data)
        
        # Return both the important sentences and tabular data
        return important_sentences_text, tabular_data_text

# Sample PDF file path
pdf_path = 'trail2.pdf'

# Keywords to search for in the PDF
keywords = ['coverage', 'benefit', 'ambulance', 'hospitalization']

# Extracting important sentences and tabular data from the PDF based on keywords
important_sentences, tabular_data = extract_important_data_from_pdf(pdf_path, keywords)

# Printing the important sentences and tabular data
print("Important Sentences:")
print(important_sentences)

print("\nTabular Data:")
print(tabular_data)
