# Jankalyan Blood Centre & Hospital
## On-Premise Private Server Requirements & Technical Specifications
### Digital Blood Donation Form System (QF/JKRP/18)

---

## 1. Sensitive Data & Privacy Compliance
Blood donor demographic information, medical screening evaluations, test outcomes, and phlebotomy details constitute highly sensitive medical data under Healthcare Data Protection Standards (DISHA / ISO 27001).

To guarantee 100% data sovereignty, complete privacy, and zero data leakage to 3rd-party public clouds, this document outlines the exact hardware, software, network, port, database, and security requirements to host the Jankalyan Blood Bank application on a dedicated On-Premise Server inside the hospital's physical network.

---

## 2. Server Hardware & PC Specifications

| Component | Minimum Requirement | Recommended Specification |
| :--- | :--- | :--- |
| **Processor (CPU)** | Intel Core i3 (9th Gen) / AMD Ryzen 3 | Intel Core i5 (11th Gen+) / AMD Ryzen 5 |
| **System Memory (RAM)** | 8 GB DDR4 | 16 GB DDR4 / DDR5 |
| **Storage (Disk)** | 128 GB SATA SSD | 256 GB NVMe M.2 SSD (High Read/Write Speed) |
| **Network Interface** | 1 Gbps Ethernet LAN Port | 1 Gbps Dual-Port Ethernet / Gigabit Switch |
| **Operating System** | Windows 10 / 11 Pro 64-bit | Windows Server 2022 OR Ubuntu Linux 22.04 LTS |

---

## 3. Network, IP Address & Firewall Port Requirements

| Port / Address | Protocol / Service | Purpose & Access Scope |
| :--- | :--- | :--- |
| **Port 8000** | HTTP (TCP) | Flask / Waitress WSGI Application Server (Internal LAN Access) |
| **Port 80** | HTTP (TCP) | Web Reverse Proxy (Nginx / IIS) - Redirects traffic to HTTPS |
| **Port 443** | HTTPS (TCP / SSL) | Encrypted Web Access (Mandatory for Donor Digital Signatures) |
| **Static Internal IP** | LAN Address (e.g., `192.168.1.100`) | Assigned via DHCP MAC Reservation on Hospital Router |

---

## 4. Database & Storage Architecture

- **Engine:** Embedded SQLite 3 Database (`database/bloodbank.db`)
- **Relational Integrity:** 12 Normalized Relational Tables with CASCADE Foreign Keys
- **Estimated Database Size:** ~250 KB (Initial baseline) + ~15 MB per 1,000 completed forms (includes high-res base64 donor/doctor signatures).
- **Automated Backups:** Scheduled automated daily backup via Windows Task Scheduler / Cron to external USB drive or NAS (Network Attached Storage).

---

## 5. Production Software Stack & Environment

- **Python Environment:** Python 3.10+ (64-bit)
- **Production WSGI Server:** Waitress Server (for Windows) / Gunicorn (for Linux)
- **Reverse Proxy:** Nginx or Microsoft IIS (Internet Information Services)
- **SSL Certificate:** Local Certificate Authority (CA) or Self-Signed Certificate to ensure end-to-end TLS 1.3 encryption for signature canvases.

---

## 6. Client Device Requirements (Staff, Doctors & Tablets)

- **Client Devices:** Android / iPad Tablets (for donor signature), Desktop PCs, Laptops connected to hospital Wi-Fi.
- **Web Browser:** Modern Web Browser (Google Chrome 100+, Microsoft Edge 100+, Safari 15+).
- **Peripherals:** Touchscreen Stylus (optional for donor signature), Barcode Scanner (for scanning blood bag numbers).
