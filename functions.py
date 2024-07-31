import os
import requests
from PyPDF2 import PdfFileReader
from PIL import Image
import io
# AIzaSyAJQICrt6u5D48UW-a6dHFphnI5zLpVWLo

API_KEY = "AIzaSyAJQICrt6u5D48UW-a6dHFphnI5zLpVWLo"

def save_uploaded_file(uploaded_file):
    """Saves an uploaded file to the server."""
    try:
        os.makedirs("uploaded_files", exist_ok=True)
        file_path = os.path.join("uploaded_files", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        print(f"File saved successfully: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """Converts a PDF file to text."""
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PdfFileReader(f)
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error converting PDF to text: {e}")
        return ""

def extract_text_from_image(image_path):
    """Processes an image without showing it."""
    try:
        with Image.open(image_path) as img:
            # Perform any necessary image processing here
            return "Image processed."  # Replace with actual processing if needed
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Error: Unable to process image."

def extract_text_from_txt(txt_path):
    """Extracts text from a text file."""
    try:
        with open(txt_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return ""

def get_assistant_response(text_content, query):
    """Sends a query to Gemini and retrieves a response using the provided text content."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Answer the following query based on the provided text content:\n\n{query}\n\nText Content:\n{text_content}"
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        return generated_text or "Gemini couldn't generate a response for your query."
    except requests.exceptions.RequestException as e:
        print(f"Error getting response from Gemini: {e}")
        return f"Error communicating with Gemini: {e}"
