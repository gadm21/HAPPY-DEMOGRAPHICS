
import mysql.connector

class face_demographics():

    def __init__(self):
        self.mydb,  self.db_cursor = self.db_connection()
        self.data = {}
        self.age_distro = {
            "0-14": 0,
            "15-17": 0,
            "18-21": 0,
            "22-29": 0,
            "30-49": 0,
            "50+": 0
        }

        self.gender_distro = {
            "female": 0,
            "male": 0
        }

        self.emotion = {
            "smile": 0,
            "anger": 0,
            "sadness": 0,
            "fear": 0,
            "surprised": 0,
            "normal": 0
        }

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
        db_cursor = mydb.cursor(buffered=True,dictionary=True)
        return mydb, db_cursor

    def commulitive_data(self, item):
        print(item)
        self.age_distro[str(item['age_range'])] += 1

        if item['gender'] == '2' :
            self.gender_distro['female'] += 1

        if item['gender'] == '1' :
            self.gender_distro['male'] += 1

        self.emotion[int(item['emotion'])] += 1


        #     self.emotion['anger'] = self.emotion['anger'] + 1 if self.emotion['anger'] == 1 else self.emotion['anger']
        # self.emotion['sadness'] = self.emotion['sadness'] + 1 if self.emotion['sadness'] == 2 else self.emotion[
        #     'sadness']
        # self.emotion['fear'] = self.emotion['fear'] + 1 if self.emotion['fear'] == 3 else self.emotion['fear']
        # self.emotion['surprised'] = self.emotion['surprised'] + 1 if self.emotion['surprised'] == 4 else self.emotion[
        #     'surprised']
        # self.emotion['normal'] = self.emotion['normal'] + 1 if self.emotion['normal'] == 5 else self.emotion['normal']

    def get_summary_demographics(self, s_date, e_date):
        self.db_cursor.execute(
            "select * from face_demographics where timestamp BETWEEN {} AND {} ;".format(s_date, e_date)
        )
        items_found = self.db_cursor.fetchall()
        # 0 - Smile
        # 1 - Anger
        # 2 - Sadness
        # 4 - Fear
        # 5 - Surprised
        # 6 - Normal
        if len(items_found) > 0 :
            for item in items_found:
                self.commulitive_data(item)


        self.data = {
            "age_distro": self.age_distro,
            "gender_distro": self.gender_distro,
            "emotion": self.emotion
        }


        return self.data









