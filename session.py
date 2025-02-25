import aiohttp

_session = None

def get_session():
    """Возвращает сессию, создавая ее при необходимости."""
    global _session
    if _session is None:
        _session = aiohttp.ClientSession()
    return _session

async def close_session():
    """Закрывает сессию, если она была создана."""
    global _session
    if _session is not None:
        await _session.close()
        _session = None