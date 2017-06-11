class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "169.254.10.11",
            "user": "root",
            "passwd": "badmin",
            "db": "docam"
        }
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getMediaFromDatabase(self):
        sqlQuery = "SELECT * FROM media"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getRingtonesFromDatabase(self):
        sqlQuery = "SELECT * FROM ringtones"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    # def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
    #     sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
    #     sqlCommand = sqlQuery.format(param1=voorwaarde)
    #
    #     self.__cursor.execute(sqlCommand)
    #     result = self.__cursor.fetchall()
    #     self.__cursor.close()
    #     return result

    def addMedia(self, value1, value2, value3):
        sqlQuery = "INSERT INTO media (filename, date, filesize, doorbell) VALUES ('{param1}',now(),{param2},{param3})"
        sqlCommand = sqlQuery.format(param1=value1, param2=value2, param3=value3)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def addRingtone(self, value1, value2):
        sqlQuery = "INSERT INTO ringtones (name, filename, creation_date) VALUES ('{param1}','{param2}',now())"
        sqlCommand = sqlQuery.format(param1=value1, param2=value2)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()
