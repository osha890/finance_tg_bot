from .user_api import get_auth_header
from finance_tg_bot.app.utils import handle_api_errors
from finance_tg_bot.config import API_BASE_URL
from finance_tg_bot.session import get_session

categories_url = f"{API_BASE_URL}/categories/"


@handle_api_errors()
async def list_categories_api(token_key, params):
    session = get_session()
    return await session.get(url=categories_url,
                             params=params,
                             headers=get_auth_header(token_key))


@handle_api_errors()
async def create_category_api(token_key, json_data):
    session = get_session()
    return await session.post(url=categories_url,
                              headers=get_auth_header(token_key),
                              json=json_data)


@handle_api_errors()
async def delete_category_api(token_key, category_id):
    session = get_session()
    return await session.delete(url=f"{categories_url}{category_id}/",
                                headers=get_auth_header(token_key))


@handle_api_errors()
async def update_category_api(token_key, category_id, json_data):
    session = get_session()
    return await session.patch(url=f"{categories_url}{category_id}/",
                               headers=get_auth_header(token_key),
                               json=json_data)
