# ai_tools.py
import os
import google.generativeai as genai

# Configure the Gemini API key
API_KEY = "AIzaSyAZWY1WQLlud8xq0HElWDu04AqW3oUwilc"  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# AI Tool: Document Summarizer
def summarize_document(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize this document: {text}")
    return response.text

# AI Tool: Text-to-Query Generator
def generate_query(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Generate a query based on: {text}")
    return response.text

# AI Tool: Image-to-Text Conversion (Placeholder for demonstration)
def image_to_text(image_path):
    from PIL import Image
    image = Image.open(image_path)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(["Describe this image", image])
    return response.text

# AI Tool: Text Translator
def translate_text(text, target_language="French"):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Translate '{text}' to {target_language}.")
    return response.text
