import datetime
import os
import jwt
import json
from flask import request, jsonify, Flask
from jwt.exceptions import DecodeError, ExpiredSignatureError

app = Flask(__name__)

TOKEN_EXPIRATION = datetime.timedelta(hours=2)
SECRET_KEY = "eHbQVVyingS"


# @app.before_request
# def before_request():
#     if request.path == '/api/login' or request.path == '/api/register' or request.method.lower() == 'options':
#         return
#
#     token = request.headers.get('Authorization')
#
#     if not token:
#         return jsonify({'message': 'Token is missing!'}), 403
#     try:
#         _ = jwt.decode(token, SECRET_KEY)
#     except DecodeError:
#         return jsonify({'message': 'Token is invalid!'}), 403
#     except ExpiredSignatureError:
#         return jsonify({'message': 'Token is expired!'}), 403


@app.route('/api/register', methods=['POST'])
def register():
    with open('user.json', "r") as file:
        s = ''.join(file.readlines())
        data = json.loads(s)
    nu = request.get_json()
    new_user = nu
    new_user["best_score"] = 0
    data.append(new_user)
    with open('user.json', "w") as file:
        json.dump(data, file)
    token = jwt.encode(nu, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token}), 200


@app.route('/api/login', methods=['POST'])
def login():
    user_data = request.get_json()
    with open('user.json', "r") as file:
        s = ''.join(file.readlines())
        data = json.loads(s)
        for i in data:
            if i["username"] == user_data["username"]:
                if i["password"] == user_data["password"]:
                    data = {'username': user_data["username"], 'user_agent': request.user_agent.string,
                            'ip_address': request.remote_addr}
                    token = jwt.encode(data, SECRET_KEY, algorithm='HS256').decode('utf-8')
                    return jsonify({'token': token}), 200
                    #
                else:
                    return "Wrong password", 403
        return 'User does not exist', 404

# @app.route('/api/stats', methods=['GET'])
# def get_user():
#     token = request.headers.get('Authorization')
#     data = jwt.decode(token, SECRET_KEY)
#
#     user = User.query.filter_by(username=data['username']).first()
#     return user.get_stats()


if __name__ == '__main__':
    app.run(debug=True)