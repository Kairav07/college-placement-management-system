# PlacePro - College Placement Management System

This is the simple, reliable version of the Web Technologies PBL demo. It uses Streamlit for the interface and SQLite for the database, so MySQL and Tomcat are not required.

## Working Features

### Student

- Register and log in
- View the student dashboard
- View featured upcoming jobs before applications open
- Search available jobs
- Automatic department and CGPA eligibility checking
- Apply for eligible jobs
- Duplicate applications are prevented
- View Pending, Selected or Rejected status

### Admin

- Open a separate admin dashboard
- Add realistic placement jobs
- Schedule future opportunities using an application opening date
- View and delete jobs
- View student applications
- Filter applications by status
- Change status to Pending, Selected or Rejected
- Student dashboards show the updated result immediately

## Fastest Way to Run on Mac

1. Extract the ZIP.
2. Open the extracted folder.
3. Double-click `run-mac.command`.
4. If macOS blocks it, right-click the file, choose **Open**, and confirm once.
5. The browser opens at `http://localhost:8501`.

The first run installs Streamlit inside the project folder. Later runs are faster.

## Terminal Method

Open Terminal and enter the extracted folder. If it is in Downloads:

```bash
cd "$HOME/Downloads/CollegePlacementPortal_Streamlit"
chmod +x run-mac.command
./run-mac.command
```

## Demo Accounts

| Role | Email | Password |
|---|---|---|
| Student | kairav.gm_2029@woxsen.edu.in | Demo@123 |
| Admin | admin@woxsen.edu.in | Demo@123 |

The login page also contains **Open student demo** and **Open admin demo** buttons.

## Upcoming Jobs

An administrator can set an **Applications open from** date while creating a job. If that date is in the future, the job appears inside the student's **Upcoming opportunities** panel. It shows the company, role, package, eligibility requirements and opening date. Students cannot apply until the opening date arrives. On that date, the job automatically moves into **Browse jobs**.

## Reset the Sample Database

Stop Streamlit using `Control + C`, then run:

```bash
source .venv/bin/activate
python3 reset_demo.py
streamlit run app.py
```

This restores the original demo students, jobs and application.

## Project Files

```text
CollegePlacementPortal_Streamlit/
├── app.py                 Main Streamlit interface
├── database.py            SQLite database functions
├── placement.db           Created automatically
├── reset_demo.py          Restores sample data
├── requirements.txt       Python dependency
├── run-mac.command        One-command Mac launcher
└── .streamlit/config.toml Application theme
```

## Technologies Used

- Python
- Streamlit
- SQLite
- HTML and CSS styling inside Streamlit
- Sessions for student and admin login state

## Stop the Application

Return to Terminal and press `Control + C`.
