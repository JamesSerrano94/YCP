import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from backend.app.main import app
from backend.app.models.login import User
from urllib.parse import urlparse, parse_qs
import asyncio


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_auth_redirect(client):
    # Test that /auth without a ticket redirects to the CAS login page
    response = client.get("/auth", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert "Location" in response.headers

    redirect_url = response.headers["Location"]
    assert redirect_url.startswith("https://secure.its.yale.edu/cas/login")

    # Verify that the service parameter is included in the redirect URL
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    assert "service" in query_params
    # The service URL should match the application's /auth endpoint
    assert query_params["service"][0] == f"{client.base_url}/auth"

def test_auth_with_valid_ticket(client):
    # Mock the CASClient.validate_ticket method to return a User object
    with patch("backend.app.routers.login.CASClient.validate_ticket", new_callable=AsyncMock) as mock_validate_ticket, \
         patch("backend.app.routers.login.os.getenv") as mock_getenv:
        mock_validate_ticket.return_value = User(net_id="testuser")
        mock_getenv.return_value = str(client.base_url)

        # Simulate calling /auth with a valid ticket
        response = client.get("/auth?ticket=valid-ticket", follow_redirects=False)
        assert response.status_code in (302, 307)
        assert "Location" in response.headers
        assert response.headers["Location"] == str(client.base_url)

        # Check that the session_id cookie is set in the client
        assert "session_id" in client.cookies

        # Access a protected route with the session cookie
        response = client.get("/test_require_auth")
        assert response.status_code == 200
        assert response.json() == {"Hello, ": "testuser"}

def test_auth_with_invalid_ticket(client):
    # Mock the CASClient.validate_ticket method to return None (invalid ticket)
    with patch("backend.app.routers.login.CASClient.validate_ticket", new_callable=AsyncMock) as mock_validate_ticket:
        mock_validate_ticket.return_value = None

        # Simulate calling /auth with an invalid ticket
        response = client.get("/auth?ticket=invalid-ticket")
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid CAS ticket"}

def test_protected_route_without_auth(client):
    # Access a protected route without authentication
    response = client.get("/test_require_auth")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_logout_authenticated_user(client):
    # Mock validate_ticket to simulate authentication
    with patch("backend.app.routers.login.CASClient.validate_ticket", new_callable=AsyncMock) as mock_validate_ticket, \
         patch("backend.app.routers.login.os.getenv") as mock_getenv:
        mock_validate_ticket.return_value = User(net_id="testuser")
        mock_getenv.return_value = str(client.base_url)

        # Authenticate the user
        response = client.get("/auth?ticket=valid-ticket", follow_redirects=False)
        assert response.status_code in (302, 307)
        assert "session_id" in client.cookies

        # Log out the user
        response = client.get("/logout")
        assert response.status_code == 200
        assert response.json() == {"success": True}

        # Ensure the session cookie is deleted
        assert "session_id" not in client.cookies

        # Access a protected route to confirm logout
        response = client.get("/test_require_auth")
        assert response.status_code == 401

def test_logout_without_authentication(client):
    # Ensure no session exists
    client.cookies.clear()

    # Attempt to log out
    response = client.get("/logout")
    assert response.status_code == 200
    assert response.json() == {"success": True}

def test_require_auth_with_authentication(client):
    # Mock validate_ticket to simulate authentication
    with patch("backend.app.routers.login.CASClient.validate_ticket", new_callable=AsyncMock) as mock_validate_ticket, \
         patch("backend.app.routers.login.os.getenv") as mock_getenv:
        mock_validate_ticket.return_value = User(net_id="testuser")
        mock_getenv.return_value = str(client.base_url)

        # Authenticate the user
        response = client.get("/auth?ticket=valid-ticket", follow_redirects=False)
        assert "session_id" in client.cookies

        # Access a protected route
        response = client.get("/test_require_auth")
        assert response.status_code == 200
        assert response.json() == {"Hello, ": "testuser"}

@pytest.mark.asyncio
async def test_validate_ticket_success():
    cas_client = CASClient(cas_config)

    # Mock the HTTP response from CAS server
    valid_cas_response = """
    <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
        <cas:authenticationSuccess>
            <cas:user>testuser</cas:user>
        </cas:authenticationSuccess>
    </cas:serviceResponse>
    """

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = valid_cas_response

        # Call validate_ticket using 'await'
        user = await cas_client.validate_ticket("valid-ticket", "service-url")
        assert user is not None
        assert user.net_id == "testuser"

@pytest.mark.asyncio
async def test_validate_ticket_invalid_ticket():
    cas_client = CASClient(cas_config)

    # Mock the HTTP response from CAS server
    invalid_cas_response = """
    <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
        <cas:authenticationFailure code="INVALID_TICKET">
            Ticket ST-12345-abcdefg not recognized
        </cas:authenticationFailure>
    </cas:serviceResponse>
    """

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = invalid_cas_response

        # Call validate_ticket using 'await'
        user = await cas_client.validate_ticket("invalid-ticket", "service-url")
        assert user is None

@pytest.mark.asyncio
async def test_validate_ticket_exception():
    cas_client = CASClient(cas_config)

    # Simulate an exception during the HTTP request
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = Exception("Network error")

        # Call validate_ticket using 'await'
        user = await cas_client.validate_ticket("any-ticket", "service-url")
        assert user is None