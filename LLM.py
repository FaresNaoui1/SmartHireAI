import os
import google.generativeai as genai
import read_pdf
from intervue import create_google_meet_event
import datetime
from email_utils import read_emails


genai.configure(api_key=(os.getenv("GOOGLE_API_KEY") or "YOUR_API_KEY_HERE"))
job = "Looking for a Python backend developer with experience in FastAPI, SpringBoot, and MySQL."
def small_model(jobreq):
    model = genai.GenerativeModel('gemini-2.0-flash')
    chat = model.start_chat()

    prompt = f"""
Here's a job description:
{jobreq}
Given the following job requirements, 
rank them from most important to least important based on relevance and impact on job performance. 
Assign a probability (between 0 and 1) to each requirement representing its importance,
such that the probabilities sum up to 1. 
Format your answer as a JSON object with the requirement as the key and the probability as the value. 
These probabilities will later be used to score and rank candidates' CVs.
"""

    response = chat.send_message(prompt)
    return response.text 



def large_model(jobreq, cvs, top_n=10):



    emails = []
    
    model = genai.GenerativeModel('gemini-2.0-flash') 
    chat = model.start_chat()
    
    
    ranking_prompt = f"""
Here's a job description:
{jobreq}

Given the following job requirements, assign a probability (between 0 and 1) to each CV based on relevance and impact on job performance.

Format the output as a JSON object with the CV (or a name if present) as the key and the probability as the value.

Here are the CVs:
{cvs}
"""
    response = chat.send_message(ranking_prompt)
    ranked_json = response.text  

    summary_prompt = f"""
Here are the top {top_n} ranked CVs with their probabilities:
{ranked_json}

Generate a summary email for each candidate,with its email, highlighting their strengths, weaknesses, name, skills, and a short qualification summary.
Include the CV rank in the email.
Format each email clearly with line breaks.
"""
    summary_response = chat.send_message(summary_prompt)

    emails.append(summary_response.text)
    return emails 



def extract_names_from_emails(emails):
       model = genai.GenerativeModel('gemini-1.0-flash', max_output_tokens=1000, temperature=0.2) 

       chat = model.start_chat()
   
       message=chat.send_message(f"""
Here's a email response from the manager about the top selected condidates:
{emails}
Read this emails and extract the name, each candidat.
""")
       response = chat.send_message(message)
       return(response.text)



def scraping_model(selected, cvs):
     
    model = genai.GenerativeModel('gemini-2.0') 
    chat = model.start_chat()

    # Step 1: Extract social media profiles
    extraction_prompt = f"""
Here are the selected candidates:
{selected}

And here are their CVs:
{cvs}

From each CV, extract social media profiles such as LinkedIn, GitHub, Twitter, or any other platform.
Format the output as a JSON object like this:
{{ "Candidate Name": {{ "LinkedIn": "...", "GitHub": "...", "Twitter": "..." }} }}
Only include available links.
"""
    social = chat.send_message(extraction_prompt)
    social_json = social.text

    # Step 2: Simulate scraping those profiles
    scraping_prompt = f"""
Based on the following extracted social media links:
{social_json}

Simulate scraping the necessary information from each profile (e.g., top skills from GitHub, job experience from LinkedIn, etc.).
Then generate a short summary email for each candidate, highlighting:
- Name
- Strengths
- Weaknesses
- Notable skills
- Summary of qualifications

Format clearly with line breaks between each email.
"""
    summary_response = chat.send_message(scraping_prompt)

    return summary_response.text


def booking_interview(interviewer_email, emails):
    model = genai.GenerativeModel('gemini-2.0') 
    chat = model.start_chat()

    scheduled_interviews = []

    for candidate_email in emails:
        candidate_info = emails[candidate_email]

        # Step 1: Generate Interview Questions
        questions_prompt = f"""
You are an HR assistant preparing for an interview.

Here is the candidate's background and profile:
{candidate_info}

Generate 5 interview questions based on their experience, strengths, and weaknesses.
Keep it professional and tailored to the candidate.
"""
        questions = chat.send_message(questions_prompt).text

        # Step 2: Create Real Google Meet Link
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        date_time_str = date.replace(hour=15, minute=0).strftime('%Y-%m-%d %H:%M')

        meet_link = create_google_meet_event(
            candidate_email=candidate_email,
            interviewer_email=interviewer_email,
            summary="Interview with candidate",
            date_time_str=date_time_str
        )

        # Step 3: Generate Email
        email_prompt = f"""
Write a professional interview invitation email to {candidate_email}, including:
- Interviewer's email: {interviewer_email}
- Google Meet link: {meet_link}
- List of personalized interview questions:
{questions}
- Scheduled time: {date_time_str}
Make it formal and friendly.
"""
        final_email = chat.send_message(email_prompt).text

        scheduled_interviews.append({
            "to": candidate_email,
            "meet_link": meet_link,
            "questions": questions,
            "email_body": final_email
        })

    return scheduled_interviews