# Jankalyan Blood Bank Digital Form System (QF/JKRP/18)
### (रक्तपेढी संगणकीय फॉर्म प्रणाली)

A lightweight, secure, tablet-friendly internal Blood Bank Digital Form System built for hospitals and blood donation centres. Digitises the standard **QF/JKRP/18** 4-page Paper Blood Donor Registration, Screening, Questionnaire, Consent, and Medical Officer Verification Workflow in **English and Marathi**.

---

## Technology Stack

- **Backend:** Python 3 + Flask framework
- **Database:** SQLite 3 (`database/bloodbank.db`)
- **Excel Export Engine:** `openpyxl`
- **Frontend:** Vanilla HTML5, CSS3, Vanilla JavaScript (No heavy frameworks, No React/Next/TS)
- **Signature Engine:** Touch/Stylus Pointer Events HTML5 Canvas

---

## Key Features

1. **Exact Form Digitisation (`QF/JKRP/18`):** Digitises all 4 paper form pages including Demographics, Medical Exam, 10+ Medication Timeframes, 25+ Permanent Deferral Checkboxes, Symptoms, Female-specific questions, 24-hr High-Risk duties, Blood Bag collection, and Donor Consent.
2. **Bilingual Engine (`[ English ] [ मराठी ]`):** Real-time language switching across UI, form fields, tooltips, validation messages, and printouts.
3. **Role-Based Access Control (RBAC):**
   - **ADMIN:** Manage users, view records, search, print, export Excel, view audit logs, database backup/restore.
   - **STAFF:** Create donor records, enter demographics, fill questionnaire, medical screening, save drafts, submit for verification.
   - **MEDICAL_OFFICER:** Review screening, clinical notes, capture electronic signature, finalise & lock records.
4. **Touch & Stylus Electronic Signature:** HTML5 Canvas signature pad supporting finger touch, stylus, and mouse.
5. **Signed Record Locking:** Immutable record locking upon Medical Officer signature. Authorised unlock procedure provided for audited administrative updates.
6. **Pixel-Perfect A4 Printing:** `@media print` CSS template reproducing the exact `QF/JKRP/18` paper form structure.
7. **Excel Data Export:** Filtered donor record export to `.xlsx`.
8. **Audit Logging & Database Backup:** Comprehensive logging of all system actions and one-click SQLite database backup/restore.

---

## Default Accounts

| Role | Username | Password | Full Name / Description |
|---|---|---|---|
| **ADMIN** | `admin` | `Admin@123` | System Administrator |
| **STAFF** | `staff` | `Staff@123` | Blood Bank Staff Person |
| **MEDICAL_OFFICER** | `doctor` | `Doctor@123` | Dr. Rajesh Sharma (Medical Officer) |

---

## Quick Start & Installation

### Prerequisites
- Python 3.8+ installed on your system.

### Setup Instructions

1. **Clone/Navigate to Project Directory:**
   ```bash
   cd d:\Jankalyaan_Digitalized_Form
   ```

2. **Install Python Dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Initialize SQLite Database & Seed Data:**
   ```bash
   python database/db_init.py
   ```

4. **Run Server:**
   ```bash
   python app.py
   ```

5. **Access Application:**
   Open browser at `http://localhost:8000` (or `http://<hospital-server-ip>:8000` on hospital LAN).

---

## Backup & Restore Procedure

### Database Backup
1. Log in as an **ADMIN**.
2. Navigate to **Audit Logs** page (`/audit.html`).
3. Click **Download Database Backup (`bloodbank.db`)**.
4. Store the downloaded `.db` file in a secure location.

### Database Restore
1. Log in as an **ADMIN**.
2. Navigate to **Audit Logs** page (`/audit.html`).
3. Choose the backup `.db` file and click **Restore Database**.

---

## Verification & Testing

An automated API and system test script is provided in `test_app.py`.

To execute tests:
```bash
python test_app.py
```

---

## Standalone Desktop (.EXE) & Inno Setup Packaging

To package the application into a standalone Windows installer:
1. Build the standalone executable with PyInstaller:
   ```bash
   python build_exe.py
   ```
2. Compile the Inno Setup script [`inno_setup.iss`](inno_setup.iss) using Inno Setup Compiler.
3. For full details and SQLite persistent storage architecture, see [`PACKAGING_GUIDE.md`](PACKAGING_GUIDE.md).
