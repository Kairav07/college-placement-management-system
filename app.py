import html
from datetime import date, timedelta

import streamlit as st

import database as db

st.set_page_config(
    page_title="PlacePro | College Placement Portal",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
    :root { --blue:#1262df; --navy:#0b1739; --ink:#17213b; --muted:#667085; --line:#e5eaf2; --soft:#f5f7fb; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    .stApp { background:var(--soft); }
    #MainMenu, footer, header { visibility:hidden; }
    .block-container { padding-top:2rem; padding-bottom:4rem; max-width:1400px; }
    section[data-testid="stSidebar"] { background:var(--navy); border-right:0; }
    section[data-testid="stSidebar"] * { color:#dbe3f4; }
    section[data-testid="stSidebar"] .stRadio label { padding:.55rem .7rem; border-radius:9px; }
    section[data-testid="stSidebar"] .stRadio label:hover { background:#172a55; }
    section[data-testid="stSidebar"] button { border:1px solid #33415f; background:#142344; color:white; }
    .brand { display:flex; align-items:center; gap:11px; color:white; font:800 21px 'Manrope'; margin-bottom:28px; }
    .brand-mark { width:38px; height:38px; display:grid; place-items:center; border-radius:11px; background:linear-gradient(135deg,#2b7cff,#074bc3); box-shadow:0 8px 20px rgba(18,98,223,.3); }
    .side-label { color:#7d8cab!important; font-size:10px; font-weight:700; letter-spacing:.14em; margin:15px 0 6px; }
    .side-user { margin-top:25px; padding:17px 4px 4px; border-top:1px solid #2a3857; }
    .side-user strong { color:white; display:block; font-size:13px; }
    .side-user span { color:#8796b5; font-size:10px; }
    .eyebrow { color:var(--blue); font-size:10px; font-weight:800; letter-spacing:.15em; }
    .page-title { font:800 31px 'Manrope'; letter-spacing:-.035em; margin:5px 0 5px; color:#13203b; }
    .page-subtitle { color:var(--muted); font-size:14px; margin-bottom:25px; }
    .metric-card { background:white; border:1px solid var(--line); border-radius:14px; padding:19px 20px; min-height:128px; box-shadow:0 4px 14px rgba(26,42,75,.025); }
    .metric-card small { font-size:9px; color:#8b95a7; font-weight:800; letter-spacing:.09em; }
    .metric-card strong { display:block; font:800 29px 'Manrope'; color:#17213b; margin:5px 0; }
    .metric-card span { font-size:11px; color:var(--muted); }
    .panel-title { font:700 19px 'Manrope'; color:#1c2842; margin:3px 0 16px; }
    div[data-testid="stVerticalBlockBorderWrapper"] { background:white; border-color:var(--line); border-radius:14px; box-shadow:0 4px 14px rgba(26,42,75,.025); }
    .job-card { padding:3px 2px; min-height:260px; }
    .company-letter { width:46px; height:46px; border-radius:12px; background:#eaf2ff; color:var(--blue); display:grid; place-items:center; font:800 19px 'Manrope'; margin-bottom:13px; }
    .job-card h3 { font:700 18px 'Manrope'; margin:0 0 3px; color:#18233e; }
    .job-card h4 { font-size:13px; color:var(--blue); margin:0 0 12px; }
    .job-meta { color:#667085; font-size:11px; margin-bottom:12px; }
    .job-description { color:#667085; font-size:12px; line-height:1.55; min-height:40px; }
    .rule { border-top:1px solid var(--line); margin:13px 0; }
    .eligibility { display:inline-block; padding:5px 9px; border-radius:30px; font-size:10px; font-weight:800; }
    .eligible { background:#e7f8ef; color:#078249; }
    .ineligible { background:#ffedeb; color:#c92b21; }
    .pending { background:#fff4df; color:#b96905; }
    .selected { background:#e7f8ef; color:#078249; }
    .rejected { background:#ffedeb; color:#c92b21; }
    .upcoming { background:#eaf2ff; color:#1262df; }
    .upcoming-job { min-height:220px; padding:3px 2px; }
    .upcoming-job h3 { font:700 17px 'Manrope'; margin:10px 0 3px; color:#18233e; }
    .upcoming-job h4 { font-size:12px; color:var(--blue); margin:0 0 10px; }
    .opening-date { color:#1262df; font-size:11px; font-weight:800; margin:12px 0 7px; }
    .login-shell { max-width:1040px; margin:4vh auto 0; }
    .login-hero { background:linear-gradient(145deg,#081a44,#0d54c7); color:white; border-radius:20px; padding:48px; min-height:530px; display:flex; flex-direction:column; justify-content:space-between; }
    .login-hero h1 { color:white; font:800 50px/1.08 'Manrope'; letter-spacing:-.05em; margin:16px 0; }
    .login-hero p { color:#c9daf7; line-height:1.7; max-width:450px; }
    .login-hero small { color:#9fb7df; }
    .login-title { font:800 31px 'Manrope'; margin:45px 0 5px; }
    .login-copy { color:#667085; margin-bottom:22px; }
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button { border-radius:9px; font-weight:700; }
    div.stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button[kind="primary"] { background:var(--blue); border-color:var(--blue); }
    .demo-note { background:#edf4ff; border:1px solid #d6e5fc; border-radius:10px; padding:12px; font-size:11px; color:#355070; margin-top:14px; }
    .record { display:grid; grid-template-columns:1.4fr 1.3fr .8fr .8fr; gap:15px; align-items:center; padding:13px 4px; border-bottom:1px solid #edf0f5; font-size:12px; }
    .record strong { display:block; color:#27324b; }
    .record small { color:#8490a3; }
    .empty { text-align:center; padding:45px 15px; color:#7c879b; }
    @media(max-width:800px){ .login-hero{min-height:300px}.login-hero h1{font-size:38px}.record{grid-template-columns:1fr 1fr}.block-container{padding:1.1rem}.metric-card{min-height:110px} }
    </style>
    """,
    unsafe_allow_html=True,
)


def safe(value):
    return html.escape(str(value or ""))


def status_badge(status):
    return f'<span class="eligibility {safe(status).lower()}">{safe(status)}</span>'


def heading(label, title, subtitle):
    st.markdown(f'<div class="eyebrow">{safe(label)}</div><div class="page-title">{safe(title)}</div><div class="page-subtitle">{safe(subtitle)}</div>', unsafe_allow_html=True)


def metric_card(label, value, note):
    st.markdown(f'<div class="metric-card"><small>{safe(label)}</small><strong>{safe(value)}</strong><span>{safe(note)}</span></div>', unsafe_allow_html=True)


def friendly_date(value):
    try:
        return date.fromisoformat(str(value)).strftime("%d %b %Y")
    except ValueError:
        return str(value)


def flash(message, kind="success"):
    st.session_state.flash = (message, kind)


def show_flash():
    item = st.session_state.pop("flash", None)
    if item:
        message, kind = item
        getattr(st, kind if kind in {"success", "warning", "error", "info"} else "info")(message)


def sign_in(user):
    st.session_state.user = user
    st.session_state.page = "Overview"
    st.rerun()


def login_screen():
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    left, right = st.columns([1.08, 1], gap="large")
    with left:
        st.markdown(
            """<div class="login-hero"><div class="brand"><span class="brand-mark">P</span>PlacePro</div>
            <div><div class="eyebrow" style="color:#a9cbff">COLLEGE PLACEMENT MANAGEMENT</div>
            <h1>Build your future<br>with confidence.</h1><p>One reliable portal for opportunities, eligibility, applications and placement results.</p></div>
            <small>Web Technologies PBL · Working localhost demo</small></div>""",
            unsafe_allow_html=True,
        )
    with right:
        mode = st.radio("Account", ["Log in", "Student registration"], horizontal=True, label_visibility="collapsed")
        if mode == "Log in":
            st.markdown('<div class="login-title">Welcome back</div><div class="login-copy">Enter your details to open the placement portal.</div>', unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email address", placeholder="name@woxsen.edu.in")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Log in to portal", type="primary", use_container_width=True)
            if submitted:
                user = db.authenticate(email, password)
                if user:
                    sign_in(user)
                else:
                    st.error("Incorrect email or password.")

            st.markdown('<div class="demo-note"><strong>Fast demo access</strong><br>Both accounts use password: Demo@123</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("Open student demo", use_container_width=True):
                sign_in(db.authenticate("student@example.com", "Demo@123"))
            if c2.button("Open admin demo", use_container_width=True):
                sign_in(db.authenticate("admin@example.com", "Demo@123"))
        else:
            st.markdown('<div class="login-title">Create student account</div><div class="login-copy">Your details are used to check job eligibility.</div>', unsafe_allow_html=True)
            with st.form("register_form"):
                full_name = st.text_input("Full name")
                email = st.text_input("College email")
                c1, c2 = st.columns(2)
                department = c1.selectbox("Department", ["CSE", "IT", "ECE", "AI & DS", "Mechanical"])
                cgpa = c2.number_input("CGPA", min_value=0.0, max_value=10.0, value=8.0, step=0.01)
                phone = st.text_input("Phone number")
                password = st.text_input("Create password", type="password")
                submitted = st.form_submit_button("Create student account", type="primary", use_container_width=True)
            if submitted:
                if not full_name.strip() or not email.strip() or len(password) < 6:
                    st.error("Enter all details. Password must contain at least 6 characters.")
                else:
                    ok, message = db.register_student(full_name, email, password, department, cgpa, phone)
                    (st.success if ok else st.error)(message)
    st.markdown('</div>', unsafe_allow_html=True)


def sidebar(user):
    with st.sidebar:
        st.markdown('<div class="brand"><span class="brand-mark">P</span>PlacePro</div>', unsafe_allow_html=True)
        label = "ADMIN CONSOLE" if user["role"] == "admin" else "STUDENT PORTAL"
        st.markdown(f'<div class="side-label">{label}</div>', unsafe_allow_html=True)
        options = ["Overview", "Manage jobs", "Applications"] if user["role"] == "admin" else ["Overview", "Browse jobs", "My applications"]
        current = st.session_state.get("page", "Overview")
        if current not in options:
            current = "Overview"
        page = st.radio("Navigation", options, index=options.index(current), label_visibility="collapsed")
        st.session_state.page = page
        role_text = "Placement administrator" if user["role"] == "admin" else f'{user["department"]} · CGPA {user["cgpa"]:.2f}'
        st.markdown(f'<div class="side-user"><strong>{safe(user["full_name"])}</strong><span>{safe(role_text)}</span></div>', unsafe_allow_html=True)
        if st.button("Log out", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    return page


def application_rows(applications, admin=False):
    if not applications:
        st.markdown('<div class="empty">No applications found.</div>', unsafe_allow_html=True)
        return
    for app in applications:
        with st.container(border=True):
            cols = st.columns([1.35, 1.35, .8, 1.05])
            if admin:
                cols[0].markdown(f'**{safe(app["full_name"])}**  \n<small>{safe(app["department"])} · CGPA {app["cgpa"]:.2f}</small>', unsafe_allow_html=True)
            else:
                cols[0].markdown(f'**{safe(app["company_name"])}**  \n<small>{safe(app["job_role"])}</small>', unsafe_allow_html=True)
            if admin:
                cols[1].markdown(f'**{safe(app["company_name"])}**  \n<small>{safe(app["job_role"])}</small>', unsafe_allow_html=True)
            else:
                cols[1].markdown(f'{safe(app["location"])}  \n<small>{safe(app["salary"])}</small>', unsafe_allow_html=True)
            cols[2].markdown(f'<small>APPLIED ON</small><br>{safe(app["application_date"])}', unsafe_allow_html=True)
            if admin:
                with cols[3]:
                    status = st.selectbox("Status", ["Pending", "Selected", "Rejected"], index=["Pending", "Selected", "Rejected"].index(app["status"]), key=f'status_{app["application_id"]}', label_visibility="collapsed")
                    if st.button("Save status", key=f'save_{app["application_id"]}', use_container_width=True):
                        db.update_application_status(app["application_id"], status)
                        flash(f'{app["full_name"]} updated to {status}.')
                        st.rerun()
            else:
                cols[3].markdown(status_badge(app["status"]), unsafe_allow_html=True)


def student_overview(user):
    heading("STUDENT DASHBOARD", f'Good morning, {user["full_name"].split()[0]}', "Track opportunities and your placement progress.")
    stats = db.student_stats(user["user_id"])
    columns = st.columns(4)
    values = [("OPEN JOBS", stats["open_jobs"], "Available now"), ("APPLICATIONS", stats["total_applications"], "Total submitted"), ("PENDING", stats["pending_count"], "Under review"), ("SELECTED", stats["selected_count"], "Offers received")]
    for column, value in zip(columns, values):
        with column:
            metric_card(*value)
    st.write("")
    with st.container(border=True):
        st.markdown('<div class="eyebrow">FEATURED JOBS</div><div class="panel-title">Upcoming opportunities</div>', unsafe_allow_html=True)
        upcoming_jobs = db.upcoming_jobs_for_student(user["user_id"], 3)
        if not upcoming_jobs:
            st.markdown('<div class="empty">No upcoming opportunities have been announced yet.</div>', unsafe_allow_html=True)
        else:
            columns = st.columns(len(upcoming_jobs))
            for column, job in zip(columns, upcoming_jobs):
                eligibility = '<span class="eligibility eligible">Requirements matched</span>' if job["eligible"] else '<span class="eligibility ineligible">Requirements not matched</span>'
                day_text = "tomorrow" if job["days_until_open"] == 1 else f'in {job["days_until_open"]} days'
                with column:
                    with st.container(border=True):
                        st.markdown(
                            f'<div class="upcoming-job"><span class="eligibility upcoming">Upcoming</span>'
                            f'<h3>{safe(job["job_role"])}</h3><h4>{safe(job["company_name"])}</h4>'
                            f'<div class="job-meta">{safe(job["location"])} · {safe(job["salary"])}</div>'
                            f'<div class="opening-date">Applications open {safe(day_text)} · {safe(friendly_date(job["open_date"]))}</div>'
                            f'<div class="job-meta">{safe(job["required_department"])} department · Minimum CGPA {job["minimum_cgpa"]:.2f}</div>'
                            f'{eligibility}</div>',
                            unsafe_allow_html=True,
                        )
        st.caption("Upcoming opportunities are announcements only. The Apply button becomes available on the opening date.")
    st.write("")
    with st.container(border=True):
        st.markdown('<div class="eyebrow">RECENT ACTIVITY</div><div class="panel-title">Your latest applications</div>', unsafe_allow_html=True)
        application_rows(db.student_applications(user["user_id"], 4))


def browse_jobs(user):
    heading("OPPORTUNITIES", "Browse available jobs", "Eligibility is checked automatically using your department and CGPA.")
    search_col, filter_col = st.columns([2, 1])
    search = search_col.text_input("Search", placeholder="Search company, role or location", label_visibility="collapsed")
    eligibility_filter = filter_col.selectbox("Filter", ["All jobs", "Eligible for me"], label_visibility="collapsed")
    jobs = db.jobs_for_student(user["user_id"])
    jobs = [job for job in jobs if search.lower() in f'{job["company_name"]} {job["job_role"]} {job["location"]}'.lower()]
    if eligibility_filter == "Eligible for me":
        jobs = [job for job in jobs if job["eligible"]]
    if not jobs:
        st.info("No jobs match your search.")
        return
    for start in range(0, len(jobs), 2):
        cols = st.columns(2)
        for col, job in zip(cols, jobs[start:start + 2]):
            with col, st.container(border=True):
                eligible = bool(job["eligible"])
                badge = '<span class="eligibility eligible">Eligible</span>' if eligible else '<span class="eligibility ineligible">Not eligible</span>'
                st.markdown(f'<div class="job-card"><div class="company-letter">{safe(job["company_name"])[0]}</div>{badge}<h3>{safe(job["job_role"])}</h3><h4>{safe(job["company_name"])}</h4><div class="job-meta">{safe(job["location"])} · {safe(job["salary"])}</div><div class="job-description">{safe(job["description"])}</div><div class="rule"></div><div class="job-meta"><strong>{safe(job["required_department"])}</strong> department · Minimum CGPA <strong>{job["minimum_cgpa"]:.2f}</strong><br>Apply before {safe(job["last_date"])}</div></div>', unsafe_allow_html=True)
                if job["applied"]:
                    st.button("Application already submitted", key=f'applied_{job["job_id"]}', disabled=True, use_container_width=True)
                elif eligible:
                    if st.button("Apply now", key=f'apply_{job["job_id"]}', type="primary", use_container_width=True):
                        ok, message = db.apply_for_job(user["user_id"], job["job_id"])
                        flash(message, "success" if ok else "error")
                        st.rerun()
                else:
                    st.button("Eligibility requirements not met", key=f'ineligible_{job["job_id"]}', disabled=True, use_container_width=True)


def my_applications(user):
    heading("APPLICATION TRACKER", "My applications", "Follow every application from submission to final result.")
    application_rows(db.student_applications(user["user_id"]))


def admin_overview():
    heading("ADMIN DASHBOARD", "Placement overview", "Manage opportunities and review student outcomes.")
    stats = db.admin_stats()
    columns = st.columns(4)
    values = [("REGISTERED STUDENTS", stats["students"], "Student profiles"), ("OPEN JOBS", stats["open_jobs"], "Active opportunities"), ("APPLICATIONS", stats["applications"], "Across all jobs"), ("SELECTED", stats["selected_count"], "Student offers")]
    for column, value in zip(columns, values):
        with column:
            metric_card(*value)
    st.write("")
    with st.container(border=True):
        st.markdown('<div class="eyebrow">LATEST SUBMISSIONS</div><div class="panel-title">Recent applications</div>', unsafe_allow_html=True)
        application_rows(db.all_applications(limit=5), admin=True)


def manage_jobs():
    heading("JOB MANAGEMENT", "Placement opportunities", "Publish, review and remove company openings.")
    with st.expander("Add a new placement job", expanded=False):
        with st.form("add_job_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            company = c1.text_input("Company name")
            role = c2.text_input("Job role")
            location = c1.text_input("Location")
            salary = c2.text_input("Salary / package", placeholder="₹6.5 LPA")
            department = c1.selectbox("Required department", ["CSE", "IT", "ECE", "AI & DS", "Mechanical"])
            minimum_cgpa = c2.number_input("Minimum CGPA", 0.0, 10.0, 7.0, .1)
            open_date = c1.date_input("Applications open from", min_value=date.today(), value=date.today())
            last_date = c2.date_input("Application deadline", min_value=date.today(), value=date.today() + timedelta(days=20))
            description = st.text_area("Job description", max_chars=600)
            submitted = st.form_submit_button("Publish opportunity", type="primary", use_container_width=True)
        if submitted:
            if not all([company.strip(), role.strip(), location.strip(), salary.strip(), description.strip()]):
                st.error("Complete all job details.")
            elif last_date < open_date:
                st.error("The application deadline must be on or after the opening date.")
            else:
                db.add_job(company, role, location, salary, department, minimum_cgpa, open_date, last_date, description)
                message = "Upcoming opportunity scheduled successfully." if open_date > date.today() else "New placement job published successfully."
                flash(message)
                st.rerun()
    jobs = db.all_jobs()
    st.markdown(f'<div class="eyebrow">ALL OPPORTUNITIES</div><div class="panel-title">Published jobs · {len(jobs)} total</div>', unsafe_allow_html=True)
    for job in jobs:
        with st.container(border=True):
            cols = st.columns([1.5, 1.1, 1.05, .65, .45])
            cols[0].markdown(f'**{safe(job["company_name"])}**  \n<small>{safe(job["job_role"])} · {safe(job["location"])}</small>', unsafe_allow_html=True)
            cols[1].markdown(f'**{safe(job["required_department"])}**  \n<small>CGPA ≥ {job["minimum_cgpa"]:.2f}</small>', unsafe_allow_html=True)
            cols[2].markdown(f'{status_badge(job["availability"])}  \n<small>Opens {safe(friendly_date(job["open_date"]))}</small>', unsafe_allow_html=True)
            cols[3].markdown(f'<small>APPLICATIONS</small><br>**{job["application_count"]}**', unsafe_allow_html=True)
            if cols[4].button("Delete", key=f'delete_{job["job_id"]}'):
                db.delete_job(job["job_id"])
                flash(f'{job["company_name"]} job deleted.', "warning")
                st.rerun()


def manage_applications():
    heading("CANDIDATE MANAGEMENT", "Student applications", "Review candidates and update placement results.")
    status = st.selectbox("Application status", ["All", "Pending", "Selected", "Rejected"], label_visibility="collapsed")
    applications = db.all_applications(status)
    st.caption(f"{len(applications)} application records")
    application_rows(applications, admin=True)


def main():
    user = st.session_state.get("user")
    if not user:
        login_screen()
        return

    user = db.student_profile(user["user_id"]) if user["role"] == "student" else user
    st.session_state.user = user
    page = sidebar(user)
    show_flash()

    if user["role"] == "student":
        if page == "Overview": student_overview(user)
        elif page == "Browse jobs": browse_jobs(user)
        else: my_applications(user)
    else:
        if page == "Overview": admin_overview()
        elif page == "Manage jobs": manage_jobs()
        else: manage_applications()


if __name__ == "__main__":
    main()
