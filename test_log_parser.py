# Testing for Log Parser
# test_log_parser.py
#
# Written by Neil Khatri
# on 09/08/2022
#
# This program tests all the functions in log_parser.py

from log_parser import (
    get_ip_address, 
    get_url, 
    count_unique_ip_addresses, 
    get_top_three
)

# Test get_ip_address function
ip_address_log_end = '- - [10/Jul/2018:22:21:28 +0200] ' \
+ '"GET /intranet-analytics HTTP/1.1" 200 3574'

def test_get_ip_address_normal():
    log = f'123.123.123.123 {ip_address_log_end}'
    assert get_ip_address(log) == '123.123.123.123'

def test_get_ip_address_medium():
    log = '12.12.12.12 {ip_address_log_end}'
    assert get_ip_address(log) == '12.12.12.12'

def test_get_ip_address_short():
    log = f'1.1.1.1 {ip_address_log_end}'
    assert get_ip_address(log) == '1.1.1.1'

def test_get_ip_address_short_2():
    log = f'1.2.3.4 {ip_address_log_end}'
    assert get_ip_address(log) == '1.2.3.4'

def test_get_ip_address_mixed():
    log = f'10.100.1.10 {ip_address_log_end}'
    assert get_ip_address(log) == '10.100.1.10'

def test_get_ip_address_mixed_2():
    log = f'255.0.255.0 {ip_address_log_end}'
    assert get_ip_address(log) == '255.0.255.0'


# Test get_url function
url_log_start = '177.71.128.21 - - [10/Jul/2018:22:21:28 +0200]'
url_log_end = '200 3574'

def test_get_url_normal():
    log = f'{url_log_start} "GET /intranet-analytics HTTP/1.1" {url_log_end}'
    assert get_url(log) == '/intranet-analytics'

def test_get_url_base():
    log = f'{url_log_start} "GET / HTTP/1.1" {url_log_end}'
    assert get_url(log) == '/'

def test_get_url_post():
    log = f'{url_log_start} "POST /intranet-analytics HTTP/1.1" {url_log_end}'
    assert get_url(log) == '/intranet-analytics'

def test_get_url_unusual():
    log = f'{url_log_start} "DELETE /intranet-analytics HTTP/4.0" {url_log_end}'
    assert get_url(log) == '/intranet-analytics'


# Test count_unique_ip_addresses function
def test_count_unique_ip_addresses():
    ip_addresses = [
        '123.123.123.123',
        '12.12.12.12',
        '1.1.1.1',
        '13.13.13.13',
        '121.121.121.121',
        '123.123.123.123',
        '255.255.255.255',
        '12.12.12.12'
    ]
    assert count_unique_ip_addresses(ip_addresses) == 6

def test_count_unique_ip_addresses_all_same():
    ip_addresses = [
        '123.123.123.123',
        '123.123.123.123',
        '123.123.123.123',
        '123.123.123.123',
        '123.123.123.123',
        '123.123.123.123',
        '123.123.123.123',
    ]
    assert count_unique_ip_addresses(ip_addresses) == 1

def test_count_unique_ip_addresses_all_different():
    ip_addresses = [
        '123.123.123.123',
        '12.12.12.12',
        '1.1.1.1',
        '13.13.13.13',
        '2.2.2.2',
        '255.255.255.255',
        '121.121.121.121'
    ]
    assert count_unique_ip_addresses(ip_addresses) == len(ip_addresses)


# Test get_top_three function
def test_get_top_three():
    ip_addresses = [
        '123.123.123.123',
        '12.12.12.12',
        '1.1.1.1',
        '123.123.123.123',
        '255.255.255.255',
        '255.255.255.255',
        '123.123.123.123',
        '12.12.12.12',
        '123.123.123.123',
        '12.12.12.12'
    ]
    expected_result = [
        ('123.123.123.123', 4),
        ('12.12.12.12', 3),
        ('255.255.255.255', 2)
    ]
    assert get_top_three(ip_addresses) == expected_result

def test_get_top_three_all_same():
    ip_addresses = [
        '123.123.123.123',
        '12.12.12.12',
        '1.1.1.1',
        '255.255.255.255'
    ]
    expected_result = [
        ('123.123.123.123', 1),
        ('12.12.12.12', 1),
        ('1.1.1.1', 1)
    ]
    assert get_top_three(ip_addresses) == expected_result

def test_get_top_three_some_same():
    ip_addresses = [
        '123.123.123.123',
        '12.12.12.12',
        '1.1.1.1',
        '123.123.123.123',
        '12.12.12.12',
        '255.255.255.255'
    ]
    expected_result = [
        ('123.123.123.123', 2),
        ('12.12.12.12', 2),
        ('1.1.1.1', 1)
    ]
    assert get_top_three(ip_addresses) == expected_result

def test_get_top_three_urls():
    urls = [
        'https://example.com/',
        'https://example.com/one',
        'https://example.com/two',
        'https://example.com/',
        'https://example.com/three',
        'https://example.com/',
        'https://example.com/three'
    ]
    expected_result = [
        ('https://example.com/', 3),
        ('https://example.com/three', 2),
        ('https://example.com/one', 1)
    ]
    assert get_top_three(urls) == expected_result