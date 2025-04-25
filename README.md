# 💼 Data Analyst Assignment - Automated Chat Report

This project processes customer chat logs and generates an Excel report with key insights.

## ✅ Features:
- Upload raw CSV chat data via web UI
- Auto generates Excel reports:
  - Chat Metrics (total, bot vs agent closed, deflection %)
  - Agent Performance (avg. response, CSAT)
  - Shift-wise CSAT scores
- Clean UI using Bootstrap
- Flask backend + Pandas for data processing

## 📁 Folder Structure:
- `app/` - Web app files
- `data/` - Upload your `data_dump.csv` here
- `reports/` - Auto-saves the generated Excel reports
- `generate_report.py` - Script that does all data crunching

## ▶️ How To Run:
1. Install dependencies:
