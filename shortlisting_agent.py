class ShortlistingAgent:
    def __init__(self, threshold):
        """
        Initializes the ShortlistingAgent with a given threshold.
        """
        self.threshold = threshold

    def calculate_match_score(self, job_description_data, cv_data):
        """
        Calculates a match score between JD and CV. (Same function as before)
        """
        jd_required_skills_str = job_description_data.get("required_skills", "").lower()
        cv_skills_value = cv_data.get("skills", "")

        if isinstance(cv_skills_value, list):
            cv_skills_str = ", ".join(cv_skills_value).lower()
        else:
            cv_skills_str = str(cv_skills_value).lower()

        if not jd_required_skills_str or not cv_skills_str:
            return 0.0

        jd_required_skills_candidates = [skill.strip() for skill in jd_required_skills_str.replace(';', ',').replace('\n', ',').split(',')]
        cv_skills_candidates = [skill.strip() for skill in cv_skills_str.replace(';', ',').replace('\n', ',').split(',')]

        jd_required_skills = [skill for skill in jd_required_skills_candidates if skill]
        cv_skills = [skill for skill in cv_skills_candidates if skill]

        matched_skills_count = 0
        for required_skill in jd_required_skills:
            if required_skill in cv_skills:
                matched_skills_count += 1

        if not jd_required_skills:
            return 0.0

        match_score = (matched_skills_count / len(jd_required_skills)) * 100.0
        return round(match_score, 2)


    def shortlist_candidates(self, cv_results):
        """
        Shortlists candidates based on match scores and the agent's threshold.

        Args:
            cv_results (list): A list of dictionaries, where each dictionary contains
                                   'cv_filename', 'candidate_name', and 'match_score'.

        Returns:
            list: A list of dictionaries representing shortlisted candidates.
        """
        shortlisted_candidates = []
        for result in cv_results:
            if result['match_score'] >= self.threshold:
                shortlisted_candidates.append(result)
        return shortlisted_candidates

    def display_shortlist_results(self, shortlisted_candidates):
        """
        Prints the results of the shortlisting process.
        """
        if shortlisted_candidates:
            print(f"\n--- Shortlisted Candidates (Match Score >= {self.threshold}%) ---")
            for candidate in shortlisted_candidates:
                print(f"  - CV File: {candidate['cv_filename']}, Candidate: {candidate['candidate_name']}, Match Score: {candidate['match_score']}%")
        else:
            print("\n--- No Candidates Shortlisted based on Threshold ---")


if __name__ == "__main__":
    # --- Sample JD and CV Data (same as before for testing) ---
    sample_jd_data = {
        "job_title": "Software Engineer",
        "required_skills": "python, java, web development, databases, problem-solving"
    }

    sample_cv_data = {
        "name": "Sample Candidate",
        "skills": ["Python", "JavaScript", "Web Development", "SQL", "Communication Skills"]
    }

    # --- Test calculate_match_score ---
    match_score = ShortlistingAgent(threshold=70).calculate_match_score(sample_jd_data, sample_cv_data) # Use the class now
    print("\n--- Match Score ---")
    print(f"Job Title: {sample_jd_data['job_title']}")
    print(f"Candidate Name: {sample_cv_data['name']}")
    print(f"Match Score: {match_score}%")

    # --- Example of using shortlist_candidates and display_shortlist_results ---
    sample_cv_results = [
        {"cv_filename": "cv1.pdf", "candidate_name": "Candidate A", "match_score": 85.0},
        {"cv_filename": "cv2.pdf", "candidate_name": "Candidate B", "match_score": 60.0},
        {"cv_filename": "cv3.pdf", "candidate_name": "Candidate C", "match_score": 92.0}
    ]
    shortlisting_agent = ShortlistingAgent(threshold=75) # Create an instance of ShortlistingAgent
    shortlisted = shortlisting_agent.shortlist_candidates(sample_cv_results) # Use the instance to call methods
    shortlisting_agent.display_shortlist_results(shortlisted) # Use the instance to call methods