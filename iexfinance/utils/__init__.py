import requests


def _init_session(session, retry_count=3):
    if session is None:
        session = requests.session()
    return session
