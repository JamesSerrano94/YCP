from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import RedirectResponse
from typing import Optional, Dict
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlencode
import logging

from ..models.login import User, CASConfig

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["authentication"])

# Initialize CAS config directly
cas_config = CASConfig(
    version="CAS2.0",
    sso_base_url="https://secure.its.yale.edu/cas"
)

# Store active sessions (in production, use Redis or similar)
active_sessions: Dict[str, User] = {}

class CASClient:
    def __init__(self, config: CASConfig):
        self.config = config

    async def validate_ticket(self, ticket: str, service_url: str) -> Optional[User]:
        """Validate CAS ticket and return user information"""
        validate_url = f"{self.config.sso_base_url}/serviceValidate"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    validate_url,
                    params={"ticket": ticket, "service": service_url}
                )

                if response.status_code != 200:
                    return None

                # Parse XML response
                root = ET.fromstring(response.text)
                ns = {"cas": "http://www.yale.edu/tp/cas"}

                success = root.find(".//cas:authenticationSuccess", ns)
                if success is not None:
                    user_node = success.find("cas:user", ns)
                    if user_node is not None:
                        net_id = user_node.text
                        # Extract additional attributes if needed
                        return User(net_id=net_id)
            except Exception as e:
                logger.error(f"Error validating ticket: {str(e)}")
                return None

        return None

cas_client = CASClient(cas_config)

async def get_current_session(request: Request) -> Optional[User]:
    """Get current user from session"""
    session_id = request.cookies.get("session_id")
    logger.debug(f"get_current_session: session_id from cookies: {session_id}")
    user = active_sessions.get(session_id)
    logger.debug(f"get_current_session: user from active_sessions: {user}")
    return user


from fastapi.responses import RedirectResponse


@router.get("/auth")
async def cas_auth(
        request: Request,
        ticket: Optional[str] = None,
):
    """Handle CAS authentication"""
    service_url = str(request.url_for("cas_auth"))
    if not ticket:
        # Redirect to CAS login page with 'service' parameter
        params = {'service': service_url}
        redirect_url = f"{cas_config.sso_base_url}/login?{urlencode(params)}"
        return RedirectResponse(url=redirect_url)

    user = await cas_client.validate_ticket(ticket, service_url)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid CAS ticket")

    # Create session
    session_id = f"session_{user.net_id}_{datetime.utcnow().timestamp()}"
    active_sessions[session_id] = user
    logger.debug(f"Created session for user {user.net_id} with session_id {session_id}")

    # Create the RedirectResponse
    redirect_response = RedirectResponse(url="/")
    # Set session cookie on the RedirectResponse
    redirect_response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        path="/"
    )
    # Return the RedirectResponse
    return redirect_response

@router.get("/check")
async def check_auth(
        request: Request
):
    """Check authentication status"""
    current_user = await get_current_session(request)
    if current_user:
        return {"auth": True, "user": current_user}
    return {"auth": False}

@router.get("/logout")
async def logout(
        request: Request,
        response: Response
):
    """Handle logout"""
    session_id = request.cookies.get("session_id")
    if session_id in active_sessions:
        del active_sessions[session_id]

    response.delete_cookie("session_id")
    return {"success": True}

async def require_auth(request: Request):
    """Dependency for protected routes"""
    session_id = request.cookies.get("session_id")
    logger.debug(f"require_auth: session_id from cookies: {session_id}")
    current_user = await get_current_session(request)
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return current_user

@router.get("/test_require_auth")
async def test_require_auth(user: User = Depends(require_auth)):
    return {"Hello, ": user.net_id}