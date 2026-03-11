import os
from datetime import datetime

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv


st.set_page_config(page_title="Date to Day of Week", page_icon="📅", layout="centered")

# Load variables from a local .env file (OPENAI_API_KEY, etc.)
load_dotenv()


def get_historical_events_for_date(date_value: datetime) -> str:
    """
    Use OpenAI to get important historical events for the given month/day.
    Returns a markdown string (or an error message) to display in the app.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "⚠️ OpenAI API key not configured. Set the `OPENAI_API_KEY` environment variable."

    client = OpenAI(api_key=api_key)

    month_day_str = date_value.strftime("%B %d")
    prompt = (
        f"List 3–5 important historical events that happened on {month_day_str} in history "
        f"(any years). For each event, include the year and a one-sentence description. "
        f"Format the answer as markdown bullet points."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise historical assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:  # pragma: no cover - defensive
        return f"⚠️ Error while calling OpenAI: {exc}"


st.title("Date → Day of Week")

date_input = st.date_input(
    "Pick a date",
    value=datetime.today(),
    min_value=date(1000, 1, 1),   # earliest selectable date
    max_value=date(3000, 12, 31), # latest selectable date
    help="Select a date to see which day of the week it is.",
)

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
day_index = date_input.weekday()
day_name = days[day_index]

st.success(f"It is **{day_name}**.")

st.markdown("### AI: Historical events on this date")

if "historical_events" not in st.session_state:
    st.session_state.historical_events = ""

if st.button("Ask AI for historical events"):
    with st.spinner("Asking AI about this date..."):
        st.session_state.historical_events = get_historical_events_for_date(date_input)

if st.session_state.historical_events:
    st.markdown(st.session_state.historical_events)
