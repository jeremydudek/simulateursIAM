import streamlit as st

# Defininition des pages
perf_page = st.Page("pages/performances.py", title="Performances", icon="🎈")
comp_page = st.Page("pages/comparaison.py", title="Comparaison", icon="❄️")

# Set up navigation
pg = st.navigation([perf_page, comp_page])

# Run the selected page
pg.run()