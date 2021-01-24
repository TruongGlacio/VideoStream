import mysql.connector


class ServerDatabaseManager:
    def __init__(self) -> None:
        super().__init__()
        
    def CreatDatabase(self):
        print('creat database')
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@12345678"
        )

        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE mydatabase")
        pass
    def InsertToDataBase(self):
        pass
    def DeleteToDataBase(self):
        pass
    def SelectFromDatabase(self):
        """
        docstring
        """
        pass
if __name__ == "__main__":
    serverDatabaseManager = ServerDatabaseManager()
    serverDatabaseManager.CreatDatabase()