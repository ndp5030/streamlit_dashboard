# streamlit_dashboard

## Analytics DB for sales/profit including breakdown of sector/location/month/etc
1. requirements.txt - venv created and libs installed locally 
2. cw_db.py - Main app which runs the analytics db. In cmd after activating venv, can run the command 'streamlit run cw_db.py'

Notes:
- get_geolocation() works and can pull in all locations using city/state. It's a bit slow so hardcoded into dicts
- Data is loaded into a pandas df from a csv file locally