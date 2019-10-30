#!/usr/bin/python

from os import environ
import sys
import time
import schedule
import urllib.request
import boto3

client = boto3.client('route53')

def getPublicIP():
    print('Retrieving public IP address')
    return urllib.request.urlopen('https://checkip.amazonaws.com').read().decode('utf-8')

def updateRecord():
    print('Making dyndns update call')
    response = client.change_resource_record_sets(
        HostedZoneId=environ['ZONEID'],
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': environ['FQDN'],
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': getPublicIP()
                            },
                        ],
                    }
                },
            ]
        }
    )
    print('Status : ' + response['ChangeInfo']['Status'])

def main():
    if ( 'ZONEID' not in environ or
         'FQDN' not in environ or
         'AWS_ACCESS_KEY_ID' not in environ or
         'AWS_SECRET_ACCESS_KEY' not in environ):
        print('Not all needed environment variables were set!')
        print('We need ZONEID, FQDN, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')
        sys.exit()

    schedule.every().hour.do(updateRecord)

    while True:
        schedule.run_pending()
        time.sleep(1)

main()

