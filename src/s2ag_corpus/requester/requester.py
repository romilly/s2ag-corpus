import os
import time
from abc import ABC, abstractmethod
from dotenv import load_dotenv
load_dotenv()

import requests

REQUEST_OK = 200
BAD_REQUEST = 400
TOO_MANY_REQUESTS = 429


class ThrottledRequesterException(Exception):
    pass


class Requester(ABC):

    @abstractmethod
    def get(self, url: str) -> dict:
        pass

    @abstractmethod
    def post(self, url: str, ids: dict) -> dict:
        pass


class ThrottledRequester(Requester):
    # STANDARD_THROTTLING_DELAY = 10.1
    STANDARD_THROTTLING_DELAY = 0.15

    def __init__(self, delay=STANDARD_THROTTLING_DELAY):
        self.delay = delay
        self._last_request = time.monotonic()
        api_key = os.getenv('S2_API_KEY')
        self.headers = {"x-api-key": api_key}

    # TODO: handle gateway codes - see webinar info
    def get(self, url: str) -> dict:
        for i in range(20):
            self.throttle(i)
            response = requests.get(url, headers=self.headers)
            if response.status_code == TOO_MANY_REQUESTS:
                continue
            if response.status_code == BAD_REQUEST:
                raise ValueError(response.reason)
            if response.status_code != REQUEST_OK:
                print('error ',response.status_code)
                raise ThrottledRequesterException(response.reason)
            else:
                result = response.json()
                break
        return result

    def throttle(self, backoff=0):
        delay = self.delay*(1.5**backoff)
        gap = time.monotonic() - self._last_request
        if gap < delay:
            wait_time = delay - gap
            time.sleep(wait_time)
        self._last_request = time.monotonic()

    def post(self, url: str,  ids: dict) -> dict:
        for i in range(20):
            self.throttle(i)
            response = requests.post(url, json=ids, headers=self.headers)
            if response.status_code == TOO_MANY_REQUESTS:
                continue
            if response.status_code == BAD_REQUEST:
                raise ValueError(response.reason)
            if response.status_code != REQUEST_OK:
                print('error ',response.status_code)
                raise ThrottledRequesterException(response.reason)
            else:
                break
        return response.json()
