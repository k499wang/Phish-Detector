import pytest
from extract_features import has_https, classify_domain, has_nonstd_port, has_favicon, check_anchors

def test_classify_domain():
    assert classify_domain("google.com") == -1
    assert classify_domain("fakefakefakewow.ir") == 1
    assert classify_domain("hello.com") == 1
    
def test_has_https_invalid():
    assert has_https("https://google.com") == -1
    assert has_https("http://google.com") == -1

def test_has_nonstd_port():
    assert has_nonstd_port("http://google.com:8080") == 1

def test_has_favicon():
    assert has_favicon("https://www.google.com") == -1
    assert has_favicon("https://visitarandomwebsite.com/") == -1
    
    

def test_check_anchors(mock_requests):
    assert check_anchors("https://www.google.com") == 1