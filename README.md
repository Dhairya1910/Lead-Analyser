# 🧠 Company Finder with Google Maps Scraper + Sentence Transformer

This project combines web scraping and natural language processing to build a **smart company finder**. It scrapes company information from **Google Maps** using Selenium, stores them in a structured format, and uses a **Sentence Transformer model** (`all-MiniLM-L6-v2`) to semantically match companies to user queries.

---

## 🚀 Features

- ✅ Scrapes company data from Google Maps:
  - Name
  - Address
  - Phone Number
  - Website
  - Ratings
- 🔍 Matches companies to user queries using Sentence Transformers
- 🧠 Finds semantically similar companies from a refined dataset
- 📁 Stores output in a clean CSV format

---

## 📂 Project Structure
├── model.py # Semantic matching using Sentence Transformers
├── scraper.py # Scraper for Google Maps using Selenium
├── refined_100_companies.csv # Sample cleaned dataset (Company Name, Industry, etc.)
├── README.md # Project documentation


## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/company-finder-nlp-scraper.git
cd company-finder-nlp-scraper






