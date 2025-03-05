from ..utils import handle_api_errors, get_auth_header
from config import API_BASE_URL
from session import get_session

operations_url = f"{API_BASE_URL}/operations/"


@handle_api_errors()
async def list_operations_api(token_key, params):
    session = get_session()
    return await session.get(url=operations_url,
                             params=params,
                             headers=get_auth_header(token_key))


@handle_api_errors()
async def create_operation_api(token_key, json_data):
    session = get_session()
    return await session.post(url=operations_url,
                              headers=get_auth_header(token_key),
                              json=json_data)


@handle_api_errors()
async def delete_operation_api(token_key, operation_id):
    session = get_session()
    return await session.delete(url=f"{operations_url}{operation_id}/",
                                headers=get_auth_header(token_key))


@handle_api_errors()
async def update_operation_api(token_key, operation_id, json_data):
    session = get_session()
    return await session.patch(url=f"{operations_url}{operation_id}/",
                               headers=get_auth_header(token_key),
                               json=json_data)


@handle_api_errors()
async def get_recent_operations_api(token_key, params):
    session = get_session()
    return await session.get(url=f"{operations_url}recent/",
                             params=params,
                             headers=get_auth_header(token_key))
