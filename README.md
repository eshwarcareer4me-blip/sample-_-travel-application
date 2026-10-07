# Smart Food Management System

A standalone Streamlit application that lets an admin or employee manage a food inventory, search items, update stock, monitor expiry, and generate summary reports.

## Features
- Admin and employee login
- Add new food items
- View inventory in a table
- Search by food name or category
- Update quantity
- Remove food items
- Expiry monitoring
- Summary dashboard
- Persistent inventory storage in `inventory.json`

## Requirements
- Python 3.10+
- Streamlit

## Run the project locally
1. Open a terminal in the project folder.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Log in with:
   - Admin: `admin` / `admin123`
   - Employee: `employee` / `employee123`

## Project structure
- `app.py` – main Streamlit app
- `inventory.json` – saved inventory data
- `requirements.txt` – Python dependencies

## Notes
The project has been converted from the notebook logic into a reusable, independent app that can be run outside of Colab.
