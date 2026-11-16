from common.request_client import RequestClient
from config.settings import BASE_URL


class BaseAPI:
    client = RequestClient(BASE_URL)
