import requests
import webbrowser
import time


def test_cas_auth():
    """Test CAS authentication flow"""
    # Base URL of your FastAPI application
    BASE_URL = "http://localhost:8000"

    # Create a session to maintain cookies
    session = requests.Session()

    # Step 1: Check initial auth status
    print("\n1. Checking initial auth status...")
    response = session.get(f"{BASE_URL}/cas/check")
    print(f"Initial auth status: {response.json()}")

    # Step 2: Get CAS login URL
    print("\n2. Getting CAS login URL...")
    response = session.get(f"{BASE_URL}/cas/auth")
    data = response.json()
    cas_url = data.get('redirect')
    print(f"CAS Login URL: {cas_url}")

    # Step 3: Manual CAS login
    print("\nPlease:")
    print(f"1. Open this URL in your browser: {cas_url}?service={BASE_URL}")
    print("2. Login to CAS")
    print("3. After login, copy the 'ticket' parameter from the URL")
    ticket = input("\nEnter the ticket value: ").strip()

    # Step 4: Validate ticket
    print("\n4. Validating ticket with backend...")
    response = session.get(f"{BASE_URL}/cas/auth", params={"ticket": ticket})
    print(f"Auth response: {response.json()}")

    # Step 5: Verify authentication
    print("\n5. Verifying authentication...")
    response = session.get(f"{BASE_URL}/cas/check")
    print(f"Auth status: {response.json()}")

    # Step 6: Access protected route
    print("\n6. Accessing protected route...")
    response = session.get(f"{BASE_URL}/protected")
    print(f"Protected route response: {response.json()}")

    return session.cookies.get_dict()


if __name__ == "__main__":
    test_cas_auth()