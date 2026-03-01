import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Date to Day of Week", page_icon="📅", layout="centered")

st.title("Date → Day of Week")

date_input = st.date_input(
    "Pick a date",
    value=datetime.today(),
    help="Select a date to see which day of the week it is.",
)

days = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]
day_index = date_input.weekday()
day_name = days[day_index]

st.success(f"It is **{day_name}**.")