
import pytest

import requests
from unittest.mock import patch, Mock, call

from marketorestpython.helper.http_lib import HttpLib


@pytest.fixture
def http():
    return HttpLib(max_retry_time_conf=300, requests_timeout=None)

def mock_response_side_effect(status_code, json_data):
    return Mock(status_code=status_code, json=lambda: json_data)

def test_http_get_retry_sends_access_token(http):
    """Test that requests.get is called with the access token in both cases if the first request fails"""
    access_token = '1234567890'
    with patch('marketorestpython.helper.http_lib.requests.get') as mock_get:
        mock_get.side_effect = [
            mock_response_side_effect(200, {'success': False, 'errors': [{'code': '604', 'message': 'Request timed out'}]}),
            mock_response_side_effect(200, {'success': True}),
        ]
        result = http.get('https://example.com', args={'access_token': access_token})

        mock_get.assert_has_calls([
            call('https://example.com', headers={'Authorization': f'Bearer {access_token}', 'Accept-Encoding': 'gzip'}, params={}, stream=False, timeout=None),
            call('https://example.com', headers={'Authorization': f'Bearer {access_token}', 'Accept-Encoding': 'gzip'}, params={}, stream=False, timeout=None),
        ])
        assert result == {'success': True}

def test_http_post_retry_sends_access_token(http):
    """Test that requests.get is called with the access token in both cases if the first request fails"""
    access_token = '1234567890'
    with patch('marketorestpython.helper.http_lib.requests.post') as mock_post:
        mock_post.side_effect = [
            mock_response_side_effect(200, {'success': False, 'errors': [{'code': '604', 'message': 'Request timed out'}]}),
            mock_response_side_effect(200, {'success': True}),
        ]
        result = http.post('https://example.com', args={'access_token': access_token}, data={'foo': 'bar'})

        mock_post.assert_has_calls([
            call('https://example.com', headers={'Authorization': f'Bearer {access_token}', 'Content-type': 'application/json; charset=utf-8'}, json={'foo': 'bar'}, params={}, timeout=None),
            call('https://example.com', headers={'Authorization': f'Bearer {access_token}', 'Content-type': 'application/json; charset=utf-8'}, json={'foo': 'bar'}, params={}, timeout=None),
        ])
        assert result == {'success': True}
