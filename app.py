import streamlit as st
from functions import save_uploaded_file, extract_text_from_pdf, extract_text_from_image, extract_text_from_txt, get_assistant_response

def main():
    st.title("AI Chatbot for Document Analysis")

    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
    query = st.text_input("Enter your query")

    if st.button("Submit"):
        if uploaded_files and query:
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    file_paths.append(file_path)

            # Extract text from each file
            text_content = ""
            for file_path in file_paths:
                if file_path.lower().endswith(".pdf"):
                    text_content += extract_text_from_pdf(file_path)
                elif file_path.lower().endswith(".jpg") or file_path.lower().endswith(".png"):
                    text_content += extract_text_from_image(file_path)
                elif file_path.lower().endswith(".txt"):
                    text_content += extract_text_from_txt(file_path)

            # Get response from AI
            if text_content:
                response = get_assistant_response(text_content, query)
                st.write("AI Response:", response)
            else:
                st.write("No text content extracted from files.")

if __name__ == "__main__":
    main()
