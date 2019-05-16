import json
import boto3
import os
import time
import logging
import hashlib

from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from datetime import timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table_fd = dynamodb.Table('face_demographics')
table_fd_record = dynamodb.Table('face_demographics_record')
table_fd_camera = dynamodb.Table('face_detection_camera')


domainip = 'http://tapwayoffice.duckdns.org:8083/admin/API'
#domainip = 'http://192.168.0.2/admin/API'
username = "system"
password = "GoTapway123#"

# Global variable: token for login authorization
TOKEN = {"token": "", "randomkey": "", "signature": ""}
connect_timeout, read_timeout = 5.0, 30.0


def pass_encrypt(randomkey):
    # Random Key MD5 Hashing
    # randomkey = response.json()['randomKey']
    temp = hashlib.md5(password.encode())
    temp = temp.hexdigest()
    temp = hashlib.md5((username + temp).encode())
    temp = temp.hexdigest()
    temp = hashlib.md5(temp.encode())
    temp = temp.hexdigest()
    temp = hashlib.md5((username + ":DSS:" + temp).encode())
    temp = temp.hexdigest()
    signature = hashlib.md5((temp + ":" + randomkey).encode())
    signature = signature.hexdigest()
    return signature


def login():
    # First login
    # url = "{}/accounts/authorize".format(domainip)
    url = '%s/accounts/authorize' % domainip

    signature = ""
    logger.debug(url)
	
    payload = {
        "username": username,
        "input_user": "",
        "ipAddress": "",
        "clientType": "WINPC"

	}
    headers = {
        'Connection': "close",
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
	
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        # Random Key MD5 Hashing
        TOKEN['randomkey'] = response.json()['randomKey']
        print('*******')
        print(response.json())
        print(response)

        TOKEN['signature'] = pass_encrypt(TOKEN['randomkey'])

    except Exception as e:
        print(e)

    # Second login
    payload_2 = {
        "userName": username,
        "randomKey": TOKEN['randomkey'],
        "mac": "",
        "encryptType": "MD5",
        "ipAddress": "",
        "signature": TOKEN['signature'],
        "clientType": "WINPC"
    }

    try:
        res = requests.post(url, data=json.dumps(payload_2), headers=headers)
        TOKEN["token"] = res.json().get('token')
        print('*******')
        print(res.json())
        print(res)

    except Exception as e:
        print(e)

def date_to_Asia(date):
    if type(date) is str:
        get_date_obj = parse(date)
        return get_date_obj.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
    else:
        return date.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))


def get_age_range(age):
    if 0 <= age <= 7:
        return 1
    elif 8 <= age <= 17:
        return 2
    elif 18 <= age <= 25:
        return 3
    elif 26 <= age <= 35:
        return 4
    elif 36 <= age <= 45:
        return 5
    elif 46 <= age <= 55:
        return 6
    elif 56 <= age:
        return 7
		

def create_query_string(c_timestamp, y_timestamp, chids, rec_num):
    return {
        "data": {
            "page": 1,
            "pageSize": rec_num,
            "glasses": "",
            "emotion": "",
            "search": "",
            "by": "",
            "repositoryId": "",
            "channelIds": chids,
            "beginTime": y_timestamp,
            "endTime": c_timestamp,
            "beginAge": "",
            "endAge": "",
            "gender": "",
            "similarity": "",
            "imageData": "",
            "personId": "",
            "personName": "",
            "personTypeIds": [],
            "searchFromClient": "true"
        }
    }


def get_registered_camera():
    cameras = []
    cameras_devices = {}
    response = table_fd_camera.scan(
        FilterExpression=Attr('id').lt(10)
	)

    items_found = response['Items']

    print(response)
    if len(items_found) > 0:
        for item in items_found:
            cameras.append("{}$1$0$0".format(item['device_id']))
            cameras_devices["{}$1$0$0".format(item['device_id'])] = item['id']
			
        return cameras, cameras_devices


def reportdaily():
    login()

    # get last hour data
    currentTime = datetime.now()
    c_timestamp = int(time.mktime(currentTime.timetuple()))
    yesterdayTime = datetime.now() - timedelta(hours=1)
    y_timestamp = int(time.mktime(yesterdayTime.timetuple()))
    records_num = 100000  # grep 100 rec from each camera every 10sec
    report_day(c_timestamp, y_timestamp, records_num)


def reportlive():
    login()

    # get last hour data
    currentTime = datetime.now()
    c_timestamp = int(time.mktime(currentTime.timetuple()))
    yesterdayTime = datetime.now() - timedelta(days=20)
    y_timestamp = int(time.mktime(yesterdayTime.timetuple()))
    records_num = 200000  # grep 100 rec from each camera every 10sec
    report_day(c_timestamp, y_timestamp, records_num)


def report_day(c_timestamp, y_timestamp, rec_num):
    # url = "http://192.168.0.2/admin/API/face/report/day/list"
    # url = http://192.168.0.2/admin/API/face/detection/record/feature

    url = "{}/face/detection/record/feature".format(domainip)
    channelIds, cameras_devices = get_registered_camera()
    payload = create_query_string(str(c_timestamp), str(y_timestamp), channelIds, rec_num)
    # querystring = {"nowTime": int(c_timestamp), "time": int(y_timestamp), "pageSize": "100000", "page": "1", "startTime": "",
    #                "endTime": "", "type": "0", "channelIds": ""}

    print(payload)

    headers = {
        'Content-Type': "application/json",
        'Connection': "keep-alive",
        'X-Subject-Token': TOKEN["token"],
        'cache-control': "no-cache",
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    dailyresultdict = []
    print("")
    print("")
    print(response.json())

    print(response)
    if 'data' in response.json():

        data = response.json().get('data').get('pageData')


        for item in data:
			
            response = table_fd.scan(
                FilterExpression='api_id =:val1',
                ExpressionAttributeValues={
                    ':val1': item['id']
                }
            )
        
            response_count = table_fd.scan(
                FilterExpression=Attr('id').gt(0)
            )
                
            count = response_count['Count'] + 1
		
            if response['Count'] == 0:
                this_id = item['id']
                this_timestamp = item['beginTime']
                this_camera_name = item['channelName']
                this_gender = item['gender']
                this_age = item['age']
                this_emotion = item['emotion']
                this_age_range = get_age_range(int(item['age']))

                #print(cameras_devices)
                this_camera_id = cameras_devices[item['channelId']]

                # insert into db

                table_fd.put_item(
                    Item={
                        'id': count,
                        'api_id': this_id,
                        'timestamp': this_timestamp,
                        'camera_id': this_camera_id,
                        'gender': this_gender,
                        'age': this_age,
                        'age_range': this_age_range,
                        'emotion': this_emotion,
                        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    ConditionExpression="attribute_not_exists(api_id)"
                )
                count = count + 1


def logic_func(event, context)
    reportdaily()

def lambda_handler(event, context):
    logic_func(event, context)
	
	
lambda_handler("","")
