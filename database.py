import hashlib
import os
import secrets
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).with_name("placement.db")


def connection():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return f"{salt}${digest.hex()}"


def verify_password(password, stored):
    try:
        salt, expected = stored.split("$", 1)
        actual = hash_password(password, salt).split("$", 1)[1]
        return secrets.compare_digest(actual, expected)
    except (AttributeError, ValueError):
        return False


def init_db(force=False):
    if force and DB_PATH.exists():
        DB_PATH.unlink()

    with connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('student','admin')),
                department TEXT,
                cgpa REAL,
                phone TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                job_role TEXT NOT NULL,
                location TEXT NOT NULL,
                salary TEXT NOT NULL,
                required_department TEXT NOT NULL,
                minimum_cgpa REAL NOT NULL,
                open_date TEXT NOT NULL DEFAULT CURRENT_DATE,
                last_date TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open','Closed')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                application_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(status IN ('Pending','Selected','Rejected')),
                UNIQUE(student_id, job_id),
                FOREIGN KEY(student_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY(job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
            );
            """
        )

        # Safe migration for folders created before upcoming jobs were added.
        job_columns = {row[1] for row in db.execute("PRAGMA table_info(jobs)").fetchall()}
        if "open_date" not in job_columns:
            db.execute("ALTER TABLE jobs ADD COLUMN open_date TEXT")
            db.execute("UPDATE jobs SET open_date=date('now') WHERE open_date IS NULL")
            db.execute(
                """INSERT INTO jobs
                (company_name,job_role,location,salary,required_department,minimum_cgpa,
                 open_date,last_date,description,status)
                VALUES(?,?,?,?,?,?,?,?,?,'Open')""",
                (
                    "Amazon", "Software Development Engineer Intern", "Bengaluru",
                    "₹60,000/month", "CSE", 8.0,
                    (date.today() + timedelta(days=7)).isoformat(),
                    (date.today() + timedelta(days=37)).isoformat(),
                    "Work with an engineering team to build and test customer-facing software.",
                ),
            )

        db.execute("UPDATE jobs SET open_date=date('now') WHERE open_date IS NULL OR open_date='' ")

        if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            db.executemany(
                """INSERT INTO users
                (full_name,email,password_hash,role,department,cgpa,phone)
                VALUES(?,?,?,?,?,?,?)""",
                [
                    ("Placement Administrator", "admin@example.com", hash_password("Demo@123"), "admin", None, None, "9000000000"),
                    ("Kairav G M", "student@example.com", hash_password("Demo@123"), "student", "CSE", 9.27, "9000003020"),
                    ("Ananya R", "ananya@woxsen.edu.in", hash_password("Demo@123"), "student", "ECE", 8.40, "9000001111"),
                ],
            )

        if db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 0:
            today = date.today()
            jobs = [
                ("Infosys", "Systems Engineer", "Hyderabad", "₹4.5 LPA", "CSE", 7.0, today, today + timedelta(days=25), "Build and support enterprise software solutions for clients."),
                ("Deloitte", "Technology Analyst", "Bengaluru", "₹7.6 LPA", "CSE", 7.5, today, today + timedelta(days=18), "Work with technology teams on digital transformation projects."),
                ("TCS", "Graduate Engineer Trainee", "Chennai", "₹3.8 LPA", "CSE", 6.5, today, today + timedelta(days=14), "Entry-level engineering role with technical training."),
                ("Bosch", "Embedded Systems Intern", "Coimbatore", "₹35,000/month", "ECE", 8.0, today, today + timedelta(days=20), "Develop and test embedded software for connected products."),
                ("Zoho", "Software Developer", "Chennai", "₹8.0 LPA", "CSE", 8.0, today, today + timedelta(days=30), "Design, develop and test business software products."),
                ("Accenture", "Associate Software Engineer", "Pune", "₹4.6 LPA", "IT", 6.5, today, today + timedelta(days=12), "Support application development and cloud projects."),
                ("Amazon", "Software Development Engineer Intern", "Bengaluru", "₹60,000/month", "CSE", 8.0, today + timedelta(days=7), today + timedelta(days=37), "Work with an engineering team to build and test customer-facing software."),
                ("Microsoft", "Cloud Support Associate", "Hyderabad", "₹9.5 LPA", "CSE", 7.5, today + timedelta(days=12), today + timedelta(days=42), "Support cloud customers and troubleshoot modern infrastructure services."),
            ]
            db.executemany(
                """INSERT INTO jobs
                (company_name,job_role,location,salary,required_department,minimum_cgpa,open_date,last_date,description)
                VALUES(?,?,?,?,?,?,?,?,?)""",
                [(job[0], job[1], job[2], job[3], job[4], job[5], job[6].isoformat(), job[7].isoformat(), job[8])
                 for job in jobs],
            )

        if db.execute("SELECT COUNT(*) FROM applications").fetchone()[0] == 0:
            student = db.execute("SELECT user_id FROM users WHERE email=?", ("student@example.com",)).fetchone()
            job = db.execute("SELECT job_id FROM jobs WHERE company_name='Infosys'").fetchone()
            db.execute(
                "INSERT INTO applications(student_id,job_id,application_date,status) VALUES(?,?,?,?)",
                (student[0], job[0], (date.today() - timedelta(days=2)).isoformat(), "Pending"),
            )


def authenticate(email, password):
    with connection() as db:
        user = db.execute("SELECT * FROM users WHERE lower(email)=lower(?)", (email.strip(),)).fetchone()
    return dict(user) if user and verify_password(password, user["password_hash"]) else None


def register_student(full_name, email, password, department, cgpa, phone):
    try:
        with connection() as db:
            db.execute(
                """INSERT INTO users(full_name,email,password_hash,role,department,cgpa,phone)
                VALUES(?,?,?,'student',?,?,?)""",
                (full_name.strip(), email.strip().lower(), hash_password(password), department, float(cgpa), phone.strip()),
            )
        return True, "Registration successful. You can now log in."
    except sqlite3.IntegrityError:
        return False, "An account already exists with this email."


def student_profile(user_id):
    with connection() as db:
        row = db.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    return dict(row) if row else None


def student_stats(user_id):
    with connection() as db:
        return dict(db.execute(
            """SELECT
            (SELECT COUNT(*) FROM jobs WHERE status='Open' AND open_date<=date('now') AND last_date>=date('now')) open_jobs,
            COUNT(*) total_applications,
            COALESCE(SUM(status='Pending'),0) pending_count,
            COALESCE(SUM(status='Selected'),0) selected_count
            FROM applications WHERE student_id=?""",
            (user_id,),
        ).fetchone())


def jobs_for_student(user_id):
    with connection() as db:
        rows = db.execute(
            """SELECT j.*, u.department student_department, u.cgpa student_cgpa,
            CASE WHEN u.department=j.required_department AND u.cgpa>=j.minimum_cgpa THEN 1 ELSE 0 END eligible,
            CASE WHEN a.application_id IS NULL THEN 0 ELSE 1 END applied
            FROM jobs j JOIN users u ON u.user_id=?
            LEFT JOIN applications a ON a.job_id=j.job_id AND a.student_id=u.user_id
            WHERE j.status='Open' AND j.open_date<=date('now')
            AND j.last_date>=date('now') ORDER BY j.last_date""",
            (user_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def upcoming_jobs_for_student(user_id, limit=3):
    with connection() as db:
        rows = db.execute(
            """SELECT j.*, u.department student_department, u.cgpa student_cgpa,
            CASE WHEN u.department=j.required_department AND u.cgpa>=j.minimum_cgpa THEN 1 ELSE 0 END eligible,
            CAST(julianday(j.open_date)-julianday(date('now')) AS INTEGER) days_until_open
            FROM jobs j JOIN users u ON u.user_id=?
            WHERE j.status='Open' AND j.open_date>date('now')
            AND j.last_date>=j.open_date
            ORDER BY j.open_date, j.job_id LIMIT ?""",
            (user_id, int(limit)),
        ).fetchall()
    return [dict(row) for row in rows]


def apply_for_job(student_id, job_id):
    with connection() as db:
        check = db.execute(
            """SELECT 1 FROM users u JOIN jobs j ON j.job_id=?
            WHERE u.user_id=? AND u.department=j.required_department
            AND u.cgpa>=j.minimum_cgpa AND j.status='Open'
            AND j.open_date<=date('now') AND j.last_date>=date('now')""",
            (job_id, student_id),
        ).fetchone()
        if not check:
            return False, "You are not eligible for this job."
        try:
            db.execute(
                "INSERT INTO applications(student_id,job_id,application_date,status) VALUES(?,?,?,'Pending')",
                (student_id, job_id, date.today().isoformat()),
            )
            return True, "Application submitted successfully."
        except sqlite3.IntegrityError:
            return False, "You have already applied for this job."


def student_applications(user_id, limit=None):
    sql = """SELECT a.*,j.company_name,j.job_role,j.location,j.salary
             FROM applications a JOIN jobs j ON a.job_id=j.job_id
             WHERE a.student_id=? ORDER BY a.application_id DESC"""
    if limit:
        sql += " LIMIT ?"
        args = (user_id, limit)
    else:
        args = (user_id,)
    with connection() as db:
        rows = db.execute(sql, args).fetchall()
    return [dict(row) for row in rows]


def admin_stats():
    with connection() as db:
        row = db.execute(
            """SELECT
            (SELECT COUNT(*) FROM users WHERE role='student') students,
            (SELECT COUNT(*) FROM jobs WHERE status='Open' AND open_date<=date('now') AND last_date>=date('now')) open_jobs,
            (SELECT COUNT(*) FROM applications) applications,
            (SELECT COUNT(*) FROM applications WHERE status='Selected') selected_count"""
        ).fetchone()
    return dict(row)


def all_jobs():
    with connection() as db:
        rows = db.execute(
            """SELECT j.*,COUNT(a.application_id) application_count,
            CASE WHEN j.status='Closed' OR j.last_date<date('now') THEN 'Closed'
                 WHEN j.open_date>date('now') THEN 'Upcoming'
                 ELSE 'Open' END availability
            FROM jobs j
            LEFT JOIN applications a ON a.job_id=j.job_id
            GROUP BY j.job_id ORDER BY j.job_id DESC"""
        ).fetchall()
    return [dict(row) for row in rows]


def add_job(company, role, location, salary, department, minimum_cgpa, open_date, last_date, description):
    if str(last_date) < str(open_date):
        raise ValueError("The application deadline must be on or after the opening date.")
    with connection() as db:
        db.execute(
            """INSERT INTO jobs(company_name,job_role,location,salary,required_department,
            minimum_cgpa,open_date,last_date,description,status) VALUES(?,?,?,?,?,?,?,?,?,'Open')""",
            (company.strip(), role.strip(), location.strip(), salary.strip(), department,
             float(minimum_cgpa), str(open_date), str(last_date), description.strip()),
        )


def delete_job(job_id):
    with connection() as db:
        db.execute("DELETE FROM jobs WHERE job_id=?", (job_id,))


def all_applications(status="All", limit=None):
    sql = """SELECT a.*,u.full_name,u.email,u.department,u.cgpa,
             j.company_name,j.job_role FROM applications a
             JOIN users u ON a.student_id=u.user_id JOIN jobs j ON a.job_id=j.job_id"""
    args = []
    if status in {"Pending", "Selected", "Rejected"}:
        sql += " WHERE a.status=?"
        args.append(status)
    sql += " ORDER BY a.application_id DESC"
    if limit:
        sql += " LIMIT ?"
        args.append(limit)
    with connection() as db:
        rows = db.execute(sql, args).fetchall()
    return [dict(row) for row in rows]


def update_application_status(application_id, status):
    if status not in {"Pending", "Selected", "Rejected"}:
        raise ValueError("Invalid application status")
    with connection() as db:
        db.execute("UPDATE applications SET status=? WHERE application_id=?", (status, application_id))


init_db()
