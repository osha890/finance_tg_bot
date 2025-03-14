from ..utils import handle_api_errors, get_auth_header
from config import API_BASE_URL
from session import get_session

accounts_url = f"{API_BASE_URL}/accounts/"


@handle_api_errors()
async def list_accounts_api(token_key):
    session = get_session()
    return await session.get(url=accounts_url,
                             headers=get_auth_header(token_key))


@handle_api_errors()
async def create_account_api(token_key, json_data):
    session = get_session()
    return await session.post(url=accounts_url,
                              headers=get_auth_header(token_key),
                              json=json_data)


@handle_api_errors()
async def delete_account_api(token_key, account_id):
    session = get_session()
    return await session.delete(url=f"{accounts_url}{account_id}/",
                                headers=get_auth_header(token_key))


@handle_api_errors()
async def update_account_api(token_key, account_id, json_data):
    session = get_session()
    return await session.patch(url=f"{accounts_url}{account_id}/",
                               headers=get_auth_header(token_key),
                               json=json_data)
