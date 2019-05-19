import json
import boto3
import os
import time

dynamodb = boto3.resource('dynamodb') #, endpoint_url='http://localhost:8000')
table_fd = dynamodb.Table('face_demographics')
table_fd_record = dynamodb.Table('face_demographics_record')
table_fd_camera = dynamodb.Table('face_detection_camera')

class face_demographics():

    def __init__(self):
        self.data = {}
        self.age_distro = {
            "0-7": 0,
            "8-17": 0,
            "18-25": 0,
            "26-35": 0,
            "36-45": 0,
            "46-55": 0,
            "56+": 0
        }

        self.gender_distro = {
            "female": 0,
            "male": 0
        }

        self.emotion = {
            "smile": 0,
            "anger": 0,
            "sadness": 0,
            "disgust": 0,
            "fear": 0,
            "surprised": 0,
            "normal": 0,
            "laughs": 0,
            "happy": 0,
            "confused": 0,
            "screams": 0

        }

    def get_camera_by_venue(self, venueId):
        camera_ids = []

        response = table_fd_camera.scan(
            FilterExpression='venue_id =:val1',
            ExpressionAttributeValues={
				':val1': venueId
			}
		)
        print("response is here!!!")
        print(response)

        if response['Count'] > 0:
            for item in response["Items"]:
                camera_ids.append(item['id'])

        return camera_ids


    def get_age_range(self, age):
        if 0 <= age <= 7:
            return "0-7"
        elif 8 <= age <= 17:
            return "8-17"
        elif 18 <= age <= 25:
            return "18-25"
        elif 26 <= age <= 35:
            return "26-35"
        elif 36 <= age <= 45:
            return "36-45"
        elif 46 <= age <= 55:
            return "46-55"
        elif 56 <= age:
            return "56+"

    def commulitive_data(self, item):

        age_range = self.get_age_range(int(item['age']))

        self.age_distro[str(age_range)] += 1

        if item['gender'] == '2':
            self.gender_distro['female'] += 1

        if item['gender'] == '1':
            self.gender_distro['male'] += 1

        self.emotion['smile'] = self.emotion['smile'] + 1 if item['emotion'] == "0" else self.emotion['smile']
        self.emotion['anger'] = self.emotion['anger'] + 1 if item['emotion'] == "1" else self.emotion['anger']
        self.emotion['sadness'] = self.emotion['sadness'] + 1 if item['emotion'] == "2" else self.emotion[
            'sadness']
        self.emotion['disgust'] = self.emotion['disgust'] + 1 if item['emotion'] == "3" else self.emotion[
            'disgust']
        self.emotion['fear'] = self.emotion['fear'] + 1 if item['emotion'] == "4" else self.emotion['fear']
        self.emotion['surprised'] = self.emotion['surprised'] + 1 if item['emotion'] == "5" else self.emotion[
            'surprised']
        self.emotion['normal'] = self.emotion['normal'] + 1 if item['emotion'] == "6" else self.emotion['normal']
        self.emotion['laughs'] = self.emotion['laughs'] + 1 if item['emotion'] == "7" else self.emotion['laughs']
        self.emotion['happy'] = self.emotion['happy'] + 1 if item['emotion'] == "8" else self.emotion['happy']
        self.emotion['confused'] = self.emotion['confused'] + 1 if item['emotion'] == "9" else self.emotion['confused']
        self.emotion['screams'] = self.emotion['screams'] + 1 if item['emotion'] == "10" else self.emotion['screams']


    def get_summary_demographics(self, s_date, e_date, venue_id):

        cameras = self.get_camera_by_venue(venue_id)
        cameraList = []
		
        for i in cameras:
            cameraList.append(int(i))
        print(cameraList)

        response = table_fd.scan(
            FilterExpression='#ts between :val1 and :val2',
            ExpressionAttributeValues={
				':val1': int(s_date),
				':val2': int(e_date), 
			},
			ExpressionAttributeNames={
				"#ts": "timestamp"
			}
		)
		
        print("response is here!!!")
        print(response)
		
        # 0 - Smile
        # 1 - Anger
        # 2 - Sadness
        # 3 - Fear
        # 4 - Surprised
        # 5 - Normal
        if response['Count'] > 0:
            for item in response["Items"]:
                if item['camera_id'] in cameraList:
                    self.commulitive_data(item)

        self.data = {
            "age_distro": self.age_distro,
            "gender_distro": self.gender_distro,
            "emotion": self.emotion
        }

        return self.data

