import mysql.connector
import socket
from datetime import datetime
host = socket.gethostname()
host_ip = socket.gethostbyname(host)


class MyCursor(object):
    def __init__(self):
        super(MyCursor, self).__init__()
        self.db = mysql.connector.connect(
            host='localhost',
            user='GymRespo',
            port='3306',
            passwd='1597530aqW*',
            database='gymsec'
        )
        self.mycursor = self.db.cursor()

# m = MyCursor()
# m.mycursor.execute("SELECT * FROM clients")
# # m.db.commit()
# f = m.mycursor.fetchall()
# for r in f:
#     print(r)
