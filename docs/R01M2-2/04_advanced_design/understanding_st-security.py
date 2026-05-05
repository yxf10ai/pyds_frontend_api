import streamlit as st
import time


st.set_page_config(page_title="Understanding Streamlit Security", layout="wide")

st.title("Understanding Streamlit security")

st.write(
    "Streamlit does not give you a full login system by itself. "
    "For simple apps, you can control access with `st.session_state`. "
    "For real production apps, use a proper authentication provider or an access gateway."
)

st.warning(
    "This file is a learning demo only. The login logic below is not secure enough for a real production app."
)


st.header("1. The basic idea")
st.write(
    "Security in Streamlit often means deciding who can see which part of the page. "
    "A common pattern is: show a login form first, then show protected content only after the user is authenticated."
)

st.code(
    '''if st.session_state.get("authenticated"):
    st.write("Protected content")
else:
    st.write("Please log in")''',
    language="python",
)


st.header("2. Demo login control")
st.write(
    "This demo uses a simple username/password check and stores the result in `st.session_state`. "
    "In a real app, the credentials should come from `st.secrets` or from an external identity provider."
)

DEFAULT_AUTH_CONFIG = {
    "users": {
        "admin": {"password": "admin123", "role": "admin"},
        "engineer01": {"password": "engineer123", "role": "viewer"},
        "engineer02": {"password": "engineer456", "role": "viewer"},
    }
}

AUTH_CONFIG = st.secrets.get("demo_auth", DEFAULT_AUTH_CONFIG)

st.code(
    '''# .streamlit/secrets.toml
[demo_auth.users.admin]
password = "use-a-real-secret"
role = "admin"

[demo_auth.users.engineer]
password = "another-secret"
role = "viewer"''',
    language="toml",
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "current_role" not in st.session_state:
    st.session_state.current_role = "guest"


def login_user() -> None:
    username = st.session_state.login_username
    password = st.session_state.login_password

    if st.session_state.authenticated:
        if username == st.session_state.current_user:
            st.session_state.login_error = "You are already logged in as this user. Please log out first if you want to re-authenticate."
        else:
            st.session_state.login_error = (
                f"Already logged in as {st.session_state.current_user}. Please log out before logging in as another user."
            )
        return

    user_record = AUTH_CONFIG.get("users", {}).get(username)

    if user_record and user_record.get("password") == password:
        st.session_state.authenticated = True
        st.session_state.current_user = username
        st.session_state.current_role = user_record.get("role", "viewer")
        st.session_state.login_error = ""
    else:
        st.session_state.authenticated = False
        st.session_state.current_user = ""
        st.session_state.current_role = "guest"
        st.session_state.login_error = "Wrong username or password!!!!!!."


def logout_user() -> None:
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.session_state.current_role = "guest"
    st.session_state.login_error = ""


if "login_username" not in st.session_state:
    st.session_state.login_username = ""

if "login_password" not in st.session_state:
    st.session_state.login_password = ""

if "login_error" not in st.session_state:
    st.session_state.login_error = ""


login_col, info_col = st.columns(2)

with login_col:
    st.subheader("Login form")

    if st.session_state.authenticated:
        st.info(
            f"You are currently logged in as {st.session_state.current_user}. Log out before trying another account."
        )
    else:
        with st.form("login_form"):
            st.text_input("Username", key="login_username")
            st.text_input("Password", type="password", key="login_password")

            login_clicked = st.form_submit_button("Log in")

        if login_clicked:
            login_user()

    if st.session_state.login_error:
        st.error(st.session_state.login_error)

with info_col:
    st.subheader("What happens here")
    st.write("1. The user enters a username and password.")
    st.write("2. The app checks them against the credential store in `st.secrets`.")
    st.write("3. If the check passes, the app sets `st.session_state.authenticated = True` and stores the user role.")
    st.write("4. The page then shows protected content.")


st.header("3. Protected content")

if st.session_state.authenticated:
    st.success(f"Logged in as {st.session_state.current_user}")
    st.caption(f"Role: {st.session_state.current_role}")
    st.write("Only authenticated users should see this section.")

    protected_left, protected_right = st.columns(2)

    with protected_left:
        st.subheader("Protected dashboard")
        st.metric("Secret score", 98)
        st.metric("Access level", "internal")

    with protected_right:
        st.subheader("Example actions")
        st.button("Sensitive action", key="sensitive_action_button")
        st.write("In a real app, this button would trigger a protected operation.")

        if st.session_state.current_role == "admin":
            st.warning("Admin-only controls would appear here.")
        else:
            time.sleep(10)
            st.info("Viewer accounts can see the dashboard, but not admin controls.")

    if st.button("!!Log OUT!!", key="logout_button"):
        logout_user()
        st.session_state.login_username = ""
        st.session_state.login_password = ""
        st.rerun()
else:
    st.info("You are not logged in yet. The protected area is hidden until authentication succeeds.")


st.header("4. Why this pattern matters")
st.write(
    "Streamlit reruns the script every time the user interacts with it. "
    "That means security decisions must be based on values stored in `st.session_state`, not on one-time variables."
)

st.code(
    '''if st.session_state.authenticated:
    st.write("Show protected content")
else:
    st.write("Hide protected content")''',
    language="python",
)


st.header("5. What to use in real projects")
st.write(
    "For a real application, do not hard-code passwords in the source file. "
    "Use a real identity provider, a reverse proxy, Streamlit Community Cloud access control, or your organization’s SSO solution."
)

st.write(
    "If you only need role-based access inside a trusted internal tool, keep the role in `st.session_state` and branch on it when showing content."
)

st.success(
    "Rule of thumb: use `st.session_state` for demo-level login state, and use a proper authentication system for real security."
)
