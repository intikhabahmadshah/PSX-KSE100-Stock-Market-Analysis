# Pakistan Stock Exchange (PSX) KSE-100 Performance & Quantitative Analytics Dashboard

![PSX KSE-100 Benchmark Analytics](https://img.shields.io/badge/Pakistan%20Stock%20Exchange-KSE--100-0071E3?style=for-the-badge&logo=cashapp&logoColor=white)
![Streamlit Ready](https://img.shields.io/badge/Streamlit-App%20Ready-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Audited Sessions](https://img.shields.io/badge/Audited%20Sessions-50%2C330-059669?style=for-the-badge)

---

## Author & Academic Credentials
- **Lead Data Analyst:** **Intikhab Ahmad Shah**
- **Academic Affiliation:** **PSEB Bootcamp AI @ Iqra University (H9), Islamabad**
- **Cohort Track:** Artificial Intelligence & Quantitative Data Analytics

---

## Executive Project Overview
This repository provides an institutional-grade quantitative surveillance and visualization terminal for the **Pakistan Stock Exchange (PSX) KSE-100 index**. 

Covering **50,330 cleared daily trading sessions** across **48 primary constituent companies** between **January 2021 and August 2025**, this platform delivers rigorous exploratory data analysis, market microstructure data integrity verification, log-normal asset pricing models, and multi-asset macroeconomic cycle tracking.

---

## Key Market Highlights & Empirical Findings

| Metric / Dimension | Quantitative Finding | Economic & Microstructure Significance |
| :--- | :--- | :--- |
| **Benchmark Universe** | 48 Constituent Tickers | Complete KSE-100 index survivorship with ~1,151 continuous sessions per core stock. |
| **Cumulative Turnover** | 90.59 Billion Shares | Executed capital volume spanning 2021 through 2025 across all sectors. |
| **Price Location** | Median: PKR 134.84 \| Mean: PKR 856.77 | Extreme positive skewness (+6.88); over 75% of stock quotes trade under PKR 480. |
| **High Valuation Leaders** | UPFL (PKR 34,139.55), RMPL (PKR 12,000) | Authentic multinational valuations with low public float; **not** data errors. |
| **Penny Counter Benchmark** | K-Electric (PKR 1.57 - 6.20) | High-liquidity retail instrument absorbing over 20% of aggregate daily share churn. |
| **Macro Trend Phases** | 2021–Mid 2023 Bear vs. 2023–2025 Bull | Mid-2023 $3B IMF SBA agreement catalyzed a major rally (stocks up 250%–350%). |
| **Strongest Correlation** | Daily High vs. Close ($r = 0.9997$) | Near-unity multicollinearity among OHLC components; volume decouples from price ($r = -0.063$). |

---

## Repository Structure

```
├── app.py                     # Streamlit Cloud deployment application
├── index.html                 # Standalone Apple-grade interactive report terminal
├── flash_api.py               # Lightweight Python HTTP server & REST API
├── prepare_dashboard_data.py  # ETL pipeline script (cleans CSV into JSON cache)
├── psx_dashboard_data.json    # Pre-computed high-speed data payload
├── pak_stock (1).csv          # Raw PSX OHLCV daily market dataset (2021–2025)
├── PSX_KSE100_Analysis.ipynb  # Executive Jupyter Notebook (80 cells, audited)
├── requirements.txt           # Python dependencies for Streamlit Cloud
├── .streamlit/config.toml     # Streamlit theme configuration (Pure Light Mode)
├── Run_Apple_Dashboard.bat    # 1-click Windows launcher for local terminal
└── Run_Streamlit.bat          # 1-click Windows launcher for Streamlit app
```

---

## Analytical Modules Included

1. **Price Action & 20-Day Moving Average:** Real-time selection across all 48 stocks with 20D EMA and volume bars alongside recent 10-session tabular breakdowns.
2. **Cross-Sectional Valuation Spread:** Empirical histogram with direct data labels demonstrating log-normal asset pricing equilibrium.
3. **Monthly Seasonality:** Calendar month trading day consistency and volume turnover spikes in January and May.
4. **Sector Capital Density:** Donut chart with direct percentage labels showing Banking and Power & Utilities liquidity dominance (45%+).
5. **Outlier Valuation Forensics:** In-depth proof that high-denomination stocks represent authentic corporate capital rather than data errors.
6. **2021–2025 Rebased Performance Trajectory:** Cumulative return tracking rebased to Base = 100 in January 2021.
7. **Cross-Asset Pearson Correlation Heatmap:** Pairwise econometric correlation matrix explaining multicollinearity and volume-volatility co-movement.
8. **Master Listed Equities Surveillance Table:** Interactive search and sector filter pills across all 48 constituent instruments.

---

## How to Run Locally

### Option 1: Instant Local Terminal (Zero Extra Installation)
Simply run the included server script or double-click `Run_Apple_Dashboard.bat`:
```bash
python flash_api.py
```
Open **`http://localhost:5000`** in any web browser.

### Option 2: Streamlit Application
Install dependencies and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```
Or double-click `Run_Streamlit.bat`.

---

## Deploying to Streamlit Community Cloud

1. Fork or push this repository to your GitHub account (`https://github.com/intikhabahmadshah/PSX-KSE100-Stock-Market-Analysis`).
2. Visit **[share.streamlit.io](https://share.streamlit.io/)** and sign in with your GitHub account.
3. Click **"New app"**.
4. Select your repository: `intikhabahmadshah/PSX-KSE100-Stock-Market-Analysis`.
5. Set the Main file path to: `app.py`.
6. Click **"Deploy!"**. Your dashboard will be live at `https://<your-custom-name>.streamlit.app`.

---

## Project Governance & Institutional Acknowledgments

Special gratitude and formal acknowledgment to our mentors, coordinators, and organizing bodies:

- **Data Analyst & Author:** Intikhab Ahmad Shah  
  *PSEB Bootcamp AI @ Iqra University (H9), Islamabad*
- **Bootcamp Trainer:** Respected. Ma'am Mahnoor Salman  
  *Lead AI & Data Science Instructor • Mentorship & Technical Guidance*
- **Bootcamp Coordinator:** Respected. Mr. Furqan  
  *Program Coordinator • Cohort Management & Operational Support*
- **Bootcamp Organizers:** Pakistan Software Export Board (PSEB) & atomcamp  
  *National Tech Sector Enablers & Strategic Implementing Partners*

---
*Developed with institutional precision for the Pakistan Stock Exchange Data Analytics Project.*
