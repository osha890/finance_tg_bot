from config import API_BASE_URL
from session import get_session

from ..utils import handle_api_errors


@handle_api_errors()
async def register_api(json_data):
    session = get_session()
    return await session.post(f"{API_BASE_URL}/register/", json=json_data)
