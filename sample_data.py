"""
Sample candidate profiles and realistic job descriptions for ATS Resumer.
Provides pre-loaded demonstration data matching the system workflow diagrams.
"""

DEFAULT_RESUME = {
    "personal": {
        "full_name": "M. Katamaiah",
        "target_role": "Python Developer",
        "email": "katamaiah@example.com",
        "phone": "+91 9876543210",
        "location": "Hyderabad, India",
        "linkedin": "linkedin.com/in/mkatamaiah",
        "github": "github.com/mkatamaiah"
    },
    "summary": "Motivated Python Developer with experience in web development, data analysis and problem solving. Skilled in Django, Flask, SQL, and modern web technologies with a strong track record of engineering reliable, high-performance software applications.",
    "education": [
        {
            "degree": "B.Tech",
            "field": "Computer Science and Engineering",
            "university": "JNTU Hyderabad",
            "passing_year": "2020",
            "grade": "8.4 CGPA"
        }
    ],
    "technical_skills": [
        "Python", "Django", "SQL", "JavaScript", "MySQL", 
        "HTML", "CSS", "Problem Solving", "Communication", "Data Analysis"
    ],
    "soft_skills": [
        "Problem Solving", "Communication", "Team Collaboration", "Time Management", "Critical Thinking"
    ],
    "experience": [
        {
            "company": "ABC Technologies",
            "designation": "Software Developer",
            "duration": "2021 - 2023",
            "location": "Hyderabad, India",
            "responsibilities": (
                "Developed scalable backend web applications and RESTful APIs using Python and Django.\n"
                "Designed and optimized SQL database schemas, reducing query response times by 30%.\n"
                "Collaborated with agile engineering teams to deploy microservices and implement automated testing.\n"
                "Integrated third-party APIs and built responsive client-facing interfaces."
            )
        }
    ],
    "projects": [
        {
            "title": "ATS Resumer – Resume Builder and Optimizer",
            "technologies": "Python, Streamlit, Pandas, ReportLab",
            "description": (
                "Engineered an automated ATS resume optimizer that analyzes job descriptions, "
                "calculates keyword match scores, and compiles clean, single-column ATS-friendly PDFs."
            )
        },
        {
            "title": "Inventory Management & Analytics Portal",
            "technologies": "Python, Django, PostgreSQL, HTML/CSS",
            "description": (
                "Created a web-based inventory management dashboard with automated stock level alerts, "
                "sales reporting, and secure role-based access control."
            )
        }
    ],
    "certifications": [
        "Python Certified Associate Programmer (PCAP)",
        "Database Design & SQL Specialist Certificate"
    ]
}

SAMPLE_JOB_DESCRIPTIONS = {
    "Python Developer": (
        "We are looking for a Python Developer with experience in web development, data analysis and problem solving skills. "
        "The candidate should have knowledge of Django, Flask, SQL and good communication skills. "
        "Experience with REST APIs, Git version control, MySQL, and cloud deployments is a strong plus. "
        "You will design scalable backend services, optimize database queries, and collaborate in an Agile software team."
    ),
    "Java Developer": (
        "Seeking an experienced Java Developer proficient in Core Java, Spring Boot, Microservices, and RESTful APIs. "
        "Candidates must have hands-on experience with Hibernate, SQL databases (MySQL/PostgreSQL), Git, and CI/CD tools like Jenkins. "
        "Knowledge of Docker, Kubernetes, AWS cloud, and strong Object-Oriented Design (OOD) principles is required. "
        "Excellent analytical thinking and unit testing skills with JUnit are essential."
    ),
    "Web Developer": (
        "Looking for a skilled Web Developer to create dynamic, modern user interfaces. "
        "Must be proficient in HTML5, CSS3, JavaScript (ES6+), React.js, and responsive web design. "
        "Experience integrating REST APIs, Node.js, Git version control, and frontend testing is preferred. "
        "The role requires good attention to UI/UX detail, cross-browser compatibility, and strong teamwork capabilities."
    ),
    "Data Analyst": (
        "We are hiring a Data Analyst to extract business insights from complex datasets. "
        "Required skills include Python, SQL, Pandas, NumPy, Data Analysis, and Data Visualization tools (PowerBI or Tableau). "
        "The ideal candidate possesses strong statistical foundations, Excel expertise, problem-solving skills, and clear reporting ability. "
        "Familiarity with ETL pipelines, machine learning basics, and data cleaning techniques is preferred."
    ),
    "Software Engineer": (
        "We are seeking a versatile Software Engineer to design, build, and maintain mission-critical software solutions. "
        "Core competencies include Data Structures and Algorithms, Python or Java, Object-Oriented Programming, and SQL. "
        "Must have experience with Git, unit testing, software architecture, and problem solving. "
        "Ability to work in cross-functional Agile teams with strong written and verbal communication is required."
    )
}
