#!/usr/bin/python

import os
import time
#import schedule
import urllib.request
import boto3

client = boto3.client('route53')

def getPublicIP():
    print('Retrieving public IP address')
    return urllib.request.urlopen('https://checkip.amazonaws.com').read().decode('utf-8')

def updateRecord():
    print('Making dyndns update call')
    response = client.change_resource_record_sets(
        HostedZoneId=os.environ['ZONEID'],
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
                                'Value': getPublicIP()
                            },
                        ],
                    }
                },
            ]
        }
    )
    print('Status : ' + response['ChangeInfo']['Status'])

#schedule.every().hour.do(updateRecord)

#while True:
#    schedule.run_pending()
#    time.sleep(1)
updateRecord()
