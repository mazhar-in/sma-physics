<div align="center">

# 🌌 SMA Physics — Daily Practice Problems (DPP) Portal

[![Live Platform](https://img.shields.io/badge/Live%20Portal-daily--practice--sheets--dpps.smaphysics.com-4F46E5?style=for-the-badge&logo=vercel&logoColor=white)](https://daily-practice-sheets-dpps.smaphysics.com/)
[![Built with Vanilla JS & Tailwind](https://img.shields.io/badge/Stack-TailwindCSS%20v4%20%7C%20KaTeX-38BDF8?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://daily-practice-sheets-dpps.smaphysics.com/)
[![Automated Publishing](https://img.shields.io/badge/Automation-Python%20%7C%20Cron-10B981?style=for-the-badge&logo=python&logoColor=white)](https://github.com/)

**An automated, high-performance Physics learning ecosystem providing daily concept capsules, timed CBT exam rooms, and printable high-density worksheets for JEE Main, JEE Advanced, and NEET aspirants.**

[Explore Platform](https://daily-practice-sheets-dpps.smaphysics.com/) • [Solve Today's DPP](https://daily-practice-sheets-dpps.smaphysics.com/practice) • [Worksheet Vault](https://daily-practice-sheets-dpps.smaphysics.com/#archive) • [Author](https://instagram.com/mazharin)

---

</div>

## 📌 Overview

**SMA Physics** is an open-access educational platform built to deconstruct complex physics derivations into intuitive 3-minute concept capsules, real-time Computer Based Tests (CBT), and high-density 2-column printable PDF worksheets.

The platform runs on a **zero-server, JSON-driven headless architecture**, allowing automated batch publishing, client-side date gating, and instantaneous global delivery via Vercel Edge.

---

## ⚡ Key Features

* **💡 3-Minute Concept Capsules:** High-yield theory breakdowns highlighting governing equations and typical competitive exam traps.
* **⏱️ Interactive CBT Simulator:**
  * Real-time countdown examination timer.
  * Interactive 20-question navigation palette.
  * In-place **Fisher-Yates randomization** of both question order and option keys ($A, B, C, D$) on every reload with dynamic answer-key remapping.
  * Instant step-by-step LaTeX derivations rendered using KaTeX.
* **📂 Exam & Chapter Segregation:**
  * Instant toggling between **NEET**, **JEE Main**, and **JEE Advanced** tracks.
  * Auto-classified chapter modules and dedicated topic landing pages (`/chapter/:slug` and `/dpp/:slug`).
* **🔍 Instant Search Engine:** Real-time debounced keyword search across 100+ problem sets, formulas, and chapters.
* **📄 Automated Worksheet Downloads:** Asynchronous Blob downloader providing clean, human-readable file titles (`Topic_Name_SMA_Physics.pdf`).
* **🌓 System-Adaptive Dark Mode:** Persistent light/dark mode with contrast-calibrated LaTeX math rendering.

---

## 🛠️ Tech Stack & Architecture

[ inbox/ (JSON + PDF) ] ───► [ publish.py ] ───► [ daily-dpps.json ] ───► [ Git Push ] ───► [ Vercel Edge ]

| Layer | Technology |
| :--- | :--- |
| **Frontend Runtime** | Vanilla JavaScript (ES6+), HTML5, Tailwind CSS |
| **Math Engine** | KaTeX `0.16.8` (Display & Inline LaTeX Parsing) |
| **Data Layer** | Dynamic JSON Schema Manifest (`daily-dpps.json`) |
| **Automation** | Python 3 (`subprocess`, `shutil`, `json`), ReportLab |
| **Hosting & CDN** | Vercel Edge Network |
| **SEO & Discovery** | Schema.org JSON-LD, Dynamic OpenGraph, Subdomain Canonical URLs |

---

## 📁 Repository Structure

```text
├── inbox/                  # Staging area for raw JSON drops & PDFs
├── queue/                  # Scheduled future DPP drops for automated releases
├── dpps/                   # Production-ready datasets & printable PDFs
│   ├── dpp-42/
│   └── dpp-43/
│       ├── dpp-43.json     # Questions, derivations, SEO metadata & capsule
│       └── SMA_DPP_43.pdf  # 2-Column printable PDF
├── daily-dpps.json         # Master manifest driving the site index & routing
├── index.html              # Homepage, Chapter Directory & Worksheet Vault
├── practice.html           # Full-screen randomized CBT Examination Room
├── about.html              # Platform philosophy, educator bio & methodology
├── publish.py              # 1-Click publisher & Git automation script
├── release_cron.py         # Headless daily scheduler engine
└── vercel.json             # Edge rewrite routing rules (/dpp, /chapter, /practice)

🚀 1-Click Publishing Workflow
To publish a new daily problem set without editing HTML or configuring servers:

Drop dpp-XX.json and optional SMA_DPP_XX.pdf into inbox/.

Run the automation engine:

Bash
python publish.py
The engine automatically creates directories, updates the manifest, executes Git commits, triggers Vercel deployments, and outputs the live link.

👨‍🏫 About the Author
Designed and Developed by Syed Mazhar Ali

JEE / NEET Physics Trainer & Software Developer

🌐 Live Portal: daily-practice-sheets-dpps.smaphysics.com

📸 Instagram: @mazharin

📄 License
This repository and all educational question datasets are licensed under the MIT License. Free for students and educators preparing for competitive examinations.