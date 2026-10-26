import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "PlacementHub — Comprehensive Project & Interview Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, page_text)
        self.drawString(54, 35, "Confidential — Prepared for Technical Placement Interviews")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 47, 558, 47)
        self.restoreState()

def build_pdf(filename="PlacementHub_Project_Interview_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#4f46e5")
    dark_color = colors.HexColor("#0f172a")
    accent_color = colors.HexColor("#059669")
    text_color = colors.HexColor("#334155")
    muted_color = colors.HexColor("#64748b")
    callout_bg = colors.HexColor("#f8fafc")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=muted_color,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=dark_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    q_style = ParagraphStyle(
        'Question_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e1b4b"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    a_style = ParagraphStyle(
        'Answer_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        leftIndent=10,
        spaceAfter=6
    )

    story = []

    # Title Banner Box
    title_data = [
        [
            Paragraph("<b>PlacementHub</b> — College Placement Management Portal", title_style),
        ],
        [
            Paragraph("<b>Complete Project Architectural Breakdown & Interview Preparation Guide</b>", subtitle_style),
        ],
        [
            Paragraph("<b>Author:</b> Candidate &bull; <b>Tech Stack:</b> Python, Django 6.1, SQLite, HTML5, Vanilla CSS / Bootstrap 5 &bull; <b>Pattern:</b> MTV", body_style)
        ]
    ]
    title_table = Table(title_data, colWidths=[504])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 14))

    # SECTION 1: 30-Second Elevator Pitch
    story.append(Paragraph("1. The 30-Second Elevator Pitch (For Interviewers)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))
    
    pitch_text = (
        "<b>\"Tell me about your project:\"</b><br/>"
        "<i>\"PlacementHub is a full-stack web application designed to streamline the campus placement ecosystem "
        "by bridging students and corporate recruiters on a single, secure platform. Built on Django's robust architecture, "
        "it implements Role-Based Access Control (RBAC) separating student and recruiter workflows. Students can maintain an academic profile "
        "with resume uploads, search and filter active job opportunities by skillset, location, and CGPA, and track their application lifecycle. "
        "Recruiters can register multiple company entities, publish job openings with eligibility criteria, review applicants with one-click resume verification, "
        "and advance candidate statuses in real time. The system prevents duplicate applications using database-level constraints and guarantees academic eligibility compliance.\"</i>"
    )
    pitch_table = Table([[Paragraph(pitch_text, callout_style)]], colWidths=[504])
    pitch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ecfdf5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#a7f3d0")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(pitch_table)
    story.append(Spacer(1, 12))

    # SECTION 2: System Architecture & Technologies
    story.append(Paragraph("2. System Architecture & Tech Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))
    
    arch_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology / Implementation</b>", body_style), Paragraph("<b>Role & Key Advantage</b>", body_style)],
        [
            Paragraph("<b>Backend Framework</b>", body_style),
            Paragraph("Python 3.13 / Django 6.1", body_style),
            Paragraph("Model-Template-View (MTV) pattern, built-in ORM, secure auth & CSRF protection.", body_style)
        ],
        [
            Paragraph("<b>Authentication & RBAC</b>", body_style),
            Paragraph("Custom <code>AbstractUser</code> with <code>role</code> field", body_style),
            Paragraph("Enforces strict permissions between <code>'student'</code> and <code>'recruiter'</code> roles.", body_style)
        ],
        [
            Paragraph("<b>Database Layer</b>", body_style),
            Paragraph("SQLite (Dev) / Relational Schema", body_style),
            Paragraph("Foreign keys with cascade deletion, unique multi-column constraints, index optimization.", body_style)
        ],
        [
            Paragraph("<b>Frontend UI/UX</b>", body_style),
            Paragraph("Vanilla CSS Design Tokens + Bootstrap 5 Grid", body_style),
            Paragraph("Dark aesthetic (HSL tokens, glassmorphism, responsive cards, micro-animations, no bloat).", body_style)
        ],
        [
            Paragraph("<b>Static & Media Storage</b>", body_style),
            Paragraph("Django Media Pipeline (resumes/)", body_style),
            Paragraph("Handles file uploads with validation, isolated storage, and served securely via MEDIA_URL.", body_style)
        ],
    ]
    arch_table = Table(arch_data, colWidths=[120, 160, 224])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 14))

    # SECTION 3: Data Models & Schema Design
    story.append(Paragraph("3. Data Modeling & Database Schema (Core Entities)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))
    story.append(Paragraph("The system is divided into modular Django apps following domain-driven design:", body_style))

    story.append(Paragraph("<b>1. accounts.User (extends AbstractUser)</b>", h2_style))
    story.append(Paragraph("&bull; Inherits standard Django security (username, hashed passwords, email, permissions).<br/>&bull; Adds <code>role</code>: Choice field with <code>'student'</code> and <code>'recruiter'</code>.<br/>&bull; Serves as the central identity model for all platform actors.", bullet_style))

    story.append(Paragraph("<b>2. students.StudentProfile (OneToOne &rarr; accounts.User)</b>", h2_style))
    story.append(Paragraph("&bull; Linked via <code>models.OneToOneField(settings.AUTH_USER_MODEL, related_name='student_profile')</code>.<br/>&bull; Fields: <code>full_name</code>, <code>department</code>, <code>graduation_year</code>, <code>cgpa</code> (DecimalField 4,2), <code>skills</code> (TextField), <code>resume</code> (FileField to <code>resumes/</code>).<br/>&bull; Property <code>skills_list</code>: dynamically splits and trims comma-separated skills for frontend badges.", bullet_style))

    story.append(Paragraph("<b>3. jobs.Company (ForeignKey &rarr; accounts.User)</b>", h2_style))
    story.append(Paragraph("&bull; Represents corporate entities registered by recruiters (a recruiter can manage multiple companies).<br/>&bull; Fields: <code>recruiter</code> (FK to User), <code>name</code>, <code>description</code>, <code>website</code> (URLField).", bullet_style))

    story.append(Paragraph("<b>4. jobs.Job (ForeignKey &rarr; Company)</b>", h2_style))
    story.append(Paragraph("&bull; Represents active or archived job openings.<br/>&bull; Fields: <code>company</code> (FK), <code>title</code>, <code>description</code>, <code>required_skills</code>, <code>minimum_cgpa</code> (DecimalField), <code>location</code>, <code>salary</code>, <code>deadline</code>, <code>is_active</code> (BooleanField), <code>created_at</code>.<br/>&bull; Property <code>skills_list</code>: parses skill strings into clean iterable badges.", bullet_style))

    story.append(Paragraph("<b>5. applications.Application (ForeignKey &rarr; User, ForeignKey &rarr; Job)</b>", h2_style))
    story.append(Paragraph("&bull; Connects student applicants to specific job postings.<br/>&bull; Fields: <code>student</code> (FK to User), <code>job</code> (FK to Job), <code>status</code> (Choices: <code>pending</code>, <code>shortlisted</code>, <code>selected</code>, <code>rejected</code>), <code>applied_at</code>.<br/>&bull; <b>Integrity Constraint:</b> <code>models.UniqueConstraint(fields=['student', 'job'], name='unique_student_job_application')</code> guarantees at the database level that no student can double-apply.", bullet_style))
    story.append(Spacer(1, 14))

    story.append(PageBreak())

    # SECTION 4: Dual Role Workflows
    story.append(Paragraph("4. End-to-End User Workflows", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    flow_data = [
        [Paragraph("<b>Student Workflow</b>", h2_style), Paragraph("<b>Recruiter Workflow</b>", h2_style)],
        [
            Paragraph(
                "<b>1. Registration & Auth:</b><br/>"
                "&bull; Registers with username, email, password, and role='student'.<br/>"
                "&bull; Auto-redirects to Student Dashboard.<br/><br/>"
                "<b>2. Profile & Resume Setup:</b><br/>"
                "&bull; Enters academic branch, grad year, CGPA, and key skills.<br/>"
                "&bull; Uploads verified PDF resume with inline status check.<br/><br/>"
                "<b>3. Job Discovery & Exploration:</b><br/>"
                "&bull; Accesses 'Browse Jobs' portal.<br/>"
                "&bull; Filters openings by keyword query (title, skills, company), location, and CGPA limit.<br/><br/>"
                "<b>4. Application & Eligibility Verification:</b><br/>"
                "&bull; System verifies student CGPA &ge; Job minimum CGPA.<br/>"
                "&bull; Visual indicator updates to 'Already Applied' button once submitted.<br/><br/>"
                "<b>5. Real-Time Tracking:</b><br/>"
                "&bull; Monitors application status (Pending &rarr; Shortlisted &rarr; Selected) on 'My Applications' dashboard.",
                body_style
            ),
            Paragraph(
                "<b>1. Registration & Auth:</b><br/>"
                "&bull; Registers with role='recruiter'.<br/>"
                "&bull; Directs to Recruiter Executive Command Center.<br/><br/>"
                "<b>2. Company Management:</b><br/>"
                "&bull; Adds multiple company profiles with logo, website, and description.<br/><br/>"
                "<b>3. Job Creation & Publishing:</b><br/>"
                "&bull; Creates job listings specifying salary package, location, required skills, and minimum CGPA criteria.<br/>"
                "&bull; Can toggle listings between Active and Inactive on the fly.<br/><br/>"
                "<b>4. Candidate Review Pipeline:</b><br/>"
                "&bull; Reviews applicants filtered by job opening or review status.<br/>"
                "&bull; Inspects candidate department, CGPA, and key skills.<br/>"
                "&bull; One-click preview of candidate's uploaded PDF resume.<br/><br/>"
                "<b>5. Decision Pipeline Management:</b><br/>"
                "&bull; Updates candidate status with zero scroll/filter loss (Shortlist, Select, Reject).",
                body_style
            )
        ]
    ]
    flow_table = Table(flow_data, colWidths=[246, 246])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f0fdf4")),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#f5f3ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 14))

    # SECTION 5: Key Technical Highlights & Challenges Solved
    story.append(Paragraph("5. Technical Challenges & Architectural Decisions", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))
    
    challenges = [
        ("Database-Level Concurrency & Integrity", 
         "Instead of relying on application-level checks that are vulnerable to race conditions, I implemented <code>models.UniqueConstraint(fields=['student', 'job'])</code>. Combined with <code>get_or_create()</code> in the view, this guarantees idempotency and zero duplicate applications."),
        
        ("Complex Multi-Criteria Dynamic Filtering", 
         "Implemented dynamic query building in <code>browse_jobs</code> and <code>recruiter_applications</code> using Django's <code>Q</code> objects. This allows simultaneous searching across multiple attributes (job title, description, skills, company name, candidate email, and academic branch) while chaining status and eligibility criteria."),
        
        ("Query Optimization with select_related", 
         "To prevent the classic 'N+1 query problem', all application queries utilize <code>select_related('student', 'student__student_profile', 'job', 'job__company')</code>. This executes an efficient SQL <code>JOIN</code> in a single query rather than hitting the database for every rendered row."),
        
        ("Preserving UI State on Mutation", 
         "When recruiters update application statuses from filtered tab views, the request carries a <code>next</code> parameter referencing <code>request.get_full_path</code>. The view redirects back to the referring state, eliminating context loss during bulk candidate evaluation."),
        
        ("Defensive Template Rendering", 
         "Created safe model properties (<code>skills_list</code>) rather than ad-hoc template filters, ensuring clean separation of concerns and preventing template rendering crashes when profiles or skill sets are partially filled.")
    ]

    for title, desc in challenges:
        story.append(Paragraph(f"<b>&bull; {title}:</b>", h2_style))
        story.append(Paragraph(desc, body_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # SECTION 6: High-Frequency Interview Questions & Answers
    story.append(Paragraph("6. Top Technical Interview Q&A (Rehearsal Sheet)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    qa_list = [
        (
            "Q1: Why did you choose Django for this project instead of Flask or FastAPI?",
            "<b>Answer:</b> Django was the optimal choice because a placement portal requires robust authentication, administrative controls, an ORM for relational modeling, and built-in security out of the box. Django's 'batteries-included' philosophy provides CSRF protection, SQL injection prevention, session management, and form validation natively, enabling rapid development without having to assemble multiple third-party libraries."
        ),
        (
            "Q2: How is Role-Based Access Control (RBAC) enforced across views?",
            "<b>Answer:</b> I extended <code>AbstractUser</code> with a <code>role</code> field (<code>'student'</code> vs <code>'recruiter'</code>). In the view layer, access is protected using a combination of the <code>@login_required</code> decorator and role-validation guards (e.g., <code>if request.user.role != 'recruiter': return redirect('home')</code>). On the template layer, conditional blocks dynamically adjust navigation menus and action buttons based on <code>user.role</code>."
        ),
        (
            "Q3: How do you prevent a student from applying to the same job twice?",
            "<b>Answer:</b> I solved this at both the database layer and the presentation layer. At the database layer, <code>Application.Meta</code> includes a <code>models.UniqueConstraint(fields=['student', 'job'])</code>. At the view layer, <code>get_or_create()</code> handles attempts gracefully. In the UI, the template checks if <code>job.id</code> exists in the student's <code>applied_job_ids</code> set, swapping the 'Apply' button for an inactive 'Already Applied' badge."
        ),
        (
            "Q4: How did you prevent the N+1 database query problem in the applications list?",
            "<b>Answer:</b> If a recruiter views 50 applications, fetching <code>application.student</code>, <code>application.student.student_profile</code>, <code>application.job</code>, and <code>application.job.company</code> individually would trigger over 200 SQL queries. I solved this by invoking <code>.select_related('student', 'student__student_profile', 'job', 'job__company')</code>, which performs SQL <code>JOIN</code> operations in one single database query."
        ),
        (
            "Q5: How are file uploads (resumes) managed securely?",
            "<b>Answer:</b> Resumes are handled through Django's <code>FileField(upload_to='resumes/')</code>. The model enforces an isolated subdirectory inside <code>MEDIA_ROOT</code>. Uploads are accepted only via <code>POST</code> with <code>enctype='multipart/form-data'</code> and validated through <code>StudentProfileForm</code> with <code>.pdf</code> constraints to prevent arbitrary script execution."
        ),
        (
            "Q6: How would you scale this application to support 50,000+ students and 500+ companies?",
            "<b>Answer:</b> In production, I would make several architectural enhancements:<br/>"
            "1. <b>Database:</b> Migrate from SQLite to PostgreSQL with read replicas and connection pooling (PgBouncer).<br/>"
            "2. <b>Media Storage:</b> Offload resume file storage from the web server to AWS S3 or Google Cloud Storage with pre-signed secure URLs.<br/>"
            "3. <b>Background Tasks:</b> Use Celery with Redis for asynchronous background tasks such as sending notification emails and parsing resumes.<br/>"
            "4. <b>Caching:</b> Implement Redis caching for high-read pages like job listings.<br/>"
            "5. <b>Pagination:</b> Implement server-side pagination with <code>Paginator</code> to limit payload sizes on large job/application lists."
        )
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, q_style))
        story.append(Paragraph(a, a_style))
        story.append(Spacer(1, 4))

    # SECTION 7: URL and App Sitemap Cheat Sheet
    story.append(Spacer(1, 6))
    story.append(Paragraph("7. Project Directory & Route Cheat Sheet", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=8))

    route_data = [
        [Paragraph("<b>App / Module</b>", body_style), Paragraph("<b>Route / URL Pattern</b>", body_style), Paragraph("<b>Target View & Role</b>", body_style)],
        [Paragraph("<b>core</b>", body_style), Paragraph("<code>/</code>", body_style), Paragraph("<code>home</code> &mdash; Landing page for all visitors", body_style)],
        [Paragraph("<b>accounts</b>", body_style), Paragraph("<code>/accounts/register/</code><br/><code>/accounts/login/</code><br/><code>/accounts/logout/</code>", body_style), Paragraph("User registration, session login, logout", body_style)],
        [Paragraph("<b>accounts</b>", body_style), Paragraph("<code>/accounts/student/dashboard/</code>", body_style), Paragraph("Student metrics command center", body_style)],
        [Paragraph("<b>accounts</b>", body_style), Paragraph("<code>/accounts/recruiter/dashboard/</code>", body_style), Paragraph("Recruiter company & job stats dashboard", body_style)],
        [Paragraph("<b>students</b>", body_style), Paragraph("<code>/students/profile/</code>", body_style), Paragraph("Student profile & resume management (Student)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/browse/</code>", body_style), Paragraph("Browse & search active jobs with filters (Student)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/&lt;id&gt;/apply/</code>", body_style), Paragraph("One-click apply with CGPA eligibility guard (Student)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/my-applications/</code>", body_style), Paragraph("Track status of applied jobs (Student)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/companies/</code><br/><code>/jobs/companies/create/</code>", body_style), Paragraph("Company list & registration (Recruiter)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/jobs/my-jobs/</code><br/><code>/jobs/jobs/create/</code>", body_style), Paragraph("Job postings management & job creation (Recruiter)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/jobs/&lt;id&gt;/toggle/</code>", body_style), Paragraph("Activate / Deactivate job posting (Recruiter)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/applications/</code>", body_style), Paragraph("Filter candidates & resume review (Recruiter)", body_style)],
        [Paragraph("<b>jobs</b>", body_style), Paragraph("<code>/jobs/applications/&lt;id&gt;/update/</code>", body_style), Paragraph("Advance candidate status in pipeline (Recruiter)", body_style)],
    ]
    route_table = Table(route_data, colWidths=[80, 180, 244])
    route_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(route_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {filename}")

if __name__ == '__main__':
    build_pdf()
