import streamlit as st
import sqlite3
import bcrypt

# Connect to database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()

# Title
st.title("Secure Authentication System")


# =========================
# REGISTER
# =========================

st.subheader("Create Account")

username = st.text_input("Username", key="register_username")
password = st.text_input(
    "Password",
    type="password",
    key="register_password"
)

if st.button("Register"):
    if username and password:
        try:
            # Hash password before storing it
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            )

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password.decode("utf-8"))
            )

            conn.commit()

            st.success("Account created successfully!")

        except sqlite3.IntegrityError:
            st.error("Username already exists.")

    else:
        st.warning("Please enter username and password.")


# =========================
# LOGIN
# =========================

st.subheader("Login")

login_username = st.text_input(
    "Username",
    key="login_username"
)

login_password = st.text_input(
    "Password",
    type="password",
    key="login_password"
)

if st.button("Login"):

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (login_username,)
    )

    user = cursor.fetchone()

    if user:

        stored_password = user[2].encode("utf-8")

        if bcrypt.checkpw(
            login_password.encode("utf-8"),
            stored_password
        ):
            st.success("Login successful! Welcome.")
        else:
            st.error("Invalid username or password.")

    else:
        st.error("Invalid username or password.")