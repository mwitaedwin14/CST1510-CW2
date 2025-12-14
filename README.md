# CST1510 Coursework 2 – Multi-Domain Intelligence Platform  
Edwin Mwita – M01036583  
Degree: BSc Information Technology
  
https://github.com/mwitaedwin14/CST1510-CW2

## Project Overview
A secure, real-time web application built with **Python + Streamlit** that delivers intelligent insights for three domains:
- **Cybersecurity Analysts** – track and respond to incidents
- **Data Scientists** – manage and visualize dataset metadata
- **IT Administrators** – monitor and prioritize support tickets

**Primary focus**: Cybersecurity domain (Tier 1) with full secure authentication, real CSV data, live dashboard, and incident reporting. Data Science and IT Operations domains are implemented with dedicated views and visualizations.

## Key Features
- **Secure Authentication** – bcrypt hashing, login/registration with SQLite backend (Week 7)
- **Database Persistence** – SQLite with real data loaded from 3 CSV files (Week 8)
- **Live Cybersecurity Dashboard** – metrics, interactive bar chart, real-time table (Week 9)
- **Incident Reporting** – form to add new incidents with instant update
- **Multi-Domain Navigation** – sidebar switching between Cybersecurity, Data Science, and IT Operations
- **Gemini AI Assistant** – sidebar AI that analyzes current incidents using real data (Week 10)
- **Professional UI** – dark mode, responsive layout, clean design

## How to Run Locally
```bash
# Clone the repository
git clone https://github.com/mwitaedwin14/CST1510-CW2.git
cd CST1510-CW2

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Home.py
