import time

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Understanding Streamlit Memory", layout="wide")

st.title("Understanding Streamlit memory and turbo caching")

st.write(
    "Streamlit apps rerun from top to bottom every time the user clicks or types. "
    "That means you need two different tools: one for remembering values, and one for speeding up expensive work."
)

st.info(
    "Simple model: `st.session_state` is the app's memory, and `st.cache_data` / `st.cache_resource` are the turbo chargers."
)


st.header("1. Memory: keep a value between reruns")
st.write(
    "Use `st.session_state` when you want the app to remember something like a click count, a form value, or a selected option."
)

if "click_count" not in st.session_state:
    st.session_state.click_count = 0

left_col, right_col = st.columns(2)

with left_col:
    if st.button("Add one click", key="add_one_click_button"):
        st.session_state.click_count += 1

    st.write(f"Current click count: {st.session_state.click_count}")

with right_col:
    st.code(
        '''if "click_count" not in st.session_state:
    st.session_state.click_count = 0

if st.button("Add one click", key="add_one_click_button"):
    st.session_state.click_count += 1

st.write(f"Current click count: {st.session_state.click_count}")''',
        language="python",
    )

st.caption(
    "Why this is memory: the count survives the next rerun, so the app does not forget it after a button click."
)


st.header("2. Turbo caching: avoid doing the same expensive work again")
st.write(
    "Use `st.cache_data` for data or computation, and `st.cache_resource` for objects that are expensive to create and can be reused."
)


@st.cache_data
def build_report_rows(report_name: str) -> pd.DataFrame:
    """Simulate an expensive data-building task."""
    time.sleep(5)
    return pd.DataFrame(
        {
            "metric": ["rows", "columns", "status"],
            "value": [1200, 8, f"ready for {report_name}"],
        }
    )


report_name = st.text_input("Report name", value="sales")

if st.button("Build report", key="build_report_button"):
    start_time = time.time()
    report_df = build_report_rows(report_name)
    elapsed_seconds = time.time() - start_time
    st.write(f"Build finished in {elapsed_seconds:.2f} seconds")
    st.dataframe(report_df, use_container_width=True)

st.code(
    '''@st.cache_data
def build_report_rows(report_name: str) -> pd.DataFrame:
    time.sleep(2)
    return pd.DataFrame({
        "metric": ["rows", "columns", "status"],
        "value": [1200, 8, f"ready for {report_name}"],
    })''',
    language="python",
)

st.caption(
    "If you click Build report again with the same report name, Streamlit can reuse the cached result instead of rebuilding it from scratch."
)


st.header("3. Turbo caching for reusable objects")
st.write(
    "Use `st.cache_resource` for things like database connections, clients, or model objects that should be created once and reused."
)


@st.cache_resource
def create_fake_client() -> dict:
    """Simulate creating a reusable client object."""
    time.sleep(10)
    return {"client_name": "demo-client", "created_for": "reused across reruns"}


client = create_fake_client()
st.write("Cached client object:", client)

st.code(
    '''@st.cache_resource
def create_fake_client() -> dict:
    time.sleep(1)
    return {"client_name": "demo-client", "created_for": "reused across reruns"}

client = create_fake_client()''',
    language="python",
)


st.header("4. When to use what")
st.write(
    "Use the right tool for the job: memory for values you want to keep, data cache for repeated computations, and resource cache for reusable connections or clients."
)

st.success(
    "Rule of thumb: if you need to remember a user choice, use `st.session_state`. If you need to speed up repeated work, use `st.cache_data` or `st.cache_resource`."
)
