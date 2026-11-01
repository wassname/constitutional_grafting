"""send_cached_request retries rate limits and timeouts instead of failing the row (v7 lost 31 rows to them). -- PI/Claude (chatdata), 2026-11-01"""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import httpx

from constitutional_grafting.data import model_requests as mr


class Resp:
    def __init__(self, code, body=None):
        self.status_code, self._body, self.text = code, body, "x"

    def json(self):
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("e", request=None, response=None)


OK = {"usage": {"cost": 0.0}, "choices": [{"finish_reason": "stop", "message": {"content": "hi"}}]}
REQ = {"endpoint": "https://example.invalid", "body": {"model": "m", "messages": []}}


class TestRetry(unittest.TestCase):
    def run_with(self, responses):
        calls = iter(responses)
        def post(*a, **k):
            r = next(calls)
            if isinstance(r, Exception):
                raise r
            return r
        with tempfile.TemporaryDirectory() as d, mock.patch.object(mr, "TRANSIENT_WAITS", (0, 0, None)), \
                mock.patch.object(mr, "api_headers", lambda: {}), mock.patch("httpx.post", post):
            return mr.send_cached_request(Path(d), REQ, context={})

    def test_429_then_ok(self):
        self.assertEqual(self.run_with([Resp(429), httpx.ReadTimeout("t"), Resp(200, OK)])["response"], OK)

    def test_400_is_not_retried(self):
        with self.assertRaises(httpx.HTTPStatusError):
            self.run_with([Resp(400), Resp(200, OK)])

    def test_gives_up_after_last_try(self):
        with self.assertRaises(httpx.HTTPStatusError):
            self.run_with([Resp(429), Resp(429), Resp(429)])


if __name__ == "__main__":
    unittest.main()
