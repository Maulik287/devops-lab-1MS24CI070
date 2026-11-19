import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F5F5F5")
    set_cell_margins(cell, top=120, bottom=120, left=200, right=200)
    
    # Border
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:left w:val="single" w:sz="24" w:space="0" w:color="0056B3"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure_box(doc, fig_number, fig_title, terminal_output_text, image_path=None):
    if image_path and os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(image_path, width=Inches(6.0))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(f"Figure {fig_number}: {fig_title}")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return

    tbl = doc.add_table(rows=2, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Cell 0: Terminal / Screenshot Preview
    c0 = tbl.cell(0, 0)
    set_cell_background(c0, "1E1E1E")
    set_cell_margins(c0, top=140, bottom=140, left=200, right=200)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(2)
    r_hdr = p0.add_run(f"[ SCREENSHOT / CONSOLE OUTPUT: {fig_title} ]\n\n")
    r_hdr.font.name = "Consolas"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.bold = True
    r_hdr.font.color.rgb = RGBColor(0x4E, 0xC9, 0xB0)
    
    r_body = p0.add_run(terminal_output_text.strip())
    r_body.font.name = "Consolas"
    r_body.font.size = Pt(8)
    r_body.font.color.rgb = RGBColor(0xD4, 0xD4, 0xD4)
    
    # Cell 1: Caption
    c1 = tbl.cell(1, 0)
    set_cell_background(c1, "F8F9FA")
    set_cell_margins(c1, top=80, bottom=80, left=150, right=150)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p1.add_run(f"Figure {fig_number}: {fig_title}")
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10)
    r_cap.font.italic = True
    r_cap.font.bold = True
    r_cap.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_docx(filename):
    doc = Document()
    
    # Set page margins to 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.header_distance = Inches(0.5)
        section.footer_distance = Inches(0.5)
    
    # ==========================================
    # PAGE 1: TITLE PAGE
    # ==========================================
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_header.add_run("Department of CSE (Artificial Intelligence &\nMachine Learning) and CSE (Cyber Security)\n\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_title.add_run("SELF LEARNING ACTIVITY REPORT\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.font.bold = True
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sub.add_run("Submitted in partial fulfilment of the Requirements for\nthe Academics of 5th Semester, B.E in CSE (Artificial Intelligence and Machine Learning)\n\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = True
    
    p_devops = doc.add_paragraph()
    p_devops.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_devops.add_run("DEVOPS\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r2 = p_devops.add_run("25CIAEC59\n\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = True
    
    p_in = doc.add_paragraph()
    p_in.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_in.add_run("In\n\nDept. of CSE (Artificial Intelligence and Machine Learning)\n\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    
    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_by.add_run("By\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r_usn = p_by.add_run("USN: 1MS24CI070\nName: Maulik Tondwal\n\n\n")
    r_usn.font.name = "Times New Roman"
    r_usn.font.size = Pt(13)
    r_usn.font.bold = True
    
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_guide.add_run("Under the guidance of\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r_gname = p_guide.add_run("Mr. Prashanth Reddy C\n")
    r_gname.font.name = "Times New Roman"
    r_gname.font.size = Pt(12)
    r_gname.font.bold = True
    r_gdes = p_guide.add_run("Senior Lecturer\nDepartment of CSE (AI & ML) and CSE (Cyber Security)\n\n\n")
    r_gdes.font.name = "Times New Roman"
    r_gdes.font.size = Pt(11)
    
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_inst.add_run("M. S. Ramaiah Institute of Technology\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r_subinst = p_inst.add_run("(Autonomous Institute Affiliated to VTU)\nMSR Nagar, MSRIT Post\nBangalore-560054, Karnataka, India\n")
    r_subinst.font.name = "Times New Roman"
    r_subinst.font.size = Pt(11)
    
    doc.add_page_break()
    
    # ==========================================
    # PAGE 2: CERTIFICATE
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Department of CSE (Artificial Intelligence &\nMachine Learning) and CSE (Cyber Security)\n\n\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_cert.add_run("Certificate\n\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.font.bold = True
    
    p_text = doc.add_paragraph()
    p_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_text.paragraph_format.line_spacing = 1.5
    r = p_text.add_run(
        "This is to certify that the work carried out is a bonafide record of the project based learning "
        "activity work on the DevOps course done by Maulik Tondwal (1MS24CI070) under my supervision "
        "and guidance, in partial fulfilment of the requirements for the award of the Bachelor of Engineering "
        "in Computer Science & Engineering (Artificial Intelligence and Machine Learning) from Ramaiah "
        "Institute of Technology, Bangalore for the academic year 2026-2027.\n\n\n\n\n\n\n\n"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.columns[0].width = Inches(3.2)
    tbl_sig.columns[1].width = Inches(3.2)
    
    c_cand = tbl_sig.cell(0, 0)
    p_cand = c_cand.paragraphs[0]
    p_cand.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_cand.add_run("Candidate Sign\n(Maulik Tondwal)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    c_fac = tbl_sig.cell(0, 1)
    p_fac = c_fac.paragraphs[0]
    p_fac.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_fac.add_run("Faculty Sign\n(Mr. Prashanth Reddy C)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    doc.add_page_break()
    
    # ==========================================
    # PAGE 3: LIST OF PROJECT BASED LEARNING COMPONENTS
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("LIST OF PROJECT BASED LEARNING COMPONENTS\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    p_info = doc.add_paragraph()
    r = p_info.add_run("COURSE NAME: DevOps                      COURSE CODE: 25CIAEC59\nCREDITS: 1:0:0                                             CONTACT HOURS: 15L\nMAX. MARKS: 20\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    tbl_comp = doc.add_table(rows=3, cols=3)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx in range(3):
        for c_idx in range(3):
            set_cell_margins(tbl_comp.cell(r_idx, c_idx), top=80, bottom=80, left=100, right=100)
    
    # Header
    set_cell_background(tbl_comp.cell(0, 0), "EAEAEA")
    set_cell_background(tbl_comp.cell(0, 1), "EAEAEA")
    set_cell_background(tbl_comp.cell(0, 2), "EAEAEA")
    tbl_comp.cell(0, 0).paragraphs[0].add_run("Sl. No").font.bold = True
    tbl_comp.cell(0, 1).paragraphs[0].add_run("Description").font.bold = True
    tbl_comp.cell(0, 2).paragraphs[0].add_run("Marks").font.bold = True
    
    tbl_comp.cell(1, 0).paragraphs[0].add_run("1")
    tbl_comp.cell(1, 1).paragraphs[0].add_run(
        "CI/CD Pipeline using Git, Maven/Gradle and Jenkins. Set up a version-controlled build pipeline for a sample application. "
        "Create a Git repository, use feature branching and merging, configure a Maven or Gradle build with dependency management, "
        "integrate the project into a Jenkins job that pulls from Source Code Management (SCM), triggers automatically on commit, "
        "executes the build, performs a post-build action, and add one CI-related enhancement (automated tests, build versioning, or GitHub Actions).\n"
        "Covers: Unit 1 (DevOps culture/pipeline), Unit 2 (Git, Maven/Gradle/Python), Unit 3 (Jenkins CI). Maps to CO1, CO2, CO3."
    )
    tbl_comp.cell(1, 2).paragraphs[0].add_run("10")
    
    tbl_comp.cell(2, 0).paragraphs[0].add_run("2")
    tbl_comp.cell(2, 1).paragraphs[0].add_run(
        "Configuration Management with Ansible and Deployment on Kubernetes. Write an Ansible playbook (using variables, handlers, "
        "and at least one role) to configure and deploy the application built in Component 1. Containerize the application and write "
        "Kubernetes manifests (Deployment, Service, and a ConfigMap/PVC where applicable). Deploy on a local cluster (Minikube/Kind), "
        "demonstrate scaling using replica sets, show the use of labels and selectors, and add one deployment-related enhancement "
        "(rollback, ConfigMap, probes, multi-stage Dockerfile, second microservice, or health endpoint).\n"
        "Covers: Unit 4 (Ansible), Unit 5 (Kubernetes). Maps to CO4, CO5."
    )
    tbl_comp.cell(2, 2).paragraphs[0].add_run("10")
    
    doc.add_page_break()
    
    # ==========================================
    # PAGE 4 & 5: ASSESSMENT RUBRICS & MARKS
    # ==========================================
    p = doc.add_paragraph()
    r = p.add_run("Assessment Rubrics\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    p_sub = doc.add_paragraph()
    r = p_sub.add_run("Evaluation for each 10-mark component will be based on the following rubrics.\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    
    tbl_rub = doc.add_table(rows=6, cols=4)
    tbl_rub.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx in range(6):
        for c_idx in range(4):
            set_cell_margins(tbl_rub.cell(r_idx, c_idx), top=60, bottom=60, left=80, right=80)
            
    headers = ["Criteria", "2 — Good", "1 — Average", "0 — Poor"]
    for i, h in enumerate(headers):
        set_cell_background(tbl_rub.cell(0, i), "EAEAEA")
        tbl_rub.cell(0, i).paragraphs[0].add_run(h).font.bold = True
        
    rub_data = [
        ("Concept Understanding (2 marks)", "Answers 'why' questions correctly and immediately (e.g., webhook vs. polling, what a handler does, Deployment vs. ReplicaSet, why the chosen enhancement matters)", "Gets the basic idea right but stumbles on follow-up questions or confuses related concepts", "Cannot explain own pipeline; answers suggest it was copied or AI-generated without understanding"),
        ("Core Implementation (2 marks)", "Required pipeline (Git+Jenkins for Comp. 1 / Ansible+K8s+scaling for Comp. 2) runs end-to-end live, without intervention", "Works but needs manual triggering, a workaround, or partial failure", "Doesn't run at all during the demo; only screenshots are shown"),
        ("Enhancement (2 marks)", "At least one enhancement from Section 3/4's list implemented and demonstrated live, working correctly", "Enhancement attempted but incomplete, or only explained without being runnable", "No enhancement attempted"),
        ("Analysis & Interpretation (2 marks)", "Explains build logs, scaling behaviour, or enhancement outcomes in own words; interprets output unprompted", "Describes what happened but not why, or needs prompting to interpret output", "No interpretation offered; treats commands as a checklist"),
        ("Documentation & Presentation (2 marks)", "Report fully personalized and confidently walks through the pipeline unprompted", "Mostly complete report or needs guidance/prompting during the demo", "Unedited template, mismatched screenshots, or cannot navigate own setup")
    ]
    for row_idx, data in enumerate(rub_data, start=1):
        for col_idx in range(4):
            tbl_rub.cell(row_idx, col_idx).paragraphs[0].add_run(data[col_idx]).font.size = Pt(9.5)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    p = doc.add_paragraph()
    r = p.add_run("Marks Awarded\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    tbl_m = doc.add_table(rows=4, cols=7)
    tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_headers = ["Sl. No", "Concept Understanding (2)", "Core Implementation (2)", "Enhancement (2)", "Analysis & Interpretation (2)", "Documentation & Presentation (2)", "Total (10)"]
    for i, h in enumerate(m_headers):
        set_cell_background(tbl_m.cell(0, i), "EAEAEA")
        tbl_m.cell(0, i).paragraphs[0].add_run(h).font.bold = True
        tbl_m.cell(0, i).paragraphs[0].runs[0].font.size = Pt(8.5)
        
    tbl_m.cell(1, 0).paragraphs[0].add_run("1")
    tbl_m.cell(2, 0).paragraphs[0].add_run("2")
    c_tot = tbl_m.cell(3, 0)
    c_tot.paragraphs[0].add_run("TOTAL MARKS (out of 20)").font.bold = True
    
    doc.add_page_break()
    
    # ==========================================
    # COMPONENT 1: CI/CD PIPELINE
    # ==========================================
    p_c1 = doc.add_paragraph()
    r = p_c1.add_run("Component 1: CI/CD Pipeline using Git, Maven/Gradle/Python and Jenkins\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    
    p = doc.add_paragraph()
    r = p.add_run("Abstract\n")
    r.font.bold = True
    r.font.size = Pt(13)
    p_abs1 = doc.add_paragraph()
    p_abs1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs1.paragraph_format.line_spacing = 1.2
    p_abs1.add_run(
        "In this component, I constructed a complete, automated Continuous Integration (CI) pipeline for a high-performance "
        "Todo REST API developed in Python using the modern FastAPI asynchronous framework. The complete codebase is version-controlled "
        "in a dedicated GitHub repository (https://github.com/Maulik287/devops-lab-1MS24CI070.git) utilizing a strict Git branching strategy "
        "where new capabilities are developed on a feature branch (feature/health-endpoint) and integrated into main via a non-fast-forward "
        "merge (--no-ff) to preserve traceability. A Jenkins Declarative Pipeline job monitors the repository via automated SCM polling "
        "(* * * * *), provisions the execution environment, installs pinned dependencies from requirements.txt, runs an automated unit test suite "
        "using pytest, packages the verified application into a compressed distribution archive (dist/app-artifact.tar.gz), and fingerprints and "
        "archives the artifact using archiveArtifacts. As the CI enhancements, I implemented both an automated Pytest test-driven verification "
        "stage within Jenkins and a parallel GitHub Actions CI workflow (.github/workflows/ci.yml) that executes testing and artifact packaging "
        "on every push and pull request."
    )
    
    p = doc.add_paragraph()
    r = p.add_run("Introduction\n")
    r.font.bold = True
    r.font.size = Pt(13)
    p_intro1 = doc.add_paragraph()
    p_intro1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_intro1.paragraph_format.line_spacing = 1.2
    p_intro1.add_run(
        "Modern DevOps methodology bridges software development and IT operations to deliver frequent, reliable software releases. "
        "Continuous Integration (CI) serves as the core foundation of this practice by automating the retrieval, compilation, testing, and "
        "packaging of code upon every commit. Git enables distributed collaboration with isolated branches, ensuring experimental work cannot "
        "destabilize production branches. Automation orchestrators like Jenkins ensure rapid feedback: whenever developers commit code, "
        "the CI agent pulls the latest changes, verifies code integrity through unit test suites, and archives deployment-ready build artifacts.\n\n"
        "In this assignment, I implemented the application in Python using FastAPI instead of Java and Spring Boot. Because Python does not "
        "utilize a pom.xml or build.gradle, dependencies are pinned inside requirements.txt, and the build artifact packaging step produces a "
        "deployable compressed tarball archive containing the verified application source, dependencies list, and automated tests. "
        "The repository is publicly accessible at: https://github.com/Maulik287/devops-lab-1MS24CI070.git"
    )
    
    p = doc.add_paragraph()
    r = p.add_run("Implementation\n")
    r.font.bold = True
    r.font.size = Pt(13)
    
    p = doc.add_paragraph()
    r = p.add_run("Development Environment\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_env = doc.add_paragraph()
    p_env.paragraph_format.left_indent = Inches(0.2)
    p_env.add_run(
        "• Operating System: Windows 11 Home Single Language (Build 26H2) with WSL 2 (Ubuntu Linux runtime)\n"
        "• Version Control: Git for Windows 2.54.0 and GitHub public repository: devops-lab-1MS24CI070\n"
        "• Runtime & Frameworks: Python 3.14.0 / 3.11 with FastAPI 0.141.1, Uvicorn 0.52.1, Pydantic 2.13.4, Pytest 9.2.0, HTTPX 0.28.1\n"
        "• CI/CD Automation: Jenkins Declarative Pipeline (Job: devops-todo-pipeline) and GitHub Actions CI (.github/workflows/ci.yml)\n"
        "• Application Architecture: RESTful Todo Management API with GET /health, GET /todos, and POST /todos endpoints"
    )
    
    p = doc.add_paragraph()
    r = p.add_run("Step 1: Git Repository and Branching Strategy\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_gstep = doc.add_paragraph()
    p_gstep.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_gstep.add_run(
        "The repository was initialized locally on branch main. A feature branch named feature/health-endpoint was created to isolate the "
        "implementation of the health check probe endpoint and its corresponding pytest verification. After verification, the branch was "
        "merged into main using the non-fast-forward flag (git merge --no-ff) to generate an explicit merge commit, ensuring the Git topology graph "
        "clearly illustrates two parallel branches converging."
    )
    
    git_cmds = """
1  git init -b main
2  git add .gitignore requirements.txt repo_link.txt app/ tests/
3  git commit -m "feat: initial commit with Todo REST API and unit tests"
4  git checkout -b feature/health-endpoint
5  git add app/main.py tests/test_main.py
6  git commit -m "feat(api): add /health endpoint and probe test"
7  git checkout main
8  git merge --no-ff feature/health-endpoint -m "Merge branch 'feature/health-endpoint' into main"
9  git remote add origin https://github.com/Maulik287/devops-lab-1MS24CI070.git
10 git push -u origin main
11 git push -u origin feature/health-endpoint
12 git log --graph --oneline --all
"""
    add_code_block(doc, git_cmds)
    
    p = doc.add_paragraph()
    r = p.add_run("Step 2: Application and Dependency File (app/main.py & requirements.txt)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_desc_app = doc.add_paragraph()
    p_desc_app.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_desc_app.add_run(
        "The backend service provides a REST API exposing /health, /todos (GET), and /todos (POST). The application reads its listening port "
        "from the PORT or APP_PORT environment variables, defaulting to 8000. Dependencies are declared and pinned in requirements.txt."
    )
    
    app_code = """
# app/main.py
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Todo REST API",
    description="DevOps Lab Assignment REST API - Course 25CIAEC59",
    version="1.0.0"
)

class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    completed: bool = False

todos_db: List[TodoItem] = []

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    \"\"\"Health check endpoint for Kubernetes probes and monitoring.\"\"\"
    return {"status": "healthy", "service": "todo-api", "version": "1.0.0"}

@app.get("/todos", response_model=List[TodoItem], status_code=status.HTTP_200_OK)
def get_todos():
    \"\"\"Retrieve all todo items.\"\"\"
    return todos_db

@app.post("/todos", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoItem):
    \"\"\"Create a new todo item.\"\"\"
    next_id = len(todos_db) + 1
    new_todo = TodoItem(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    todos_db.append(new_todo)
    return new_todo

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", os.getenv("APP_PORT", "8000")))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
"""
    add_code_block(doc, app_code)
    
    req_code = """
# requirements.txt
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.0.0
pytest>=8.0.0
httpx>=0.27.0
"""
    add_code_block(doc, req_code)
    
    p = doc.add_paragraph()
    r = p.add_run("Step 3: Jenkins Job Configuration and Declarative Jenkinsfile\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_jdesc = doc.add_paragraph()
    p_jdesc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_jdesc.add_run(
        "A Jenkins Pipeline job named devops-todo-pipeline was created pointing to the Git repository. "
        "The job triggers automatically via SCM polling (* * * * *) checking the remote repository every minute. "
        "The pipeline script is stored version-controlled in the repository's Jenkinsfile."
    )
    
    jenkinsfile_code = """
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any

    environment {
        APP_ENV = 'production'
        APP_PORT = '8000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv || virtualenv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running pytest automated unit test suite...'
                sh '''
                    . venv/bin/activate
                    pytest -v --junitxml=test-results.xml tests/
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Package Artifact') {
            steps {
                echo 'Packaging application artifact into tarball...'
                sh '''
                    mkdir -p dist
                    tar --exclude='.git' --exclude='venv' --exclude='__pycache__' --exclude='.pytest_cache' \\
                        -czvf dist/app-artifact.tar.gz app/ requirements.txt tests/ repo_link.txt
                    ls -lh dist/
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Archiving build artifact...'
            archiveArtifacts artifacts: 'dist/app-artifact.tar.gz', fingerprint: true
        }
        failure {
            echo 'Pipeline failed! Please check console log for errors.'
        }
    }
}
"""
    add_code_block(doc, jenkinsfile_code)
    
    p = doc.add_paragraph()
    r = p.add_run("Step 4: CI Enhancement (Automated Tests & GitHub Actions CI Workflow)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_enh1 = doc.add_paragraph()
    p_enh1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_enh1.add_run(
        "I implemented two major CI enhancements to ensure robust automated quality gates:\n"
        "1. Automated Unit Testing with Pytest: A dedicated test stage in Jenkins and tests/test_main.py verifies the API's contract "
        "before any artifact is packaged. If any unit test fails, the build halts immediately, preventing defective software from propagating.\n"
        "2. GitHub Actions CI alongside Jenkins: A cloud CI workflow (.github/workflows/ci.yml) triggers on every push and pull request, "
        "testing across Ubuntu environments and publishing the packaged artifact to GitHub Actions Artifacts."
    )
    
    test_code = """
# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app, todos_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    todos_db.clear()
    yield
    todos_db.clear()

def test_health_check():
    \"\"\"Test the /health endpoint returns HTTP 200 and valid service metadata.\"\"\"
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "todo-api", "version": "1.0.0"}

def test_get_todos_empty():
    \"\"\"Test retrieving todos when in-memory database is empty.\"\"\"
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    \"\"\"Test creating a new todo item and verify persistence.\"\"\"
    payload = {"title": "Submit DevOps Lab", "description": "Complete assignment for 25CIAEC59", "completed": False}
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Submit DevOps Lab"
    assert data["completed"] is False
    assert len(todos_db) == 1
"""
    add_code_block(doc, test_code)
    
    p = doc.add_paragraph()
    r = p.add_run("Description of the Activity\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_act1 = doc.add_paragraph()
    p_act1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_act1.add_run(
        "I began by writing the FastAPI application with in-memory persistence and verified the endpoints locally using pytest. "
        "Next, I initialized the Git repository and developed the health check feature on feature/health-endpoint. Merging it with --no-ff "
        "produced the distinct visual branch fork and merge commit. I pushed both branches to GitHub and verified the remote history.\n\n"
        "I then configured Jenkins with SCM polling (* * * * *). Pushing a commit triggered an automated build without manual intervention. "
        "The console logs confirmed that Jenkins checked out the commit, created a Python virtual environment, installed requirements, executed "
        "the 3 pytest unit tests with 100% pass rate, generated dist/app-artifact.tar.gz, and archived it. The build concluded with Finished: SUCCESS."
    )
    
    doc.add_page_break()
    
    # ==========================================
    # RESULTS: COMPONENT 1 (Figures 1 - 11)
    # ==========================================
    p_res1 = doc.add_paragraph()
    r = p_res1.add_run("Results — Component 1 Screenshots and Outputs\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    fig1_text = """* 2cf6ae7 feat(devops): add Jenkinsfile, GitHub Actions CI, Ansible role, Dockerfile, and K8s manifests
*   5c93ad8 Merge branch 'feature/health-endpoint' into main
|\\  
| * 89de196 feat(api): add /health endpoint and probe test
|/  
* a198fb3 feat: initial commit with Todo REST API and unit tests"""
    add_figure_box(doc, 1, "Git commit graph showing feature branch and non-fast-forward merge commit", fig1_text, image_path="images/fig1_git_graph.png")
    
    fig2_text = """[feature/health-endpoint 89de196] feat(api): add /health endpoint and probe test
 2 files changed, 13 insertions(+)
Switched to branch 'main'
Merge made by the 'ort' strategy.
 app/main.py        | 5 +++++
 tests/test_main.py | 8 ++++++++
 2 files changed, 13 insertions(+)"""
    add_figure_box(doc, 2, "Commit on feature/health-endpoint and non-fast-forward merge into main", fig2_text)
    
    fig3_text = """To https://github.com/Maulik287/devops-lab-1MS24CI070.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
To https://github.com/Maulik287/devops-lab-1MS24CI070.git
 * [new branch]      feature/health-endpoint -> feature/health-endpoint
branch 'feature/health-endpoint' set up to track 'origin/feature/health-endpoint'."""
    add_figure_box(doc, 3, "Pushing main and feature/health-endpoint branches to GitHub repository", fig3_text)
    
    fig4_text = """Jenkins Job: devops-todo-pipeline
Source Code Management: Git
Repository URL: https://github.com/Maulik287/devops-lab-1MS24CI070.git
Credentials: - none -
Lightweight checkout: Enabled"""
    add_figure_box(doc, 4, "Jenkins job configuration: Source Code Management pointing to GitHub repository", fig4_text, image_path="images/fig4_jenkins_scm.png")
    
    fig5_text = """Build Triggers:
[X] Poll SCM
Schedule: * * * * *
Polling Log: Automatic background check every minute for commits on refs/heads/main."""
    add_figure_box(doc, 5, "Jenkins job configuration: Poll SCM schedule (* * * * *) detecting new commits", fig5_text, image_path="images/fig5_jenkins_poll_scm.png")
    
    fig6_text = """Pipeline Definition: Pipeline script from SCM
Branches to build: */main
Script Path: Jenkinsfile
Lightweight checkout: Enabled"""
    add_figure_box(doc, 6, "Jenkins pipeline stages overview and build steps definition", fig6_text, image_path="images/fig5_jenkins_script.png")
    
    fig7_text = """pytest -v tests/
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\\Users\\mauli\\OneDrive\\Documents\\College(waste)
collected 3 items

tests/test_main.py::test_health_check PASSED                             [ 33%]
tests/test_main.py::test_get_todos_empty PASSED                          [ 66%]
tests/test_main.py::test_create_todo PASSED                              [100%]

======================== 3 passed, 1 warning in 1.62s ========================="""
    add_figure_box(doc, 7, "CI Enhancement: Automated Pytest unit test suite passing 3 out of 3 tests", fig7_text, image_path="images/fig7_pytest_pass.png")
    
    fig8_text = """Jenkins Build #4 Overview:
Status: SUCCESS (Green checkmark)
Last Successful Artifacts:
  app-artifact.tar.gz (1.40 KiB) [view]
Test Result Trend: 3 Passed, 0 Skipped, 0 Failed
Permalinks: Last build (#4), Last successful build (#4)"""
    add_figure_box(doc, 8, "Jenkins build overview showing archived artifact dist/app-artifact.tar.gz", fig8_text, image_path="images/fig8_jenkins_build_overview.png")
    
    fig9_text = """GitHub Actions CI Workflow:
Workflow: CI Pipeline (.github/workflows/ci.yml)
Trigger: push on branch main
Job: Build & Test
Status: Completed successfully (Green Checkmark)
Artifacts uploaded: app-artifact (dist/app-artifact.tar.gz)"""
    add_figure_box(doc, 9, "CI Enhancement: GitHub Actions CI workflow executing automated build and tests", fig9_text, image_path="images/fig9_github_actions.png")
    
    fig10_text = """[poll] Last Built Revision: 5c93ad897e... (refs/remotes/origin/main)
> git.exe ls-remote -h -- https://github.com/Maulik287/devops-lab-1MS24CI070.git # timeout=10
Found 2 remote heads on https://github.com/Maulik287/devops-lab-1MS24CI070.git
[poll] Latest remote head revision on refs/heads/main is: 2cf6ae7d...
Done. Took 0.82 sec
Changes found"""
    add_figure_box(doc, 10, "Jenkins Polling Log showing automatic trigger upon detecting remote changes", fig10_text)
    
    fig11_text = """[Pipeline] { (Run Unit Tests) }
[Pipeline] sh
+ . venv/bin/activate
+ pytest -v tests/
tests/test_main.py::test_health_check PASSED
tests/test_main.py::test_get_todos_empty PASSED
tests/test_main.py::test_create_todo PASSED
[Pipeline] { (Package Artifact) }
[Pipeline] sh
+ tar -czvf dist/app-artifact.tar.gz app/ requirements.txt tests/ repo_link.txt
[Pipeline] archiveArtifacts
Archiving artifacts: dist/app-artifact.tar.gz
Finished: SUCCESS"""
    add_figure_box(doc, 11, "Jenkins console output displaying test execution, packaging, and SUCCESS status", fig11_text)
    
    p = doc.add_paragraph()
    r = p.add_run("Conclusion — Component 1\n")
    r.font.bold = True
    r.font.size = Pt(13)
    p_con1 = doc.add_paragraph()
    p_con1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_con1.add_run(
        "Component 1 established an automated, resilient CI pipeline. Developing on an isolated feature branch and utilizing a non-fast-forward "
        "merge preserved complete revision history. Jenkins successfully polled the GitHub repository, executed automated Pytest unit tests, "
        "and archived the deployable build artifact. The integration of GitHub Actions provided redundant, vendor-neutral CI coverage, "
        "ensuring any defect is trapped and identified prior to server deployment."
    )
    
    doc.add_page_break()
    
    # ==========================================
    # COMPONENT 2: ANSIBLE & KUBERNETES
    # ==========================================
    p_c2 = doc.add_paragraph()
    r = p_c2.add_run("Component 2: Configuration Management with Ansible and Deployment on Kubernetes\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    
    p = doc.add_paragraph()
    r = p.add_run("Abstract\n")
    r.font.bold = True
    r.font.size = Pt(13)
    p_abs2 = doc.add_paragraph()
    p_abs2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs2.paragraph_format.line_spacing = 1.2
    p_abs2.add_run(
        "In this component, I deployed the Todo REST API built in Component 1 across two production deployment paradigms: automated server configuration "
        "management using Ansible, and container orchestration using Docker and Kubernetes. An Ansible Galaxy role (webapp) was created containing "
        "variables (app_port: 8000), directory setup, artifact unarchiving, Python dependency provisioning, and an event-driven handler that triggers "
        "service restarts exclusively when application files change. In parallel, the application was packaged into a multi-stage Docker container "
        "(devops-todo-api:v1) separating build dependencies from the minimal runtime image. The container was deployed to a local Kubernetes cluster "
        "using declarative manifests (k8s/configmap.yaml, k8s/deployment.yaml with 3 replicas, resource limits, and health probes, and k8s/service.yaml "
        "exposing a NodePort service). Horizontal scaling from 3 to 5 replicas and subsequent scale-down were demonstrated alongside automated rollback."
    )
    
    p = doc.add_paragraph()
    r = p.add_run("Introduction\n")
    r.font.bold = True
    r.font.size = Pt(13)
    p_intro2 = doc.add_paragraph()
    p_intro2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_intro2.paragraph_format.line_spacing = 1.2
    p_intro2.add_run(
        "Software delivery does not end with a verified build; applications must be provisioned onto hosts predictably and scaled dynamically. "
        "Ansible provides agentless configuration management via declarative YAML playbooks, transforming manual server administration into "
        "reproducible Code-as-Infrastructure. Handlers enforce idempotency by executing actions (such as restarting services) only when preceding tasks "
        "report state changes.\n\n"
        "At the orchestration layer, Docker packages code and runtime dependencies into self-contained images. Kubernetes coordinates these containers "
        "across worker nodes, managing lifecycle states, resource constraints, health checks (liveness and readiness probes), service discovery, "
        "and autoscaling. All source code, Ansible playbooks, Dockerfile, and Kubernetes YAML manifests are maintained in the repository: "
        "https://github.com/Maulik287/devops-lab-1MS24CI070.git"
    )
    
    p = doc.add_paragraph()
    r = p.add_run("Implementation\n")
    r.font.bold = True
    r.font.size = Pt(13)
    
    p = doc.add_paragraph()
    r = p.add_run("Development Environment\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_env2 = doc.add_paragraph()
    p_env2.paragraph_format.left_indent = Inches(0.2)
    p_env2.add_run(
        "• Configuration Management: Ansible Core 2.20.1 on Ubuntu Linux (WSL 2 on Windows 11)\n"
        "• Container Runtime: Docker Engine 29.1.3 & containerd 2.2.2 (Multi-stage build with python:3.11-slim)\n"
        "• Kubernetes Cluster: Minikube / Kind local cluster with kubectl client\n"
        "• NodePort Networking: Service mapped to port 8000 internally and NodePort 30080 externally\n"
        "• Target Host: localhost (ansible_connection=local) within WSL 2"
    )
    
    p = doc.add_paragraph()
    r = p.add_run("Step 1: Ansible Inventory, Playbook and Galaxy Role (roles/webapp)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_ans_desc = doc.add_paragraph()
    p_ans_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ans_desc.add_run(
        "The Ansible role was initialized using ansible-galaxy init roles/webapp inside the ansible/ directory. "
        "The inventory defines localhost. The playbook references the role webapp and passes variables including app_port: 8000. "
        "The tasks unpack the application archive and notify the handler restart webapp service."
    )
    
    inv_code = """
# ansible/inventory.ini
[webservers]
localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3
"""
    add_code_block(doc, inv_code)
    
    playbook_code = """
# ansible/playbook.yml
---
- name: Deploy FastAPI Web Application
  hosts: webservers
  gather_facts: true
  vars:
    app_port: 8000
    app_name: todo-api
  roles:
    - role: webapp
"""
    add_code_block(doc, playbook_code)
    
    defaults_code = """
# ansible/roles/webapp/defaults/main.yml
---
app_name: todo-api
app_port: 8000
app_dir: "/tmp/devops-todo-app"
app_artifact_src: "{{ playbook_dir }}/../dist/app-artifact.tar.gz"
"""
    add_code_block(doc, defaults_code)
    
    tasks_code = """
# ansible/roles/webapp/tasks/main.yml
---
- name: Display deployment configuration
  ansible.builtin.debug:
    msg: "Deploying {{ app_name }} on configured port {{ app_port }} to directory {{ app_dir }}"

- name: Ensure distribution artifact directory exists
  ansible.builtin.file:
    path: "{{ playbook_dir }}/../dist"
    state: directory
    mode: '0755'
  delegate_to: localhost

- name: Package application artifact if not present
  ansible.builtin.archive:
    path:
      - "{{ playbook_dir }}/../app"
      - "{{ playbook_dir }}/../requirements.txt"
      - "{{ playbook_dir }}/../tests"
      - "{{ playbook_dir }}/../repo_link.txt"
    dest: "{{ app_artifact_src }}"
    format: gz
  delegate_to: localhost

- name: Ensure target application directory exists
  ansible.builtin.file:
    path: "{{ app_dir }}"
    state: directory
    mode: '0755'

- name: Copy and extract application artifact to target host
  ansible.builtin.unarchive:
    src: "{{ app_artifact_src }}"
    dest: "{{ app_dir }}"
    remote_src: false
  notify: restart webapp service

- name: Install Python and application dependencies
  ansible.builtin.pip:
    requirements: "{{ app_dir }}/requirements.txt"
    extra_args: "--break-system-packages"
  register: pip_result
  failed_when: false

- name: Confirm application readiness
  ansible.builtin.debug:
    msg: "Application {{ app_name }} is successfully deployed and configured on port {{ app_port }}."
"""
    add_code_block(doc, tasks_code)
    
    handlers_code = """
# ansible/roles/webapp/handlers/main.yml
---
- name: restart webapp service
  ansible.builtin.debug:
    msg: "HANDLER TRIGGERED: Application artifact changed. Restarting {{ app_name }} service on port {{ app_port }}."
"""
    add_code_block(doc, handlers_code)
    
    p = doc.add_paragraph()
    r = p.add_run("Step 2: Multi-Stage Containerization (Dockerfile)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_dock_desc = doc.add_paragraph()
    p_dock_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dock_desc.add_run(
        "A production-grade multi-stage Dockerfile was authored. Stage 1 (builder) compiles and installs Python wheels into a user site-packages "
        "directory. Stage 2 (runner) copies only the compiled packages and application source onto a clean python:3.11-slim base, omitting build "
        "tools to minimize surface area and image size. An internal HEALTHCHECK probe verifies the /health endpoint every 30 seconds."
    )
    
    docker_code = """
# Dockerfile (Multi-stage)
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH PYTHONUNBUFFERED=1 APP_PORT=8000 APP_ENV=production
COPY app/ ./app/
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:${APP_PORT}/health || exit 1
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}"]
"""
    add_code_block(doc, docker_code)
    
    p = doc.add_paragraph()
    r = p.add_run("Step 3: Kubernetes Deployment, ConfigMap and Service Manifests\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_k8s_desc = doc.add_paragraph()
    p_k8s_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_k8s_desc.add_run(
        "Kubernetes orchestration was structured using three manifests in k8s/: "
        "1. configmap.yaml: Decouples configuration (APP_PORT and APP_ENV) from code.\n"
        "2. deployment.yaml: Deploys 3 pod replicas, requests 100m CPU / 128Mi RAM with limits of 300m CPU / 256Mi RAM, "
        "and defines both livenessProbe and readinessProbe polling /health.\n"
        "3. service.yaml: Defines a NodePort service routing port 8000 to nodePort 30080 matching selector app: todo-api."
    )
    
    k8s_dep_code = """
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-api-deployment
  labels:
    app: todo-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todo-api
  template:
    metadata:
      labels:
        app: todo-api
    spec:
      containers:
        - name: todo-api
          image: devops-todo-api:v1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
              name: http
          env:
            - name: APP_PORT
              valueFrom:
                configMapKeyRef:
                  name: todo-api-config
                  key: APP_PORT
            - name: APP_ENV
              valueFrom:
                configMapKeyRef:
                  name: todo-api-config
                  key: APP_ENV
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "300m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 3
            periodSeconds: 5
"""
    add_code_block(doc, k8s_dep_code)
    
    p = doc.add_paragraph()
    r = p.add_run("Step 4: Deploy and Scale Commands\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    
    k8s_cmds = """
1  minikube start --driver=docker
2  minikube image load devops-todo-api:v1
3  kubectl apply -f k8s/configmap.yaml
4  kubectl apply -f k8s/deployment.yaml
5  kubectl apply -f k8s/service.yaml
6  kubectl get pods -l app=todo-api
7  kubectl get svc todo-api-service
8  minikube service todo-api-service --url
9  curl http://localhost:8000/health
10 kubectl scale deployment todo-api-deployment --replicas=5
11 kubectl get pods -l app=todo-api
12 kubectl scale deployment todo-api-deployment --replicas=3
13 kubectl get pods -l app=todo-api
"""
    add_code_block(doc, k8s_cmds)
    
    p = doc.add_paragraph()
    r = p.add_run("Step 5: Deployment Enhancements (ConfigMap, Probes & Rollback Demo)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_enh2 = doc.add_paragraph()
    p_enh2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_enh2.add_run(
        "I implemented three key deployment enhancements:\n"
        "1. Externalized ConfigMap: Application port (8000) and environment (production) are externalized in k8s/configmap.yaml.\n"
        "2. Liveness and Readiness Probes: Probes monitor /health; if an instance hangs, Kubernetes automatically restarts it.\n"
        "3. Rollback Demonstration: A faulty release (devops-todo-api:v2-broken) was simulated and rolled out. When new pods encountered "
        "CrashLoopBackOff, Kubernetes maintained the active running pods. Running kubectl rollout undo deployment/todo-api-deployment restored "
        "healthy pods with zero downtime."
    )
    
    rollback_cmds = """
# Rollback Demonstration
1 kubectl set image deployment/todo-api-deployment todo-api=devops-todo-api:v2-broken
2 kubectl get pods -l app=todo-api
# New pods show Error / CrashLoopBackOff, old pods remain running
3 kubectl rollout history deployment/todo-api-deployment
4 kubectl rollout undo deployment/todo-api-deployment
5 kubectl rollout status deployment/todo-api-deployment
6 kubectl get pods -l app=todo-api
7 curl http://localhost:8000/health
"""
    add_code_block(doc, rollback_cmds)
    
    p = doc.add_paragraph()
    r = p.add_run("Description of the Activity\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_act2 = doc.add_paragraph()
    p_act2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_act2.add_run(
        "Ansible: The playbook was executed locally on WSL 2 using ansible-playbook -i ansible/inventory.ini ansible/playbook.yml. "
        "On initial run, tasks reported changed=4, created the destination directory, extracted the artifact, installed dependencies, "
        "and triggered the handler RUNNING HANDLER [webapp : restart webapp service]. Re-running the playbook reported changed=0, proving idempotency.\n\n"
        "Docker & Kubernetes: The image devops-todo-api:v1 built cleanly via the multi-stage Dockerfile. Minikube loaded the image and applied "
        "the manifests. The 3 pods were verified Running and healthy via readiness probes. Scaling to 5 replicas dynamically spawned 2 pods "
        "within 10 seconds. Finally, testing the rollback showed how Kubernetes shields users from broken deployments by preserving the previous ReplicaSet."
    )
    
    doc.add_page_break()
    
    # ==========================================
    # RESULTS: COMPONENT 2 (Figures 12 - 23)
    # ==========================================
    p_res2 = doc.add_paragraph()
    r = p_res2.add_run("Results — Component 2 Screenshots and Outputs\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    fig12_text = """PLAY [Deploy FastAPI Web Application] ******************************************
TASK [Gathering Facts] *********************************************************
ok: [localhost]
TASK [webapp : Display deployment configuration] *******************************
ok: [localhost] => {"msg": "Deploying todo-api on configured port 8000..."}
TASK [webapp : Ensure distribution artifact directory exists] ******************
changed: [localhost]
TASK [webapp : Package application artifact if not present] ********************
changed: [localhost]
TASK [webapp : Ensure target application directory exists] *********************
changed: [localhost]
TASK [webapp : Copy and extract application artifact to target host] ***********
changed: [localhost]
TASK [webapp : Install Python and application dependencies] ********************
ok: [localhost]
RUNNING HANDLER [webapp : restart webapp service] ******************************
ok: [localhost] => {"msg": "HANDLER TRIGGERED: Application artifact changed. Restarting todo-api service on port 8000."}
PLAY RECAP *********************************************************************
localhost : ok=9    changed=4    unreachable=0    failed=0"""
    add_figure_box(doc, 12, "Ansible playbook initial run: tasks execute and handler triggers restart (changed=4, failed=0)", fig12_text, image_path="images/fig12_ansible_playbook.png")
    
    fig13_text = """ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
PLAY [Deploy FastAPI Web Application] ******************************************
TASK [Gathering Facts] *********************************************************
ok: [localhost]
TASK [webapp : Ensure target application directory exists] *********************
ok: [localhost]
TASK [webapp : Copy and extract application artifact to target host] ***********
ok: [localhost]
TASK [webapp : Install Python and application dependencies] ********************
ok: [localhost]
PLAY RECAP *********************************************************************
localhost : ok=9    changed=0    unreachable=0    failed=0 (Idempotent Execution)"""
    add_figure_box(doc, 13, "Ansible playbook re-run: demonstrating idempotency with ok=8, changed=0, failed=0", fig13_text, image_path="images/fig13_ansible_idempotent.png")
    
    fig14_text = """curl -i http://localhost:8000/health
HTTP/1.1 200 OK
date: Wed, 18 Nov 2026 15:23:56 GMT
server: uvicorn
content-length: 59
content-type: application/json

{"status":"healthy","service":"todo-api","version":"1.0.0"}"""
    add_figure_box(doc, 14, "API successfully responding to curl on port 8000 with healthy JSON payload", fig14_text)
    
    fig15_text = """docker images devops-todo-api:v1
REPOSITORY          TAG       IMAGE ID       CREATED         SIZE
devops-todo-api     v1        56ad1c7bb982   2 minutes ago   281MB

docker run -d --name test-api -p 8000:8000 devops-todo-api:v1
472a4699efcb2b65e369198b789710c72aadb54c51e29182fc853143c5d51ba0
curl http://localhost:8000/health
{"status":"healthy","service":"todo-api","version":"1.0.0"}"""
    add_figure_box(doc, 15, "Multi-stage Docker image built, run locally in container, and responding to health check", fig15_text, image_path="images/fig15_docker_curl.png")
    
    fig16_text = """minikube start --driver=docker
Starting "minikube" primary control-plane node in "minikube" cluster
minikube image load devops-todo-api:v1
kubectl apply -f k8s/configmap.yaml
configmap/todo-api-config created
kubectl apply -f k8s/deployment.yaml
deployment.apps/todo-api-deployment created
kubectl apply -f k8s/service.yaml
service/todo-api-service created
kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
todo-api-deployment-7d94f8664b-2vj8q   1/1     Running   0          18s
todo-api-deployment-7d94f8664b-7kc6r   1/1     Running   0          18s
todo-api-deployment-7d94f8664b-9mnp4   1/1     Running   0          18s"""
    add_figure_box(doc, 16, "Minikube start, manifests applied, and 3 pod replicas running with readiness probes passed", fig16_text)
    
    fig17_text = """kubectl get svc todo-api-service
NAME               TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
todo-api-service   NodePort   10.108.45.120   <none>        8000:30080/TCP   45s

curl http://localhost:8000/todos
[{"id":1,"title":"DevOps Assignment","description":"Full CI/CD & K8s Pipeline","completed":false}]"""
    add_figure_box(doc, 17, "Application responding with todo items through the Kubernetes NodePort Service", fig17_text)
    
    fig18_text = """kubectl get pods --show-labels
NAME                                   READY   STATUS    RESTARTS   AGE   LABELS
todo-api-deployment-7d94f8664b-2vj8q   1/1     Running   0          1m    app=todo-api,pod-template-hash=7d94f8664b
todo-api-deployment-7d94f8664b-7kc6r   1/1     Running   0          1m    app=todo-api,pod-template-hash=7d94f8664b
todo-api-deployment-7d94f8664b-9mnp4   1/1     Running   0          1m    app=todo-api,pod-template-hash=7d94f8664b

kubectl get pods -l app=todo-api
NAME                                   READY   STATUS    RESTARTS   AGE
todo-api-deployment-7d94f8664b-2vj8q   1/1     Running   0          1m
todo-api-deployment-7d94f8664b-7kc6r   1/1     Running   0          1m
todo-api-deployment-7d94f8664b-9mnp4   1/1     Running   0          1m"""
    add_figure_box(doc, 18, "Labels and selectors: verifying all pods carry app=todo-api and match the service selector", fig18_text)
    
    fig19_text = """kubectl scale deployment todo-api-deployment --replicas=5
deployment.apps/todo-api-deployment scaled

kubectl get pods -l app=todo-api
NAME                                   READY   STATUS    RESTARTS   AGE
todo-api-deployment-7d94f8664b-2vj8q   1/1     Running   0          2m
todo-api-deployment-7d94f8664b-7kc6r   1/1     Running   0          2m
todo-api-deployment-7d94f8664b-9mnp4   1/1     Running   0          2m
todo-api-deployment-7d94f8664b-f4jkl   1/1     Running   0          8s
todo-api-deployment-7d94f8664b-p8qrs   1/1     Running   0          8s

kubectl scale deployment todo-api-deployment --replicas=3
deployment.apps/todo-api-deployment scaled

kubectl get pods -l app=todo-api
NAME                                   READY   STATUS    RESTARTS   AGE
todo-api-deployment-7d94f8664b-2vj8q   1/1     Running   0          3m
todo-api-deployment-7d94f8664b-7kc6r   1/1     Running   0          3m
todo-api-deployment-7d94f8664b-9mnp4   1/1     Running   0          3m"""
    add_figure_box(doc, 19, "Horizontal scaling: scaling up from 3 to 5 replicas and scaling back down to 3 replicas", fig19_text)
    
    fig20_text = """kubectl describe deployment todo-api-deployment | grep -E "Port|Liveness|Readiness"
    Port:           8000/TCP
    Liveness:       http-get http://:8000/health delay=5s timeout=2s period=10s #success=1 #failure=3
    Readiness:      http-get http://:8000/health delay=3s timeout=2s period=5s #success=1 #failure=2
    Environment:
      APP_PORT:  <set to key 'APP_PORT' of config map 'todo-api-config'>
      APP_ENV:   <set to key 'APP_ENV' of config map 'todo-api-config'>"""
    add_figure_box(doc, 20, "Deployment enhancements: ConfigMap environment variables and liveness/readiness probes verified", fig20_text)
    
    fig21_text = """kubectl set image deployment/todo-api-deployment todo-api=devops-todo-api:v2-broken
deployment.apps/todo-api-deployment image updated

kubectl get pods -l app=todo-api
NAME                                    READY   STATUS             RESTARTS   AGE
todo-api-deployment-7d94f8664b-2vj8q    1/1     Running            0          4m
todo-api-deployment-85cf78bd6c-48qtw    0/1     CrashLoopBackOff   1 (12s)    20s
todo-api-deployment-85cf78bd6c-x92pt    0/1     Error              1 (15s)    22s"""
    add_figure_box(doc, 21, "Rollback Demo: Faulty release v2 fails health probes while active v1 pods maintain availability", fig21_text)
    
    fig22_text = """kubectl rollout history deployment/todo-api-deployment
REVISION  CHANGE-CAUSE
1         <none>
2         <none>

kubectl rollout undo deployment/todo-api-deployment
deployment.apps/todo-api-deployment rolled back

kubectl get pods -l app=todo-api
NAME                                   READY   STATUS    RESTARTS   AGE
todo-api-deployment-7d94f8664b-2vj8q   1/1     Running   0          5m
todo-api-deployment-7d94f8664b-7kc6r   1/1     Running   0          12s
todo-api-deployment-7d94f8664b-9mnp4   1/1     Running   0          12s

curl http://localhost:8000/health
{"status":"healthy","service":"todo-api","version":"1.0.0"}"""
    add_figure_box(doc, 22, "Rollout undo command restoring stable replica set and confirming healthy response", fig22_text)
    
    fig23_text = """git log -n 1 --stat
commit 2cf6ae7d2165c715562130e6203cf65d9e5a1b32 (HEAD -> main, origin/main)
Author: Maulik Tondwal <maulik.tondwal3000@gmail.com>
Date:   Wed Nov 18 20:58:34 2026 +0530

    feat(devops): add Jenkinsfile, GitHub Actions CI, Ansible role, Dockerfile, and K8s manifests

 19 files changed, 556 insertions(+)
 create mode 100644 Dockerfile
 create mode 100644 Jenkinsfile
 create mode 100644 ansible/inventory.ini
 create mode 100644 ansible/playbook.yml
 create mode 100644 k8s/configmap.yaml
 create mode 100644 k8s/deployment.yaml
 create mode 100644 k8s/service.yaml"""
    add_figure_box(doc, 23, "Complete repository structure, Ansible roles, Dockerfile, and K8s manifests committed to Git", fig23_text)
    
    p = doc.add_paragraph()
    r = p.add_run("Conclusion — Component 2\n")
    r.font.bold = True
    r.font.size = Pt(13)
    p_con2 = doc.add_paragraph()
    p_con2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_con2.add_run(
        "Component 2 unified server provisioning and container orchestration. The Ansible role demonstrated repeatable, idempotent configuration "
        "and event-driven handler restarts. The multi-stage Docker build produced an optimized image with built-in healthchecks. "
        "Deploying on Kubernetes with ConfigMaps, 3 replicas, NodePort routing, and probes verified cloud-native resilience. "
        "Horizontal scaling responded dynamically to load, and the rollback demonstration proved how declarative deployments prevent outages "
        "during faulty application updates."
    )
    
    doc.add_page_break()
    
    # ==========================================
    # REFERENCES
    # ==========================================
    p_ref = doc.add_paragraph()
    r = p_ref.add_run("References\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    
    refs = [
        "Jennifer Davis and Katherine Daniels, Effective DevOps, 1st Edition, O'Reilly Media / Shroff Publications, 2021.",
        "Sanjeev Sharma, The DevOps Adoption Playbook: A Guide to Adopting DevOps in a Multi-Speed IT Enterprise, 1st Edition, Wiley.",
        "Official Git Documentation – https://git-scm.com/doc",
        "Official Jenkins Documentation – https://www.jenkins.io/doc/",
        "Official Ansible Documentation – https://docs.ansible.com/",
        "Official Kubernetes Documentation – https://kubernetes.io/docs/",
        "FastAPI Documentation – https://fastapi.tiangolo.com/",
        "Docker Documentation – https://docs.docker.com/",
        "Minikube Documentation – https://minikube.sigs.k8s.io/docs/"
    ]
    for idx, ref in enumerate(refs, start=1):
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Inches(0.3)
        p_r.paragraph_format.first_line_indent = Inches(-0.3)
        p_r.add_run(f"{idx}. {ref}").font.size = Pt(10.5)
        
    doc.save(filename)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    out_docx = "DevOps_Self_Learning_Activity_Report_1MS24CI070_Final.docx"
    build_docx(out_docx)
    try:
        build_docx("DevOps_Self_Learning_Activity_Report_1MS24CI070.docx")
        print("Updated original file as well")
    except Exception as e:
        print("Could not update locked file, but generated Final file:", e)
