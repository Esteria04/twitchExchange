from flask import Flask
from flask_mysqldb import MySQL
from flask_restful import Resource, Api, reqparse
from dotenv import load_dotenv
import os

# settings
app = Flask(__name__)
api = Api(app)
load_dotenv()
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
mysql = MySQL(app)

class UserData(Resource):
    # 유저 최초 등록
    def post(self):
        parser = reqparse.RequestParser()
        cursor = mysql.connection.cursor()
        parser.add_argument('nickname', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        nickname = args['nickname']
        password = args['password']
        cursor.execute(f"INSERT into userData (nickname, password) values ('{nickname}','{password}')")
        mysql.connection.commit()
        cursor.close()

    # 유저 정보 조회
    def get(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM userData")
        userDetails = cursor.fetchall()
        users = dict()
        for row in userDetails:
            Id = row[0]
            Nickname = row[1]
            Password = row[2]
            RefreshDate = row[3]
            Point = row[4]
            user = {
                'id': Id,
                'nickname': Nickname,
                'password': Password,
                'refresh-date': str(RefreshDate),
                'point': Point
            }
            users[user['nickname']] = user
        return users
api.add_resource(UserData, '/users')

class PointsData(Resource):
    # 포인트 업데이트
    def patch(self, nickname):
        parser = reqparse.RequestParser()
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT nickname, point FROM userData WHERE nickname='{nickname}'")
        pointsDetails = cursor.fetchall()
        point = pointsDetails[0][1]
        parser.add_argument('newPoint', type=int)
        args = parser.parse_args()
        newPoint = args['newPoint']
        cursor.execute(f"UPDATE userData SET point='{point + newPoint}' WHERE nickname='{nickname}'")
        mysql.connection.commit()
        cursor.close()
api.add_resource(PointsData, '/points/<string:nickname>')

if __name__ == '__main__':
    app.run(debug=True)