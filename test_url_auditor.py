"""Network-free unit tests for URL auditor fallback and conservative statuses."""
import unittest
from unittest.mock import patch
import urllib.error
from audit_source_urls import check_url

class FakeHeaders(dict):
    pass
class FakeResponse:
    status = 200
    headers = FakeHeaders({'Content-Type': 'text/html; charset=utf-8'})
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def geturl(self): return 'https://example.edu/final'

class AuditorTests(unittest.TestCase):
    @patch('audit_source_urls.urllib.request.urlopen', return_value=FakeResponse())
    def test_head_success(self, mock_open):
        result = check_url('https://example.edu', retries=0)
        self.assertEqual(result['Reachability'], 'REACHABLE')
        self.assertEqual(result['Method'], 'HEAD')
        self.assertEqual(result['Final URL'], 'https://example.edu/final')

    @patch('audit_source_urls.urllib.request.urlopen', side_effect=[urllib.error.HTTPError('https://example.edu', 405, 'Method Not Allowed', {}, None), FakeResponse()])
    def test_head_rejected_get_fallback(self, mock_open):
        result = check_url('https://example.edu', retries=0)
        self.assertEqual(result['Reachability'], 'REACHABLE')
        self.assertEqual(result['Method'], 'GET')

    @patch('audit_source_urls.urllib.request.urlopen', side_effect=TimeoutError('timed out'))
    def test_timeout_is_review_not_invalid(self, mock_open):
        result = check_url('https://example.edu', retries=0)
        self.assertEqual(result['Reachability'], 'REVIEW')
        self.assertIn('TimeoutError', result['Check Detail'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
