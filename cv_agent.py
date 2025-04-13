import ollama
import fitz  # PyMuPDF

class CVAgent:
    def __init__(self, model_name='mistral'):
        """
        Initializes the CVAgent with a specified Ollama model.
        """
        self.model_name = model_name

    def extract_cv_data(self, cv_text):
        """
        Extracts key data from a CV text using Ollama, including contact info, and structures output in JSON.
        """
        prompt = f"""
        Please analyze the following CV text and extract the following information.
        Organize the extracted information into a JSON-like format (Python dictionary) with keys:
        "name", "education", "work_experience", "skills", "email", "phone_number". <--- Added email and phone_number

        For each section, extract the relevant details as concisely as possible. If a section is not found, leave the corresponding key's value empty.

        Specifically for "email" and "phone_number", try to find the candidate's primary email address and phone number from the CV. If multiple are listed, choose the most likely personal contact information. If not found, leave them empty.

        CV Text:
        {cv_text}

        ---

        Extract the following:

        1.  Full Name of the candidate:
        2.  Education: (List degrees, institutions, years - if available. Focus on the most recent or relevant education)
        3.  Work Experience: (Summarize 2-3 most recent or most relevant work experiences, including job titles, companies, and years. Briefly mention key responsibilities for each role)
        4.  Skills: (List key technical and soft skills mentioned in the CV. Be concise, list skills as comma-separated values)
        5.  Email Address: (Primary email address for contact) <--- Added instructions for email
        6.  Phone Number: (Primary phone number for contact) <--- Added instructions for phone
        """

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        extracted_data_text = response['message']['content']

        print("\n--- Raw LLM Response (CV Agent - Contact Info) ---") # Updated print statement
        print(extracted_data_text)

        # ---  Attempt to parse LLM output as JSON ---
        extracted_data = {
            "name": "",
            "education": [],
            "work_experience": [],
            "skills": "",
            "email": "",       # Added email key
            "phone_number": ""  # Added phone_number key
        }
        try:
            import json

            llm_response_json = json.loads(extracted_data_text)

            extracted_data["name"] = llm_response_json.get("name", "")
            extracted_data["education"] = llm_response_json.get("education", [])
            extracted_data["work_experience"] = llm_response_json.get("work_experience", [])
            extracted_data["skills"] = llm_response_json.get("skills", "")
            extracted_data["email"] = llm_response_json.get("email", "")         # Parse email
            extracted_data["phone_number"] = llm_response_json.get("phone_number", "") # Parse phone_number

        except json.JSONDecodeError as json_error:
            print(f"Warning: Error parsing LLM output as JSON: {json_error}")
            print(f"Raw LLM Output:\n{extracted_data_text}")
        except Exception as parse_error:
            print(f"Warning: General error during JSON parsing: {parse_error}")
            print(f"Raw LLM Output:\n{extracted_data_text}")

        return extracted_data


    def read_cv_from_file(self, file_path):
        """
        Reads CV text from a PDF file.
        """
        try:
            text = ""
            pdf_document = fitz.open(file_path)
            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)
                text += page.get_text()
            pdf_document.close()
            return text
        except FileNotFoundError:
            print(f"Error: CV PDF file not found at {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred while reading the CV PDF: {e}")
            return None


if __name__ == "__main__":
    CV_FILE_PATH_DEMO = "data/CVs1/C1061.pdf" # Example CV with likely contact info
    cv_file_path = CV_FILE_PATH_DEMO

    cv_agent = CVAgent()
    cv_text = cv_agent.read_cv_from_file(cv_file_path)

    if cv_text:
        print("\n--- Original CV Text (Partial - First 500 chars) ---")
        print(cv_text[:500] + "..." if len(cv_text) > 500 else cv_text)

        print("\n--- Extracted CV Data (Ollama's Response) ---")
        extracted_cv_info = cv_agent.extract_cv_data(cv_text)
        print(extracted_cv_info)
    else:
        print("Could not read CV. Exiting.")