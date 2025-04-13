class SchedulerAgent:
    COMPANY_NAME = "[Company Name]"  # Class attribute for company name

    def __init__(self, interview_format="Online Video Call"):
        """
        Initializes the SchedulerAgent with a default interview format.
        """
        self.interview_format = interview_format

    def generate_interview_request(self, candidate_name, job_title, potential_dates, potential_times):
        """
        Generates a personalized interview request message.

        Args:
            candidate_name (str): Name of the candidate.
            job_title (str): Title of the job they are being interviewed for.
            potential_dates (list): List of potential interview dates (strings).
            potential_times (list): List of potential interview times (strings, in a consistent time zone).

        Returns:
            str: The generated interview request message.
        """
        dates_str = ", ".join(potential_dates) if potential_dates else "To be determined"
        times_str = ", ".join(potential_times) if potential_times else "To be determined"

        message = f"""
        Subject: Interview Invitation for {job_title} at {SchedulerAgent.COMPANY_NAME}  <-- Use class attribute here

        Dear {candidate_name},

        We are pleased to invite you for an interview for the {job_title} position at {SchedulerAgent.COMPANY_NAME}.  <-- Use class attribute here
        Your application stood out, and we are excited to learn more about your qualifications.

        The interview will be conducted as an {self.interview_format}.

        Please let us know your availability from the following potential dates and times:

        Potential Dates: {dates_str}
        Potential Times (Your Time Zone): {times_str}

        Please reply to this message to confirm your preferred date and time, or to suggest alternative times if none of these work for you. We are flexible and happy to find a time that suits your schedule.

        We look forward to speaking with you!

        Sincerely,

        The {SchedulerAgent.COMPANY_NAME} Recruitment Team  <-- Use class attribute here
        """
        return message

    def send_interview_request(self, candidate_name, interview_request_message):
        """
        "Sends" the interview request (for hackathon, just prints to console).

        Args:
            candidate_name (str): Name of the candidate.
            interview_request_message (str): The generated interview request message.
        """
        print(f"\n--- Interview Request for {candidate_name} ---")
        print(interview_request_message)
        print(f"--- End of Interview Request for {candidate_name} ---\n")


if __name__ == "__main__":
    # --- Example Usage ---
    scheduler = SchedulerAgent(interview_format="Online Video Call") # Create SchedulerAgent instance

    sample_candidate = {
        "candidate_name": "Alice Smith",
        "cv_filename": "alice_cv.pdf",
        "match_score": 88.5
    }
    sample_job_title = "Software Engineer"
    potential_interview_dates = ["October 26th, 2023", "October 27th, 2023", "October 30th, 2023"]
    potential_interview_times = ["10:00 AM", "2:00 PM", "4:00 PM"]

    interview_message = scheduler.generate_interview_request(
        candidate_name=sample_candidate["candidate_name"],
        job_title=sample_job_title,
        potential_dates=potential_interview_dates,
        potential_times=potential_interview_times
    )

    scheduler.send_interview_request(
        candidate_name=sample_candidate["candidate_name"],
        interview_request_message=interview_message
    )