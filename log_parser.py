# Log Parser
# log_parser.py
#
# Written by Neil Khatri
# on 09/08/2022
#
# This program parses a log file and prints out the number of unique
# IP addresses, the top 3 most visited URLs and top 3 most active IP addresses

import re
from collections import Counter

# Given a log, the IP address of the log is extracted and returned
def get_ip_address(log):
    # Extract IP address using regex
    regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    # Get first match by using [0]
    ip_address = re.findall(regex, log)[0]
    return ip_address

# Given a log, the URL in the log is extracted and returned
def get_url(log):
    # Extract URL using regex - URL is between request type and HTTP so extract
    # what is between those two
    request_methods = 'GET|POST|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE|PATCH'
    # Target area is structured like "GET /url HTTP/1.1"
    regex = rf'(\b{request_methods}\b)(.*?)(\bHTTP\b)'
    result = re.search(regex, log)
    # The URL will be in the second group
    url = result.group(2).strip()
    return url

# Given a list of IP addresses, the number of unique IP addresses is returned
def count_unique_ip_addresses(ip_addresses):
    # Create a set from the list to remove duplicates
    unique_ip_addresses = set(ip_addresses)
    return len(unique_ip_addresses)

# Given a list, the three most common items in the list are returned with the
# item name and its occurrences
def get_top_three(list):
    # Count number of times each item appears in list
    list_count = Counter(list)
    # Get the 3 most common items in the list - if multiple have the same, it
    # chooses items that appeared first
    top_three_items = list_count.most_common(3)
    return top_three_items


# Read file
filename = 'programming-task-example-data.log'
log_file = open(filename, 'r')

# Create lists to store IP addresses and URLs
ip_addresses = []
urls = []

print(f"Reading {filename}...\n")
# Iterate through each line in log file
for log in log_file:
    # Extract IP address and URL and add them to their respective lists
    ip_address = get_ip_address(log)
    ip_addresses.append(ip_address)
    url = get_url(log)
    urls.append(url)


# Get required summarised contents of log file
num_unique_ip_addresses = count_unique_ip_addresses(ip_addresses)
# The most visited URLs and most active IP addresses essentially have same
# requirements (getting 3 most common) so the same function is used
most_visited_urls = get_top_three(urls)
most_active_ip_addresses = get_top_three(ip_addresses)


# Print number of unique IP addresses
print(f'The number of unique IP addresses is {num_unique_ip_addresses}.')
# Print three most visited URLs
print('The top three most visited URLs are:')
for i in range(3):
    url = most_visited_urls[i][0]
    visits = most_visited_urls[i][1]
    print(f'    {i + 1}. {url} (Visits: {visits})')
# Print three most visited IP addresses
print('The three most active IP addresses are:')
for i in range(3):
    ip_address = most_active_ip_addresses[i][0]
    count = most_active_ip_addresses[i][1]
    print(f'    {i + 1}. {ip_address} (Count: {count})')