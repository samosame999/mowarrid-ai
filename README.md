# 🇦🇪 MOWARRID PRO (مُورّد)
### Autonomous Multi-Lingual AI Procurement, Voice Negotiation & Customs Agent for Dubai's Trade Ecosystem

![Status](https://img.shields.io/badge/Status-MVP_Ready-10b981?style=for-the-badge)
![Competition](https://img.shields.io/badge/Dubai_Chamber-Create_AI_Agents_Championship-d4af37?style=for-the-badge)
![Tech](https://img.shields.io/badge/Stack-FastAPI_|_SQLite_|_Tailwind_|_Vision_OCR-0284c7?style=for-the-badge)
![Languages](https://img.shields.io/badge/UI_&_PO_Languages-7_Global_Languages-f59e0b?style=for-the-badge)

<p align="center">
  <img src="LOGO.jpg" alt="Mowarrid Logo" width="180" style="border-radius: 16px;" />
</p>

---

## 📌 1. The Real-World Problem
Dubai is a global trade hub hosting over 200 nationalities, numerous Free Zones (**JAFZA**, **DIC**, **DHCC**), and thousands of international investors. However, B2B procurement and supply chain sourcing in Dubai still suffer from critical bottlenecks:
* **Time-Consuming Sourcing:** Procurement teams waste **5 to 7 business days** manually searching for verified local suppliers, sending RFQs, and waiting for quotations.
* **Language & Cultural Barriers:** International investors (speaking Chinese, Russian, Korean, French, Spanish, or English) struggle to coordinate seamlessly with local Arabic/English-speaking suppliers.
* **Complex Customs & Tax Calculations:** Manually verifying **Dubai Customs HS Codes**, Free Zone exemptions, and **5% UAE VAT** slows down deal execution.

---

## 💡 2. The Solution: Mowarrid Autonomous AI Agent
**Mowarrid PRO** is **not a chatbot**. It is an end-to-end **Autonomous AI Procurement Agent** engineered specifically for Dubai's business ecosystem across the **4 Core Pillars of Autonomous Agents**:

### 🧠 Pillar 01: Problem Understanding
* **Vision OCR Document Analyzer:** Reads uploaded PDF/Image invoices, RFPs, and tender specifications or accepts live **Multi-Lingual Voice Dictation**.
* Automatically extracts quantities, technical specs, target budgets (AED), and operational priorities.

### 🗺️ Pillar 02: Autonomous Planning & Decision-Making
* Dynamically builds a sourcing and negotiation strategy based on the selected Dubai commercial sector (*Hospitality*, *Construction*, or *Medical*).
* Routes search queries to optimal Dubai Free Zones (e.g., **JAFZA**) to secure customs duty exemptions and fast delivery.

### 🛠️ Pillar 03: Tool Integration & Active Execution
* **🏢 Dubai Merchants SQLite Database (`SQLite DB`):** Queries verified local suppliers and stock availability.
* **🛃 Dubai Customs HS Code Calculator (`HS Code API`):** Automatically identifies HS codes, duty exemptions, and 5% VAT.
* **📞 Live Bilingual Voice Negotiation (`UAE TDRA-Compliant SIP & WhatsApp API`):** Initiates a real-time simulated SIP voice call in **Arabic (🇦🇪)** or **English (🇬🇧)** to secure instant cash discounts (9% to 15%).

### 📄 Pillar 04: Task Completion & Official PO Issuance
* Evaluates counter-offers, ranks suppliers in a live **Comparison Matrix**, and selects the winning vendor.
* Automatically generates a legally formatted, printable **Official Purchase Order (PO)** in **7 global languages** (Arabic, English, French, Spanish, Russian, Chinese, and Korean).

---

## 🌐 3. Built for Global Investors: 7-Language Localization
The entire platform—including the **UI, Scenarios, SQLite Offer Matrix, and Official Printable Purchase Order (PO)**—supports instant switching across **7 global languages**:
1. 🇦🇪 **Arabic (العربية)**
2. 🇬🇧 **English (EN)**
3. 🇫🇷 **French (FR)**
4. 🇪🇸 **Spanish (ES)**
5. 🇷🇺 **Russian (RU)**
6. 🇨🇳 **Chinese (中文)**
7. 🇰🇷 **Korean (한국어)**

---

## 🛠️ 4. Installation & Setup
1. Ensure **Python** is installed on your system.
2. Open your terminal inside the project folder and install the required dependencies:
   ```bash
   pip install fastapi uvicorn pydantic


   Bash

python -m uvicorn server:app --reload


Plaintext

[http://127.0.0.1:8000](http://127.0.0.1:8000)
