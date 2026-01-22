# 🇮🇳 BuddySplit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**BuddySplit** is a "humanized" bill-splitting web application designed specifically for Indian users. It handles the math so you don't have to, ensuring that every paisa is accounted for when splitting bills with friends.

## ✨ Features
- **INR First:** Default currency set to Indian Rupees (₹).
- **The "Penny Gap" Fix:** Smart logic that assigns the rounding remainder to the primary payer so the total always matches the bill.
- **🌍 Foreign Exchange:** One-click toggle to see splits in USD, EUR, GBP, etc., using live exchange rates.
- **Buddy System:** Clear breakdown of who owes what, including a "Payer" badge.
- **Mobile Friendly:** Designed to work perfectly on smartphone browsers.

## 🚀 Quick Start

### Prerequisites
Ensure you have Python installed. Then, install the required libraries:
```bash
pip install streamlit requests pandas