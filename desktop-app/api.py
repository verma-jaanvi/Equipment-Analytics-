import requests

BASE_URL = "http://127.0.0.1:8000/api/"
TOKEN = None


# =====================================================
# ✅ Signup (NEW Feature Added Safely)
# =====================================================
def signup(username, email, password):
    """
    Creates a new user in SQLite backend.
    Does not affect existing login/upload/history/report logic.
    """
    response = requests.post(
        BASE_URL + "signup/",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    response.raise_for_status()
    return response.json()


# =====================================================
# ✅ Login (UNCHANGED)
# =====================================================
def login(username, password):
    global TOKEN

    response = requests.post(
        BASE_URL + "token/",
        data={"username": username, "password": password}
    )

    response.raise_for_status()
    TOKEN = response.json()["token"]
    return TOKEN


# =====================================================
# ✅ Logout (FIX ADDED ✅)
# =====================================================
def logout():
    """
    Clears the session token locally.
    UI expects this function.
    Backend logout endpoint is not required.
    """
    global TOKEN
    TOKEN = None


# =====================================================
# ✅ Attach token in headers (UNCHANGED)
# =====================================================
def auth_headers():
    if TOKEN is None:
        raise Exception("User not logged in. TOKEN missing.")

    return {"Authorization": f"Token {TOKEN}"}


# =====================================================
# ✅ Upload CSV (UNCHANGED)
# =====================================================
def upload_csv(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            BASE_URL + "upload/",
            headers=auth_headers(),
            files={"file": f},
        )

    response.raise_for_status()
    return response.json()


# =====================================================
# ✅ Get last 5 uploads (UNCHANGED)
# =====================================================
def get_history():
    response = requests.get(
        BASE_URL + "history/",
        headers=auth_headers()
    )

    response.raise_for_status()
    return response.json()


# =====================================================
# ✅ Download PDF report (UNCHANGED)
# =====================================================
def download_report(dataset_id, save_path):
    response = requests.get(
        BASE_URL + f"report/{dataset_id}/",
        headers=auth_headers(),
        stream=True,
    )

    response.raise_for_status()

    with open(save_path, "wb") as file:
        file.write(response.content)