import ollama
import pandas as pd

class JDSummarizerAgent:
    def __init__(self, model_name='mistral'):
        """
        Initializes the JDSummarizerAgent with a specified Ollama model.
        """
        self.model_name = model_name

    def summarize_jd(self, jd_text):
        """
        Summarizes a job description using Ollama and extracts key elements.

        Args:
            jd_text (str): The job description text.

        Returns:
            dict: A dictionary containing extracted JD elements (job_title, responsibilities, ...).
        """
        prompt = f"""
             Please analyze the following job description and extract the following key elements.
            Format your response as a **valid JSON object**. Ensure that **all keys and string values in the JSON are enclosed in DOUBLE QUOTES** (").
            Use the following JSON keys: "job_title", "responsibilities", "required_skills", "required_experience", "educational_qualifications".

            For "responsibilities" and "educational_qualifications", if there are multiple items, please provide them as a JSON array (list). For "required_skills" and "required_experience", provide them as strings.

            If any section is not found in the job description, the corresponding JSON key should still be present, but the value should be an empty string (for string values) or an empty JSON array (for "responsibilities" and "educational_qualifications").

            Job Description:
            {jd_text}
        """

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        extracted_data_text = response['message']['content']

        print("\n--- Raw LLM Response (JD Summarizer) ---")
        print(extracted_data_text)

        extracted_jd_data = {
            "job_title": "",
            "responsibilities": [],
            "required_skills": "",
            "required_experience": "",
            "educational_qualifications": ""
        }

        try:
            import json
            llm_response_json = json.loads(extracted_data_text)

            extracted_jd_data["job_title"] = llm_response_json.get("job_title", "")
            extracted_jd_data["responsibilities"] = llm_response_json.get("responsibilities", [])
            extracted_jd_data["required_skills"] = llm_response_json.get("required_skills", "")
            extracted_jd_data["required_experience"] = llm_response_json.get("required_experience", "")
            extracted_jd_data["educational_qualifications"] = llm_response_json.get("educational_qualifications", "")

        except json.JSONDecodeError as json_error:
            print(f"Warning (JD Summarizer): JSON Parse Error: {json_error}")
            print(f"Raw LLM Output (JD Summarizer):\n{extracted_data_text}")
        except Exception as parse_error:
            print(f"Warning (JD Summarizer): General Parse Error: {parse_error}")
            print(f"Raw LLM Output (JD Summarizer):\n{extracted_data_text}")

        return extracted_jd_data

    def load_job_descriptions_from_csv(self, csv_file_path):
        """
        Loads job descriptions from a CSV file into a pandas DataFrame.

        Args:
            csv_file_path (str): Path to the CSV file.

        Returns:
            pandas.DataFrame: DataFrame containing job descriptions, or None if error.
        """
        try:
            # Try reading with 'latin-1' encoding first
            df = pd.read_csv(csv_file_path, encoding='latin-1')
            return df

        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_file_path}")
            return None
        except UnicodeDecodeError:
            print(f"Error: Could not decode CSV with 'latin-1' encoding. Trying 'cp1252'...")
            try:
                df = pd.read_csv(csv_file_path, encoding='cp1252')
                return df
            except Exception as e2:
                print(f"Error reading CSV with 'cp1252' encoding: {e2}")
                return None
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return None


if __name__ == "__main__":
    CSV_JD_FILE_PATH_DEMO = "data/job_description.csv"
    csv_jd_file_path = CSV_JD_FILE_PATH_DEMO

    jd_agent = JDSummarizerAgent() # Create instance of JDSummarizerAgent
    job_data_frame = jd_agent.load_job_descriptions_from_csv(csv_jd_file_path) # Call method on instance

    if job_data_frame is not None:
        print("\n--- Processing Job Descriptions from CSV ---")
        for index, row in job_data_frame.iterrows():
            job_title = row['Job Title']
            job_description_text = row['Job Description']

            print(f"\n--- Processing Job Title: {job_title} ---")
            print("\n--- Original Job Description ---")
            print(job_description_text)

            print("\n--- Summarized Job Description (Ollama's Response) ---")
            summary = jd_agent.summarize_jd(job_description_text) # Call method on instance
            print(summary)
    else:
        print("Could not load job descriptions from CSV. Exiting.")