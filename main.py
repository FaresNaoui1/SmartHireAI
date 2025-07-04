import email_managment
import os
from dotenv import load_dotenv
import LLM


from fastapi import FastAPI
load_dotenv()  # Load .env file

# Sample CVs as strings for testing
cvs = [
    """
    Name: Sarah Tarek
    Email: sarah.tarek@example.com
    Phone: +213 555 123 456

    Summary:
    Motivated Python Backend Developer with 3 years of experience building scalable APIs and microservices.
    Strong background in FastAPI, Docker, and PostgreSQL.

    Skills:
    - Python, FastAPI, Flask
    - PostgreSQL, Redis
    - Docker, AWS Lambda
    - Git, CI/CD

    Experience:
    - Backend Developer at AlgérieTech (2022–Present)
    - Junior Developer at StartupDev DZ (2020–2021)
    """,

    """
    Name: Rachid Belaid
    Email: rachid.belaid@example.com
    Phone: +213 777 000 111

    Summary:
    Full-stack engineer with focus on Spring Boot and Angular. Interested in cloud infrastructure and DevOps.

    Skills:
    - Java, Spring Boot, Angular
    - MySQL, MongoDB
    - Jenkins, Docker

    Experience:
    - Full Stack Developer at NumidiaSoft (2021–Present)
    - DevOps Intern at CloudZone DZ (2020)
    """,

    """
    Name: Amina Dali
    Email: amina.dali@example.com

    Summary:
    Junior Python Developer skilled in automation and REST API development.

    Skills:
    - Python, Flask, FastAPI
    - SQLite, MySQL
    - HTML/CSS

    Experience:
    - Freelance projects (2022–2023)
    - Python intern at TechUp (2021)
    """,

    """
    Name: Nassim Bouras
    Email: nassim.b@example.com

    Summary:
    Backend specialist with 5+ years in Spring Boot and enterprise systems.

    Skills:
    - Java, Spring Boot
    - Oracle DB, MySQL
    - Kafka, RabbitMQ

    Experience:
    - Backend Lead at ElMouradiaTech (2019–Now)
    - Software Engineer at BouiraTech (2016–2019)
    """,

    """
    Name: Leila Haddad
    Email: leila.h@example.com

    Summary:
    Fresh graduate with strong academic background in Computer Science and passion for backend systems.

    Skills:
    - Java, Python
    - FastAPI (self-taught)
    - GitHub, Firebase

    Education:
    - Bachelor in CS, Univ. of Blida (2021)
    """
]

top_n = 5

# Get credentials
sender_email = os.getenv("HR_EMAIL")
sender_password = os.getenv("HR_PASS")
manager_email = os.getenv("MANAGER_EMAIL")

# Job requirements
jobreq = """
We are looking for a **Python Backend Developer** to join our growing engineering team.

**Key Requirements:**
- Strong experience with **FastAPI** or **Flask**
- Solid knowledge of **SQL databases** such as **MySQL** or **PostgreSQL**
- Familiarity with **Spring Boot** is a strong plus
- Experience in building **RESTful APIs**
- Ability to write clean, maintainable, and efficient code
- Comfortable with **Docker** and basic DevOps (CI/CD)
- Good communication skills and ability to work in a team
- Bonus: Experience with **AWS** or **Google Cloud**

**Preferred Qualifications:**
- Bachelor's degree in Computer Science or related field
- At least 2 years of backend development experience

**Responsibilities:**
- Design and implement backend systems and APIs
- Work closely with frontend developers and product teams
- Maintain and scale existing services
- Write unit and integration tests

We value problem-solvers who are passionate about clean architecture and efficient backend services.
"""
jobreq=LLM.small_model(jobreq)
print("Job Requirements:", jobreq)
response = LLM.large_model(jobreq, cvs, top_n)
print("Response from LLM:", response)

email_managment.send_summary_email(response, jobreq, cvs, top_n, sender_email, sender_password, manager_email)
emails=LLM.read_emails(sender_email, sender_password, sender_filter=manager_email, subject_filter="AI Candidate Evaluation - Top")
names= LLM.extract_names_from_emails(emails)
scarping= LLM.scrape_social_media(names,cvs)
# Example of creating a Google Meet event   

app= FastAPI()
@app.get("/")
def root():
    print("Welcome to the HR AI Agent API!")