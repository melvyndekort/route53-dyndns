#!/usr/bin/python

import os
import sys
import socket
import urllib.request
import boto3

client = boto3.client('route53')

def getPublicIP():
    print('Retrieving public IP address')
    ip = urllib.request.urlopen('https://checkip.amazonaws.com').read().decode('utf-8').rstrip()
    print(ip)
    return ip

def getCurrentRecord():
    print('Retrieving current DNS record')
    ip = socket.gethostbyname(os.environ['FQDN'])
    print(ip)
    return ip

def updateRecord(ip):
    print('Making dyndns update call')
    response = client.change_resource_record_sets(
        HostedZoneId=os.environ['AWS_HOSTED_ZONE_ID'],
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': os.environ['FQDN'],
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': ip
                            },
                        ],
                    }
                },
            ]
        }
    )
    print('Status : ' + response['ChangeInfo']['Status'])

def testVariables():
    if ( 'AWS_HOSTED_ZONE_ID' not in os.environ or
         'FQDN' not in os.environ or
         'AWS_ACCESS_KEY_ID' not in os.environ or
         'AWS_SECRET_ACCESS_KEY' not in os.environ):
        print('Not all needed environment variables were set!')
        print('We need AWS_HOSTED_ZONE_ID, FQDN, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')
        sys.exit()

testVariables()

publicIP  = getPublicIP()
curRecord = getCurrentRecord()

if curRecord == publicIP:
    print('DNS record is up to date, no action needed')
else:
    updateRecord(publicIP)
