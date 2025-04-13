import jd_summarizer_agent
import cv_agent
import shortlisting_agent
import scheduler_agent
import os
import tkinter as tk
from tkinter import filedialog, Spinbox, Scrollbar, Text, YView, Checkbutton, IntVar, Label, Entry, Button, END
import csv  # Import csv module for CSV export

class JobScreeningApp:
    def __init__(self, master):
        self.master = master
        master.title("AI Job Screening System")

        # --- Configuration Variables ---
        self.excel_jd_file_path = tk.StringVar(master, value="D:/project/Accenture/job_screening_ai/data/job_description.csv")  # Default path
        self.cv_folder_path = tk.StringVar(master, value="D:/project/Accenture/job_screening_ai/data/CVs1")  # Default path
        self.shortlisting_threshold = tk.IntVar(master, value=70)
        self.interview_format = "Online Video Call"  # Fixed for now
        self.selected_job_titles = []
        self.job_title_vars = {}
        self.csv_report_data = [] # Initialize csv_report_data

        # --- UI Elements ---
        row = 0
        Label(master, text="Job Description CSV File:").grid(row=row, column=0, sticky="w")
        Entry(master, textvariable=self.excel_jd_file_path, width=50).grid(row=row, column=1, padx=5, pady=5)
        Button(master, text="Select CSV File", command=self.select_jd_csv_file).grid(row=row, column=2, padx=5, pady=5)
        row += 1

        Label(master, text="CV Folder:").grid(row=row, column=0, sticky="w")
        Entry(master, textvariable=self.cv_folder_path, width=50).grid(row=row, column=1, padx=5, pady=5)
        Button(master, text="Select CV Folder", command=self.select_cv_folder).grid(row=row, column=2, padx=5, pady=5)
        row += 1

        Label(master, text="Shortlisting Threshold (%):").grid(row=row, column=0, sticky="w")
        Spinbox(master, from_=0, to=100, textvariable=self.shortlisting_threshold, width=5).grid(row=row, column=1, padx=5, pady=5, sticky="w")
        row += 1

        Label(master, text="Select Job Titles to Process:").grid(row=row, column=0, sticky="nw")
        self.job_title_canvas = tk.Canvas(master, borderwidth=2, relief="groove")  # Canvas for scrollable job titles
        self.job_title_frame = tk.Frame(self.job_title_canvas)  # Frame inside Canvas for checkboxes
        self.vsb_job_titles = tk.Scrollbar(master, orient="vertical", command=self.job_title_canvas.yview)
        self.job_title_canvas.configure(yscrollcommand=self.vsb_job_titles.set)
        self.vsb_job_titles.grid(row=row, column=3, sticky='ns')
        self.job_title_canvas.grid(row=row, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.job_title_canvas_frame = self.job_title_canvas.create_window((0, 0), window=self.job_title_frame, anchor="nw", tags="job_title_frame_tag")
        self.job_title_frame.bind("<Configure>", self.on_frame_configure)
        row += 1

        Button(master, text="Start Job Screening", command=self.start_processing).grid(row=row, column=1, columnspan=2, pady=20)
        row += 1

        # CSV Export Button (initially disabled)
        Button(master, text="Generate CSV Report", command=self.generate_csv_report, state=tk.DISABLED, width=20).grid(row=row, column=1, columnspan=2, pady=10)
        self.csv_button = master.children['!button4']  # Access the button to control state
        row += 1

        # Results Display Area
        Label(master, text="Results:").grid(row=row, column=0, sticky="nw")
        self.results_text = Text(master, height=20, width=80, wrap=tk.WORD)
        self.results_text.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        scrollbar = Scrollbar(master, command=self.results_text.yview)
        scrollbar.grid(row=row, column=3, sticky='nsw')
        self.results_text.config(yscrollcommand=scrollbar.set)
        row += 1
        master.grid_columnconfigure(1, weight=1)

    def on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.job_title_canvas.configure(scrollregion=self.job_title_canvas.bbox("all"))

    def select_jd_csv_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.excel_jd_file_path.set(file_path)
            self.populate_job_titles()

    def select_cv_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.cv_folder_path.set(folder_path)

    def populate_job_titles(self):
        # Clear existing checkboxes
        for widget in self.job_title_frame.winfo_children():
            widget.destroy()
        self.job_title_vars = {}

        csv_file_path = self.excel_jd_file_path.get()
        if not csv_file_path or not os.path.exists(csv_file_path):
            self.results_text.insert(END, "Error: Please select a valid Job Description CSV file first.\n")
            return

        jd_agent = jd_summarizer_agent.JDSummarizerAgent()
        job_data_frame = jd_agent.load_job_descriptions_from_csv(csv_file_path)
        if job_data_frame is not None:
            job_titles = job_data_frame['Job Title'].unique()
            for i, job_title in enumerate(job_titles):
                var = IntVar(value=1)
                Checkbutton(self.job_title_frame, text=job_title, variable=var).grid(row=i, column=0, sticky="w")
                self.job_title_vars[job_title] = var
            self.selected_job_titles = job_titles.tolist()

    def start_processing(self):
        self.results_text.delete("1.0", END)
        jd_csv_file = self.excel_jd_file_path.get()
        cv_folder = self.cv_folder_path.get()
        threshold = self.shortlisting_threshold.get()

        if not jd_csv_file or not os.path.exists(jd_csv_file):
            self.results_text.insert(END, "Error: Invalid Job Description CSV file path.\n")
            return
        if not cv_folder or not os.path.exists(cv_folder):
            self.results_text.insert(END, "Error: Invalid CV folder path.\n")
            return

        selected_job_titles = [title for title, var in self.job_title_vars.items() if var.get() == 1]
        if not selected_job_titles:
            self.results_text.insert(END, "Error: No Job Titles selected for processing.\n")
            return

        self.results_text.insert(END, "--- Starting Job Screening Process ---\n")
        self.results_text.insert(END, f"Job Description CSV: {jd_csv_file}\n")
        self.results_text.insert(END, f"CV Folder: {cv_folder}\n")
        self.results_text.insert(END, f"Shortlisting Threshold: {threshold}%\n")
        self.results_text.insert(END, f"Selected Job Titles: {selected_job_titles}\n")
        self.results_text.see(END)

        jd_agent = jd_summarizer_agent.JDSummarizerAgent()
        cv_agent_instance = cv_agent.CVAgent()
        shortlisting_agent_instance = shortlisting_agent.ShortlistingAgent(threshold=threshold)
        scheduler = scheduler_agent.SchedulerAgent(interview_format=self.interview_format)

        job_data_frame = jd_agent.load_job_descriptions_from_csv(jd_csv_file)
        job_titles_to_process = selected_job_titles

        all_cv_data = self.preprocess_cvs(cv_folder, cv_agent_instance)

        final_results_for_csv = []  # List to collect results for CSV export

        for job_title_to_process in job_titles_to_process:
            job_row = job_data_frame[job_data_frame['Job Title'] == job_title_to_process]
            job_description_text = job_row['Job Description'].iloc[0]
            jd_data = jd_agent.summarize_jd(job_description_text)

            self.results_text.insert(END, f"\n--- Summarized Job Description Data (for: {job_title_to_process}) ---\n")
            self.results_text.insert(END, str(jd_data) + "\n")
            self.results_text.see(END)

            cv_results = self.match_cvs_to_jd(all_cv_data, jd_data, shortlisting_agent_instance, job_title_to_process)

            final_results_for_csv.extend(cv_results)  # Collect results for CSV export
            self.shortlist_and_schedule(cv_results, job_title_to_process, shortlisting_agent_instance, scheduler)


        self.results_text.insert(END, "\n--- Finished Processing ALL Selected Job Titles ---\n")
        self.results_text.see(END)

        self.csv_report_data = final_results_for_csv # Store results for CSV export
        self.csv_button.config(state=tk.NORMAL)  # Enable CSV export button AFTER processing


    def generate_csv_report(self):
        if not self.csv_report_data:
            self.results_text.insert(END, "Warning: No data available to export to CSV.\nRun Job Screening first.\n")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV file", "*.csv"), ("All files", "*.*")],
                                                    initialfile="job_screening_report.csv")

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['CV Filename', 'Candidate Name', 'Match Score (%)', 'Email', 'Phone Number'])  # Header row
                    for row_data in self.csv_report_data:
                        csv_writer.writerow([row_data['cv_filename'], row_data['candidate_name'], row_data['match_score'],
                                             row_data['email'], row_data['phone_number']])  # Write data rows
                self.results_text.insert(END, f"\nCSV report generated successfully and saved to: {file_path}\n")
                self.results_text.see(END)
            except Exception as e:
                self.results_text.insert(END, f"Error generating CSV report: {e}\n")
                self.results_text.see(END)


    def preprocess_cvs(self, cv_folder, cv_agent_instance):
        all_cv_data = {}
        cv_file_names = [filename for filename in os.listdir(cv_folder) if filename.lower().endswith(".pdf")]

        if not cv_file_names:
            self.results_text.insert(END, f"Warning: No PDF CV files found in folder: {cv_folder}\n")
        else:
            self.results_text.insert(END, f"\n--- Pre-processing CVs from folder: {cv_folder} (once) ---\n")
            for cv_filename in cv_file_names:
                cv_file_path = os.path.join(cv_folder, cv_filename)
                self.results_text.insert(END, f"  - Pre-processing CV: {cv_filename}\n")
                self.results_text.see(END)

                cv_text = cv_agent_instance.read_cv_from_file(cv_file_path)
                if not cv_text:
                    self.results_text.insert(END, f"    Error: Could not read CV file: {cv_filename}. Skipping pre-processing for this CV.\n")
                    continue

                cv_data = cv_agent_instance.extract_cv_data(cv_text)
                all_cv_data[cv_filename] = cv_data
        return all_cv_data

    def match_cvs_to_jd(self, all_cv_data, jd_data, shortlisting_agent_instance, job_title_to_process):
        cv_results = []
        self.results_text.insert(END, f"\n--- Matching Pre-processed CVs for Job Title: {job_title_to_process} ---\n")
        for cv_filename, cv_data in all_cv_data.items():
            self.results_text.insert(END, f"  - Matching CV: {cv_filename}\n")
            self.results_text.see(END)

            # Include email and phone_number in the cv_results
            cv_results.append({
                "cv_filename": cv_filename,
                "candidate_name": cv_data.get('name', 'N/A'),
                "match_score": shortlisting_agent_instance.calculate_match_score(jd_data, cv_data),
                "email": cv_data.get('email', 'N/A'),  # Get email from cv_data
                "phone_number": cv_data.get('phone_number', 'N/A')  # Get phone_number from cv_data
                , "job_title": job_title_to_process # Keep job_title in cv_results
            })
        return cv_results


    def shortlist_and_schedule(self, cv_results, job_title_to_process, shortlisting_agent_instance, scheduler):
        self.results_text.insert(END, f"\n--- Job Screening Results for Job Title: {job_title_to_process} ---\n")
        shortlisted_candidates = shortlisting_agent_instance.shortlist_candidates(cv_results)

        shortlist_output = ""
        if shortlisted_candidates:
            shortlist_output += f"\n--- Shortlisted Candidates (Match Score >= {shortlisting_agent_instance.threshold}%) ---\n"
            for candidate in shortlisted_candidates:
                shortlist_output += f"  - CV File: {candidate['cv_filename']}, Candidate: {candidate['candidate_name']}, Match Score: {candidate['match_score']}%\n"
        else:
            shortlist_output += "\n--- No Candidates Shortlisted based on Threshold ---\n"
        self.results_text.insert(END, shortlist_output)
        self.results_text.see(END)

        if shortlisted_candidates:
            self.results_text.insert(END, f"\n--- Scheduling Interviews for Shortlisted Candidates for Job Title: {job_title_to_process} ---\n")
            potential_interview_dates = ["November 5th, 2023", "November 6th, 2023"]
            potential_interview_times = ["10:00 AM - 12:00 PM", "2:00 PM - 4:00 PM"]

            for candidate in shortlisted_candidates:
                interview_request_message = scheduler.generate_interview_request(
                    candidate_name=candidate['candidate_name'],
                    job_title=job_title_to_process,
                    potential_dates=potential_interview_dates,
                    potential_times=potential_interview_times
                )
                scheduler.send_interview_request(
                    candidate_name=candidate['candidate_name'],
                    interview_request_message=interview_request_message
                )
                self.results_text.insert(END, f"\n--- Interview Request for {candidate['candidate_name']} ---\n")
                self.results_text.insert(END, interview_request_message + "\n")
                self.results_text.insert(END, f"--- End of Interview Request for {candidate['candidate_name']} ---\n")
                self.results_text.see(END)
        else:
            self.results_text.insert(END, f"\n--- No Candidates to Schedule Interviews For - Job Title: {job_title_to_process} ---\n")
            self.results_text.see(END)


if __name__ == "__main__":
    root = tk.Tk()
    app = JobScreeningApp(root)
    root.mainloop()