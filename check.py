#!/usr/bin/python

"""
This script uses the Zendesk API to perform a simple search of unassigned unclosed open tickets.
"""

import argparse
import os
import sys
import requests
import simplejson

# REST API endpoint
baseurl = 'https://wmf.zendesk.com/api/v2'
query   = 'type:ticket+assignee:none+status<closed'
fullurl = '%s/search.json?query=%s' % (baseurl, query)

# Enable debugging for more output
DEBUG=False

# Parse command line options
parser = argparse.ArgumentParser(description="Simple Zendesk API Query")
parser.add_argument('-u', '--user', 
    help='User name for API access - can also be an environment variable - ZENDESK_API_USER')
parser.add_argument('-t', '--token', 
    help='API Token - can also be read as an environment variable - ZENDESK_API_TOKEN')
args = parser.parse_args()


# Make sure we have needed variables
# If command line option was not given, check for environment variable, otherwise fail
if args.user is None and os.environ.get('ZENDESK_API_USER'):
    args.user = os.environ.get('ZENDESK_API_USER')
elif args.user is None:
    print 'ERROR: API user not given'
    parser.print_help()

if args.token is None and os.environ.get('ZENDESK_API_TOKEN'):
    args.token = os.environ.get('ZENDESK_API_TOKEN')
elif args.token is None:
    print 'ERROR: API token not defined'
    parser.print_help()
    sys.exit(2)

# Append '/token' to user, if not given
if not args.user.endswith('/token'):
    args.user+='/token'

# Debugging inputs
if DEBUG:
    print 'User:  ', args.user
    print 'Token: ', args.token
    print 'URL:   ', fullurl

# Make HTTP API request
r = requests.get(fullurl, auth=(args.user, args.token))

# Check for bad HTTP response
if r.status_code != 200:
    print 'ERROR %s in HTTP response' % (r.status_code)
    if DEBUG:
            print r.text
    sys.exit()

# Print matching count
if 'count' in r.json():
    print 'Unassigned Ticket Count:', r.json()['count']

# If it's a single ticket, you can't iterate over the list
if r.json()['count'] == 1:
    ticket=r.json()['results'][0]
    if DEBUG:
            print simplejson.dumps(ticket, sort_keys=True, indent=4)
    print 'From:    ', ticket['via']['source']['from']['name']
    print 'Subject: ', ticket['subject']
    print 'Ticket:   https://wmf.zendesk.com/agent/#/tickets/%s' % (ticket['id'])

# Iterate over many tickets
elif r.json()['count'] > 1:
    for ticket in r.json()['results']:
        print '-'*80
        if DEBUG:
            print simplejson.dumps(ticket, sort_keys=True, indent=4)
        print 'From:    ', ticket['via']['source']['from']['name']
        print 'Subject: ', ticket['subject']
        print 'Ticket:   https://wmf.zendesk.com/agent/#/tickets/%s' % (ticket['id'])

