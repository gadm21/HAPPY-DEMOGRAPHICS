import mysql.connector


class face_demographics():

    def __init__(self):
        self.mydb, self.db_cursor = self.db_connection()
        self.data = {}
        self.age_distro = {
            "0-7": 0,
            "8-17": 0,
            "18-25": 0,
            "26-35": 0,
            "36-45": 0,
            "46-55": 0,
            "56+": 0,
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
        result = []
        self.db_cursor.execute(
            "select * from face_detection_camera where venue_id = {} ;".format(venueId)
        )
        result = self.db_cursor.fetchall()

        return result

    def db_connection(self):
        # # Connect to production database
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="tapwayabc123#",
            database="dahuadb_face",
        )

        # mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     port=0,
        #     passwd="tapway",
        #     database="dahuadb_face",
        # )
        db_cursor = mydb.cursor(buffered=True, dictionary=True)
        return mydb, db_cursor

    def get_age_range(self, age):
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
    self.db_cursor.execute(
        "select * from face_demographics where ventimestamp BETWEEN {} AND {} ;".format(s_date, e_date)
    )
    items_found = self.db_cursor.fetchall()
    # 0 - Smile
    # 1 - Anger
    # 2 - Sadness
    # 3 - Fear
    # 4 - Surprised
    # 5 - Normal
    if len(items_found) > 0:
        for item in items_found:
            self.commulitive_data(item)

    self.data = {
        "age_distro": self.age_distro,
        "gender_distro": self.gender_distro,
        "emotion": self.emotion
    }

    return self.data









