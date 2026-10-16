"""
Complete Generator Script for Jankalyan Blood Bank Digital Form System (QF/JKRP/18)
Creates 'Jankalyan_Technical_Documentation.docx' with professional styling,
concise and summarized sections, clear tables, and visual callouts.
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E0", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout(doc, text, title="NOTE / COMPLIANCE MANDATE", alert_type="info"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    
    if alert_type == "danger":
        fill_hex = "FFF5F5"
        border_hex = "E53E3E"
        title_color = RGBColor(197, 48, 48)
    elif alert_type == "warning":
        fill_hex = "FFFAF0"
        border_hex = "DD6B20"
        title_color = RGBColor(221, 107, 32)
    elif alert_type == "success":
        fill_hex = "F0FFF4"
        border_hex = "38A169"
        title_color = RGBColor(56, 161, 105)
    else: # info
        fill_hex = "EBF8FF"
        border_hex = "3182CE"
        title_color = RGBColor(49, 130, 206)
        
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:top w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_title = p.add_run(f"[{title}]\n")
    run_title.bold = True
    run_title.font.size = Pt(9.5)
    run_title.font.color.rgb = title_color
    
    run_text = p.add_run(text)
    run_text.font.size = Pt(9)
    run_text.font.color.rgb = RGBColor(45, 55, 72)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_row(row, widths, is_header=False, bg_color="1A365D"):
    for idx, cell in enumerate(row.cells):
        cell.width = widths[idx]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if is_header:
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    run.font.bold = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(255, 255, 255)
        else:
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                for run in p.runs:
                    run.font.size = Pt(8.5)
                    run.font.color.rgb = RGBColor(45, 55, 72)

def build_styled_table(doc, headers, data, col_widths, col_alignments=None, zebra=True):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="CBD5E0", sz="4")
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        p = hdr_cells[i].paragraphs[0]
        if col_alignments and i < len(col_alignments):
            p.alignment = col_alignments[i]
    format_row(table.rows[0], col_widths, is_header=True, bg_color="1A365D")
    
    # Repeat header across pages
    trPr = table.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    # Data rows
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            row.cells[c_idx].text = str(val)
            p = row.cells[c_idx].paragraphs[0]
            if col_alignments and c_idx < len(col_alignments):
                p.alignment = col_alignments[c_idx]
        
        bg = "F7FAFC" if (zebra and r_idx % 2 == 1) else "FFFFFF"
        format_row(row, col_widths, is_header=False)
        for cell in row.cells:
            set_cell_background(cell, bg)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return table

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(26, 54, 93) # Navy
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(43, 108, 176) # Slate Blue
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(45, 55, 72)
    return p

def add_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(26, 54, 93)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(45, 55, 72)
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(26, 54, 93)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(45, 55, 72)
    return p

def generate_technical_documentation():
    print("[*] Generating Technical Documentation Word document...")
    doc = Document()

    # Configure 1-inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    # ----------------------------------------------------
    # COVER / HEADER SECTION
    # ----------------------------------------------------
    p_org = doc.add_paragraph()
    p_org.paragraph_format.space_before = Pt(12)
    p_org.paragraph_format.space_after = Pt(2)
    r_org = p_org.add_run("JANKALYAN BLOOD CENTRE & HOSPITAL | JANKALYAN TRUST")
    r_org.font.name = "Arial"
    r_org.font.size = Pt(10)
    r_org.font.bold = True
    r_org.font.color.rgb = RGBColor(197, 48, 48) # Medical Red Accent

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("Technical Documentation & System Specifications")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(26, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Digital Blood Donor Registration, Medical Screening, Consent & Verification System (Form QF/JKRP/18)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(74, 85, 104)

    # Metadata Table
    meta_headers = ["Attribute", "Specification / Value"]
    meta_data = [
        ["System Reference", "Jankalyan Blood Bank Digital Form System (QF/JKRP/18)"],
        ["Clinical Form Digitised", "QF/JKRP/18 (Standard 4-Page Blood Donation Card)"],
        ["System Languages", "Bilingual: English & Marathi (मराठी) with Instant Real-Time Toggle"],
        ["Deployment Models", "1) Standalone Windows Desktop App (.exe) | 2) Hospital Private LAN Web Server"],
        ["Data Sovereignty", "100% On-Premise Private Hosting (Zero Cloud Dependency / Zero Telemetry)"],
        ["Compliance Alignment", "DISHA / ISO 27001 / CDSCO & Drugs and Cosmetics Blood Bank Rules"],
        ["Timezone Standard", "Indian Standard Time (IST - Asia/Kolkata, UTC+05:30)"],
        ["Document Version", "v1.0.0 (Summarized Comprehensive Technical Edition)"]
    ]
    build_styled_table(doc, meta_headers, meta_data, [Inches(2.2), Inches(4.5)])

    add_callout(
        doc,
        "This document provides the complete, summarized technical and architectural specification for the Jankalyan "
        "Blood Bank Digital System. It serves as an authoritative guide for software engineers, clinical administrators, "
        "and IT infrastructure managers.",
        title="DOCUMENT PURPOSE & SCOPE",
        alert_type="info"
    )

    # ----------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & SYSTEM OVERVIEW
    # ----------------------------------------------------
    add_h1(doc, "1. Executive Summary & System Overview")
    
    add_p(doc, 
          "The Jankalyan Blood Bank Digital Form System replaces the legacy 4-page paper blood donor card (Form QF/JKRP/18) "
          "with a secure, highly responsive, tablet-friendly digital workflow. Blood donation involves strictly regulated, "
          "high-risk medical assessments where donor suitability, medical history, vital signs, and informed consent must be recorded "
          "with 100% clinical fidelity.",
          bold_prefix="Clinical Context: ")

    add_p(doc, "The digital platform addresses the critical vulnerabilities of paper-based workflows:", bold_prefix="Key Objectives: ")
    add_bullet(doc, "Eliminates illegible handwriting, incomplete forms, and manual paper storage risks.", bold_prefix="Data Integrity: ")
    add_bullet(doc, "Mandatory vitals ranges (Weight >= 45kg, Hb >= 12.5 g/dL, normal BP) prevent accidental collection from unfit donors.", bold_prefix="Clinical Safety: ")
    add_bullet(doc, "Donors can read, comprehend, and answer questionnaire items in English or Marathi seamlessly.", bold_prefix="Bilingual Inclusivity: ")
    add_bullet(doc, "Finger touch and stylus digital signature capture on HTML5 canvas with base64 PNG serialization.", bold_prefix="Legal & Consent Signatures: ")
    add_bullet(doc, "Once verified by the Medical Officer, records are immutably locked. Audited unlock procedure prevents tampering.", bold_prefix="Tamper Resistance: ")
    add_bullet(doc, "Built for hospital LANs or standalone desktop PCs with no 3rd-party cloud dependencies.", bold_prefix="Data Sovereignty: ")

    # ----------------------------------------------------
    # SECTION 2: TECHNOLOGY STACK & ARCHITECTURE
    # ----------------------------------------------------
    add_h1(doc, "2. Technology Stack & Architecture")

    add_p(doc, "The system employs a lean, zero-bloat architecture prioritizing high reliability, near-zero maintenance, and instant startup.")

    tech_headers = ["Layer / Domain", "Technology", "Version", "Role & Justification"]
    tech_data = [
        ["Backend Core", "Python", "3.10+", "Robust, high-security server environment."],
        ["Web Framework", "Flask", ">= 3.0.0", "Micro-framework providing minimal attack surface and fast REST routing."],
        ["WSGI Server", "Waitress", ">= 3.0.0", "Production-grade, multi-threaded pure Python WSGI server for Windows/Linux."],
        ["Database Engine", "SQLite 3", "3.x (WAL)", "Zero-configuration embedded SQL with foreign keys and ACID transactions."],
        ["Data Export", "openpyxl", ">= 3.1.0", "Generates styled Excel (.xlsx) workbooks with auto-sized columns."],
        ["Security / Auth", "Werkzeug", ">= 3.0.0", "Salted PBKDF2/scrypt password hashing and session cookie protection."],
        ["Frontend UI", "Vanilla HTML5 / CSS3", "Modern Web", "No React/Next/Webpack bloat; loads in <15ms with full tablet touch support."],
        ["Scripting / Logic", "Vanilla ES6+ JS", "ES2022+", "Handles client validations, bilingual I18N state, and dynamic rendering."],
        ["Signature Pad", "HTML5 Canvas API", "Pointer Events", "Captures stylus, pen, and touch signatures with high resolution."],
        ["Printing Engine", "@media print CSS", "CSS3 Paged Media", "Pixel-perfect A4 form output reproducing physical QF/JKRP/18 card."],
        ["Desktop Packaging", "PyInstaller", ">= 6.0.0", "Packages runtime, assets, and WSGI into a standalone Windows folder/exe."],
        ["Windows Installer", "Inno Setup", "6.x", "Builds standard Windows setup executable (`.exe`) with desktop & start menu icons."],
        ["Timezone Engine", "zoneinfo / datetime", "Built-in", "Strict Indian Standard Time (IST Asia/Kolkata, UTC+05:30) enforcement."]
    ]
    build_styled_table(doc, tech_headers, tech_data, [Inches(1.5), Inches(1.3), Inches(1.0), Inches(2.7)])

    add_h2(doc, "2.1 Storage & %APPDATA% Persistence Architecture")
    add_p(doc, 
          "A major pitfall of standard desktop packaging is SQLite data loss caused by temporary file extraction (`sys._MEIPASS`) "
          "or Windows write-permission denials in `C:\\Program Files`. To solve this permanently, the system includes a dynamic path resolver "
          "(`services/path_service.py`):")
    add_bullet(doc, "Application binary and read-only static files reside in Program Files or PyInstaller bundle.", bold_prefix="Read-Only Layer: ")
    add_bullet(doc, "Active SQLite database (`bloodbank.db`) and backups are placed in `%APPDATA%\\JankalyanBloodBank\\data\\`.", bold_prefix="Writable Data Layer: ")
    add_bullet(doc, "First startup automatically executes `database/schema.sql` and seeds default credentials if DB is absent.", bold_prefix="Automatic Bootstrap: ")
    add_bullet(doc, "Updating or uninstalling the software never touches or deletes donor records or audit logs in %APPDATA%.", bold_prefix="Preservation Guarantee: ")

    add_h2(doc, "2.2 Dual-Mode Deployment Architecture")
    add_bullet(doc, "Runs `desktop_launcher.py`, spins up Waitress WSGI on `127.0.0.1:8000`, and opens the default browser.", bold_prefix="Mode A - Standalone Desktop: ")
    add_bullet(doc, "Server runs on dedicated hospital PC (`0.0.0.0:8000`), accessed by nurse/doctor tablets and PCs over LAN/Wi-Fi.", bold_prefix="Mode B - Private LAN Server: ")

    # ----------------------------------------------------
    # SECTION 3: FUNCTIONAL REQUIREMENTS SPECIFICATION (FRS)
    # ----------------------------------------------------
    add_h1(doc, "3. Functional Requirements Specification (FRS)")

    add_p(doc, "The system models the complete donor lifecycle through an interactive 6-step digital workflow matching Form QF/JKRP/18:")

    frs_headers = ["Module / Step", "Functional Scope", "Key Business Rules & Validations"]
    frs_data = [
        [
            "1. Authentication & RBAC",
            "Role-based login, session timeout (12 hours), soft-deletion, password management.",
            "Roles: ADMIN, STAFF, MEDICAL_OFFICER. Deactivated accounts blocked. Root 'admin' cannot be deleted."
        ],
        [
            "2. Donor Demographics (Step 1)",
            "Captures Auto-ID (`BB-YYYY-000001`), Donor ID, Name, Gender, DOB, Age, Address, Phone, Donation Type.",
            "Validates mandatory mobile number (10 digits), age (18-65), address, and voluntary/replacement donation type."
        ],
        [
            "3. Health Questionnaire (Step 2)",
            "Screening questions 1 to 10: sleep adequacy, 4-hour meal, heavy work, weakness, alcohol, daily meds.",
            "Bilingual Q&A. Night-shift sleep check (Q3B) and recent acute infections trigger warning/deferrals."
        ],
        [
            "4. Deferrals & History (Step 3)",
            "10 timeframe medication history, 15 permanent deferrals checklist, endoscopy, past donation issues.",
            "Timeframes from 3 days (aspirin) to 2 years (TB). Permanent deferral grid immediately marks record for doctor review."
        ],
        [
            "5. High-Risk & Females (Step 4)",
            "Unsafe sexual history, injectable narcotics, HIV/Hep risk, female screening (pregnancy, lactation, periods).",
            "Next 24-hr high-risk occupation checks (pilots, long-haul drivers, crane operators, deep-sea divers)."
        ],
        [
            "6. Medical Exam (Step 5)",
            "Vitals measurement: Weight, BP systolic/diastolic, Pulse, Hemoglobin, Temperature, Phlebotomy site.",
            "Auto-validation: Weight >= 45 kg, Hb >= 12.5 g/dL, normal BP. Staff selects outcome: Eligible, Deferred, Rejected."
        ],
        [
            "7. Blood Bag Details (Step 5)",
            "Barcode/Bag number, bag type (Single, Double, Triple, Quadruple), anticoagulant, volume (350/450 ml).",
            "Phlebotomist staff ID logging and donor adverse reaction monitoring (fainting, hematoma, dizziness)."
        ],
        [
            "8. Consent & Signature (Step 6)",
            "Informed consent clauses, notification of abnormal test results consent, touch/stylus signature pad.",
            "HTML5 canvas captures signature as high-res base64 PNG. Clear and redo controls provided."
        ],
        [
            "9. Doctor Verification",
            "Medical officer reviews screening vitals, enters clinical notes, and electronically signs off.",
            "Upon signature, status transitions to `SIGNED` and all form fields are permanently locked from editing."
        ],
        [
            "10. Audited Unlock Workflow",
            "Authorized override for correcting locked records by Administrator or Medical Officer.",
            "Requires mandatory reason text. Resets status to `DRAFT` and generates security audit log entry."
        ],
        [
            "11. Bilingual Translation",
            "Real-time instant toggle between English and Marathi across all UI elements and form labels.",
            "No page refresh required. Translated data retained consistently across both languages."
        ],
        [
            "12. A4 Print & PDF Output",
            "Generates exact physical replica of Form QF/JKRP/18 ready for single or double-sided A4 printing.",
            "CSS `@media print` eliminates UI buttons, headers, and footers, rendering high-contrast clinical form."
        ],
        [
            "13. Search & Excel Export",
            "Multi-filter query (date range, record no, blood group, status) and styled `.xlsx` workbook generation.",
            "OpenPyXL creates navy-styled headers, bordered data cells, and Indian date formats."
        ],
        [
            "14. Audit & Disaster Recovery",
            "Immutable audit log table tracking every system event; one-click SQLite `.db` backup and live restore.",
            "Captures user ID, username, action, IP address, and IST timestamp for compliance audits."
        ]
    ]
    build_styled_table(doc, frs_headers, frs_data, [Inches(1.8), Inches(2.5), Inches(2.4)])

    add_h2(doc, "3.1 Donor Record Lifecycle State Machine")
    add_bullet(doc, "Form initialized by staff; demographics, questionnaire, vitals, or bag details partially filled.", bold_prefix="1. DRAFT: ")
    add_bullet(doc, "Staff completes preliminary screening, captures donor consent & signature, and forwards for verification.", bold_prefix="2. SUBMITTED: ")
    add_bullet(doc, "Awaiting Medical Officer examination, vitals verification, and clinical approval.", bold_prefix="3. MEDICAL_VERIFICATION: ")
    add_bullet(doc, "Medical Officer signs electronically. Record becomes IMMUTABLE and LOCKED.", bold_prefix="4. SIGNED: ")
    add_bullet(doc, "Blood bag collected, processed, and released to testing / component separation laboratory.", bold_prefix="5. COMPLETED: ")
    add_bullet(doc, "Donor deferred, medical rejection, or donor withdrew consent.", bold_prefix="6. CANCELLED / DEFERRED: ")

    # ----------------------------------------------------
    # SECTION 4: NON-FUNCTIONAL REQUIREMENTS (NFRS)
    # ----------------------------------------------------
    add_h1(doc, "4. Non-Functional Requirements Specification (NFRS)")

    nfr_headers = ["Category", "Requirement Target", "Implementation & Architecture Mechanism"]
    nfr_data = [
        [
            "Performance",
            "Sub-100ms API response; instant page rendering.",
            "Vanilla HTML/JS with no heavy client bundles; SQLite WAL mode indexing; in-memory caching."
        ],
        [
            "Data Sovereignty",
            "100% On-Premise; Zero cloud transmission.",
            "Self-contained database (`bloodbank.db`) and WSGI server running locally inside hospital intranet."
        ],
        [
            "Compliance",
            "DISHA, ISO 27001, NABH, and CDSCO standards.",
            "Consent documentation, electronic signature tracking, immutable audit trails, and strict RBAC."
        ],
        [
            "Security",
            "Zero unauthorized data tampering or leaks.",
            "Werkzeug salted password hashing; parameterized SQL (zero SQLi); HTTPOnly 12-hr session cookies."
        ],
        [
            "Reliability",
            "99.9% uptime on hospital LAN; zero data loss.",
            "SQLite ACID transactions; persistent `%APPDATA%` path resolver; one-click hot backup/restore."
        ],
        [
            "Usability",
            "Intuitive for clinical staff and donors on tablets.",
            "Bilingual English/Marathi toggle; large touch buttons; responsive HTML5 canvas stylus pad."
        ],
        [
            "Portability",
            "Runs on Windows 10/11, Windows Server, or Linux.",
            "Cross-platform Python runtime; PyInstaller standalone executable; Inno Setup Windows installer."
        ]
    ]
    build_styled_table(doc, nfr_headers, nfr_data, [Inches(1.5), Inches(2.2), Inches(3.0)])

    # ----------------------------------------------------
    # SECTION 5: DATABASE SCHEMA & DATA DICTIONARY
    # ----------------------------------------------------
    add_h1(doc, "5. Database Architecture & Data Dictionary")
    add_p(doc, 
          "The database runs on embedded SQLite 3 with WAL (Write-Ahead Logging) and CASCADE Foreign Key enforcement. "
          "It consists of 12 normalized relational tables centered around the `blood_donation_records` master entity:")

    tables_summary = [
        ["users", "System credentials, roles (ADMIN/STAFF/MEDICAL_OFFICER), doctor registration numbers, profile signature."],
        ["blood_donation_records", "Master record header: record number (`BB-YYYY-000001`), donor number, donation date, lifecycle status."],
        ["donor_details", "Personal demographics: full name, gender, DOB, age, occupation, address, city, pincode, mobile, blood group."],
        ["medical_examinations", "Vitals screening: weight, height, pulse, BP systolic/diastolic, Hb, temperature, venepuncture inspection, outcome."],
        ["medication_history", "JSON structure containing donor responses to 10 distinct medication and disease timeframe deferrals."],
        ["permanent_deferrals", "JSON array of selected high-risk permanent deferral medical conditions (heart disease, cancer, epilepsy, etc.)."],
        ["questionnaire_answers", "JSON object capturing responses to Questions 1 through 17 (endoscopy, past complications, symptoms, female Qs)."],
        ["donor_consent", "Informed consent flag, abnormal test notification agreement, base64 donor signature, and IST timestamp."],
        ["donation_details", "Phlebotomy data: blood bag barcode, bag type (single/double/triple/quadruple), volume (mL), adverse reactions."],
        ["signatures", "Medical Officer approval record: doctor user ID, name, registration no, base64 signature, notes, IST timestamp."],
        ["system_settings", "Global configuration key-value pairs (record prefix `BB`, sequence counter, hospital naming)."],
        ["audit_logs", "Security audit trail: user ID, username, record number, action type, IP address, and IST timestamp."]
    ]
    build_styled_table(doc, ["Table Name", "Table Purpose & Clinical Scope"], tables_summary, [Inches(2.2), Inches(4.5)])

    add_h2(doc, "5.1 Key Master Table Schema (`blood_donation_records`)")
    bdr_headers = ["Column", "Data Type", "Constraints", "Description"]
    bdr_data = [
        ["id", "INTEGER", "PK AUTOINCREMENT", "Internal primary surrogate key."],
        ["record_number", "TEXT", "UNIQUE, NOT NULL", "Standard formatted record number (e.g. `BB-2026-000001`)."],
        ["donor_number", "TEXT", "Optional", "Hospital master donor identification number."],
        ["donation_date", "DATE", "NOT NULL", "Date of donation (stored in YYYY-MM-DD format)."],
        ["status", "TEXT", "CHECK Constraint", "DRAFT, SUBMITTED, MEDICAL_VERIFICATION, SIGNED, COMPLETED, CANCELLED."],
        ["created_by", "INTEGER", "FK -> users(id)", "Staff user ID who initiated the record."],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Record creation timestamp in Indian Standard Time."],
        ["updated_by", "INTEGER", "FK -> users(id)", "User ID who last modified the record."],
        ["updated_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Last update timestamp in Indian Standard Time."]
    ]
    build_styled_table(doc, bdr_headers, bdr_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.2)])

    add_h2(doc, "5.2 Medical Examinations Schema (`medical_examinations`)")
    med_headers = ["Column", "Data Type", "Constraints", "Clinical Purpose & Validation Rule"]
    med_data = [
        ["id", "INTEGER", "PK AUTOINCREMENT", "Surrogate identifier."],
        ["record_id", "INTEGER", "FK (UNIQUE)", "Direct 1-to-1 link to `blood_donation_records(id)`."],
        ["weight_kg", "REAL", "NOT NULL", "Donor body weight. Minimum acceptable clinical threshold: 45.0 kg."],
        ["height_cm", "REAL", "Optional", "Donor height in centimeters."],
        ["pulse_rate", "INTEGER", "NOT NULL", "Resting heart rate in beats per minute (acceptable: 60 - 100 bpm)."],
        ["bp_systolic", "INTEGER", "NOT NULL", "Systolic Blood Pressure (mmHg). Standard threshold: 100 - 140 mmHg."],
        ["bp_diastolic", "INTEGER", "NOT NULL", "Diastolic Blood Pressure (mmHg). Standard threshold: 60 - 90 mmHg."],
        ["hemoglobin_g_dl", "REAL", "NOT NULL", "Hemoglobin in g/dL. Minimum regulatory safety threshold: 12.5 g/dL."],
        ["body_temperature", "REAL", "NOT NULL", "Body temperature (°F). Standard acceptable limit: <= 99.5 °F (afebrile)."],
        ["skin_site_inspection", "TEXT", "NOT NULL", "Venepuncture site check: Satisfactory or Unsatisfactory."],
        ["screening_outcome", "TEXT", "CHECK Constraint", "Pre-donation outcome: ELIGIBLE, DEFERRED, or REJECTED."],
        ["deferral_reason", "TEXT", "Optional", "Clinical justification for temporary or permanent deferral."],
        ["deferral_duration", "TEXT", "Optional", "Duration of temporary deferral (e.g., '14 Days', '3 Months')."],
        ["examined_by_staff_id", "INTEGER", "FK -> users(id)", "Staff or Medical Officer who performed physical examination."]
    ]
    build_styled_table(doc, med_headers, med_data, [Inches(1.8), Inches(1.1), Inches(1.4), Inches(2.4)])

    # ----------------------------------------------------
    # SECTION 6: REST API SPECIFICATIONS
    # ----------------------------------------------------
    add_h1(doc, "6. REST API Reference & Interface Contracts")
    add_p(doc, "The Flask application exposes clean, RESTful JSON endpoints guarded by role-based authentication decorators:")

    api_headers = ["Method & Endpoint", "Allowed Roles", "Request Payload / Params", "Description & Response Status"]
    api_data = [
        ["POST /api/auth/login", "Anonymous", "{username, password}", "Authenticates user; sets 12-hr session cookie. [200, 401]"],
        ["POST /api/auth/logout", "All Authenticated", "None", "Clears session; records logout audit log. [200]"],
        ["GET /api/auth/me", "All Authenticated", "None", "Returns currently logged-in user profile & role. [200]"],
        ["GET /api/profile", "All Authenticated", "None", "Retrieves active user profile & stored signature. [200]"],
        ["POST /api/profile/signature", "All Authenticated", "{signature_data}", "Saves user profile digital signature canvas string. [200, 400]"],
        ["GET /api/users", "ADMIN", "None", "Lists all active/inactive system user accounts. [200, 403]"],
        ["POST /api/users", "ADMIN", "{username, password, full_name, role, reg_no}", "Creates new user account with hashed credentials. [200, 400]"],
        ["PUT /api/users/<id>", "ADMIN", "{username, full_name, role, password?}", "Updates user profile, role, or resets password. [200, 400, 404]"],
        ["DELETE /api/users/<id>", "ADMIN", "None", "Soft-deletes user account (prevents primary admin deletion). [200, 400]"],
        ["POST /api/users/<id>/reactivate", "ADMIN", "None", "Reactivates a previously soft-deleted account. [200, 404]"],
        ["GET /api/records", "All Authenticated", "?search=&status=&blood_group=&from_date=", "Searches & filters donor records with IST dates. [200]"],
        ["GET /api/records/<id>", "All Authenticated", "None", "Fetches complete record bundle across all 8 sub-tables. [200, 404]"],
        ["POST /api/records", "STAFF, ADMIN", "{record_id?, save_as_draft, donor, exam, ...}", "Creates or updates donor record across all sub-tables. [200, 400, 403]"],
        ["POST /api/records/<id>/submit", "STAFF, ADMIN", "None", "Submits draft record for Medical Verification. [200, 404]"],
        ["POST /api/records/<id>/sign", "MEDICAL_OFFICER, ADMIN", "{signature_data, medical_notes}", "Attaches doctor signature and immutably locks record. [200, 400]"],
        ["POST /api/records/<id>/unlock", "ADMIN, MEDICAL_OFFICER", "{reason}", "Unlocks signed record for authorized modifications. [200, 400]"],
        ["GET /print/<id>", "All Authenticated", "None", "Renders pixel-perfect A4 printable Form QF/JKRP/18. [200, 404]"],
        ["GET /api/export/excel", "All Authenticated", "?search=&status=&blood_group=", "Downloads formatted Excel (.xlsx) report with IST dates. [200]"],
        ["GET /api/backup/download", "ADMIN", "None", "Downloads live `bloodbank.db` SQLite hot backup. [200, 403]"],
        ["POST /api/backup/restore", "ADMIN", "multipart/form-data: backup_file (.db)", "Hot-restores database from uploaded `.db` backup file. [200, 400]"],
        ["GET /api/audit-logs", "ADMIN", "None", "Returns recent 200 security audit log entries. [200, 403]"]
    ]
    build_styled_table(doc, api_headers, api_data, [Inches(1.8), Inches(1.4), Inches(1.6), Inches(1.9)])

    # ----------------------------------------------------
    # SECTION 7: SECURITY & RBAC PERMISSION MATRIX
    # ----------------------------------------------------
    add_h1(doc, "7. System Security & Role-Based Access Control (RBAC)")

    add_p(doc, "The system implements granular role-based permissions enforced at both the UI layer and API middleware decorators:")

    rbac_headers = ["System Capability / Action", "ADMIN", "STAFF", "MEDICAL_OFFICER"]
    rbac_data = [
        ["Create & Draft Donor Records", "YES", "YES", "NO"],
        ["Edit Draft / Submitted Records", "YES", "YES", "NO"],
        ["Submit Form for Verification", "YES", "YES", "NO"],
        ["Review Medical Screening & Vitals", "YES", "YES (View Only)", "YES"],
        ["Sign Off & Finalize Record", "YES", "NO", "YES"],
        ["Unlock Finalized (Locked) Record", "YES", "NO", "YES (Audited)"],
        ["View All Records & Dashboard", "YES", "YES", "YES"],
        ["Print Form QF/JKRP/18", "YES", "YES", "YES"],
        ["Export Records to Excel (.xlsx)", "YES", "YES", "YES"],
        ["Manage System Users (Create/Edit)", "YES", "NO", "NO"],
        ["Soft-Delete & Reactivate Users", "YES", "NO", "NO"],
        ["View System Security Audit Trail", "YES", "NO", "NO"],
        ["Download & Restore Database Backup", "YES", "NO", "NO"]
    ]
    build_styled_table(doc, rbac_headers, rbac_data, [Inches(3.2), Inches(1.1), Inches(1.1), Inches(1.3)])

    add_callout(
        doc,
        "Record Locking Security Guarantee: Once a Medical Officer submits their electronic signature, the record status "
        "is set to 'SIGNED' and all editing permissions are revoked for standard users. Any subsequent changes require an "
        "audited administrative unlock with recorded clinical justification.",
        title="RECORD IMMUTABILITY MANDATE",
        alert_type="warning"
    )

    # ----------------------------------------------------
    # SECTION 8: HARDWARE, NETWORK & SERVER SPECIFICATIONS
    # ----------------------------------------------------
    add_h1(doc, "8. Hardware, Network & Server Specifications")

    add_p(doc, "For on-premise private hospital deployment, the following hardware and network topology is recommended:")

    hw_headers = ["Component", "Minimum Requirement", "Recommended Specification"]
    hw_data = [
        ["Processor (CPU)", "Intel Core i3 (9th Gen) / AMD Ryzen 3", "Intel Core i5 (11th Gen+) / AMD Ryzen 5"],
        ["System Memory (RAM)", "8 GB DDR4", "16 GB DDR4 / DDR5"],
        ["Storage (Disk)", "128 GB SATA SSD", "256 GB NVMe M.2 SSD (High I/O speed)"],
        ["Network Interface", "1 Gbps Ethernet LAN Port", "1 Gbps Dual-Port Ethernet / Gigabit Switch"],
        ["Operating System", "Windows 10 / 11 Pro (64-bit)", "Windows Server 2022 OR Ubuntu Linux 22.04 LTS"]
    ]
    build_styled_table(doc, hw_headers, hw_data, [Inches(1.8), Inches(2.4), Inches(2.5)])

    add_h2(doc, "8.1 Network & Firewall Configuration")
    net_headers = ["Port / Address", "Protocol / Service", "Access Scope & Purpose"]
    net_data = [
        ["Port 8000", "HTTP (TCP)", "Waitress WSGI Application Server (Hospital LAN Access)."],
        ["Port 80", "HTTP (TCP)", "Web Reverse Proxy (Nginx/IIS) - Redirects traffic to HTTPS."],
        ["Port 443", "HTTPS (TLS 1.3)", "Mandatory encrypted web access for secure signature transmission."],
        ["Static Internal IP", "IPv4 (e.g. `192.168.1.100`)", "Assigned via DHCP MAC reservation on hospital gateway router."]
    ]
    build_styled_table(doc, net_headers, net_data, [Inches(1.8), Inches(1.8), Inches(3.1)])

    # ----------------------------------------------------
    # SECTION 9: DESKTOP PACKAGING & DEPLOYMENT
    # ----------------------------------------------------
    add_h1(doc, "9. Standalone Desktop Packaging & Deployment")

    add_p(doc, 
          "The system supports a 100% turnkey standalone Windows deployment via PyInstaller and Inno Setup. "
          "A medical practitioner can run the entire blood bank digital system without installing Python or configuring web servers:")

    pkg_headers = ["Build Step / Script", "Command / Tool", "Output & Execution Details"]
    pkg_data = [
        [
            "1. Dependency Verification",
            "`pip install -r requirements.txt`",
            "Installs Flask, Waitress, OpenPyXL, and PyInstaller."
        ],
        [
            "2. Standalone Binary Compilation",
            "`build.bat` OR `python build_exe.py`",
            "Executes PyInstaller with `bloodbank.spec`. Compiles into `dist\\JankalyanBloodBank\\`."
        ],
        [
            "3. Setup Installer Generation",
            "`iscc inno_setup.iss`",
            "Compiles Inno Setup script into `dist_installer\\JankalyanBloodBank_Setup_v1.0.exe`."
        ],
        [
            "4. Runtime Bootstrap",
            "`JankalyanBloodBank.exe`",
            "Initializes `%APPDATA%` SQLite database, starts Waitress on port 8000, and auto-opens default browser."
        ]
    ]
    build_styled_table(doc, pkg_headers, pkg_data, [Inches(2.0), Inches(2.2), Inches(2.5)])

    # ----------------------------------------------------
    # SECTION 10: STANDARD OPERATING PROCEDURES (SOP) & TESTING
    # ----------------------------------------------------
    add_h1(doc, "10. Standard Operating Procedures (SOP) & QA Testing")

    add_h2(doc, "10.1 Clinical Workflow SOP")
    add_bullet(doc, "Staff logs in -> Clicks 'New Donor Form' -> Captures donor demographics, mobile number, and age.", bold_prefix="Step 1 (Reception): ")
    add_bullet(doc, "Staff presents tablet in Marathi or English -> Donor answers health questionnaire and medication history.", bold_prefix="Step 2 (Questionnaire): ")
    add_bullet(doc, "Staff records Weight, BP, Hb, Pulse, Temperature -> Verifies phlebotomy site -> Sets outcome to Eligible.", bold_prefix="Step 3 (Vitals Exam): ")
    add_bullet(doc, "Donor reads informed consent clauses -> Signs on the digital touch pad -> Staff submits for verification.", bold_prefix="Step 4 (Consent & Sign): ")
    add_bullet(doc, "Medical Officer logs in -> Reviews vitals and history -> Adds clinical remarks -> Confirms and finalises record.", bold_prefix="Step 5 (Medical Review): ")
    add_bullet(doc, "Phlebotomist records Blood Bag Barcode, Bag Type, Collected Volume, and monitors adverse reactions.", bold_prefix="Step 6 (Phlebotomy): ")
    add_bullet(doc, "Record is automatically locked. Staff can print Form QF/JKRP/18 on standard A4 paper or export to Excel.", bold_prefix="Step 7 (Finalization): ")

    add_h2(doc, "10.2 Automated Test Suite (`test_app.py`)")
    add_p(doc, "An automated Python unit test suite validates system integrity prior to production deployment:")
    add_bullet(doc, "Verifies credential validation, session creation, and role authorization.", bold_prefix="Test 01 & 02 (Authentication): ")
    add_bullet(doc, "Simulates Staff drafting record -> submitting -> Doctor signing -> verifying record is locked.", bold_prefix="Test 03 (End-to-End Workflow): ")
    add_bullet(doc, "Validates OpenPyXL spreadsheet generation, headers, and MIME type.", bold_prefix="Test 04 (Excel Export): ")
    add_bullet(doc, "Verifies `@media print` A4 rendering endpoint returns valid HTML.", bold_prefix="Test 05 (Print Engine): ")
    add_bullet(doc, "Tests Admin creating user, updating password, and soft-deleting accounts.", bold_prefix="Test 06 (User Management): ")
    add_bullet(doc, "Validates that non-admin accounts receive HTTP 403 Forbidden on administrative endpoints.", bold_prefix="Test 07 (RBAC Security): ")

    # Save document
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Jankalyan_Technical_Documentation.docx")
    doc.save(output_path)
    print(f"[OK] Document generated successfully at: {output_path}")
    print(f"[*] File Size: {os.path.getsize(output_path):,} bytes")

if __name__ == '__main__':
    generate_technical_documentation()
