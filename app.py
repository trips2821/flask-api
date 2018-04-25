#!/usr/bin/env python

import datetime

from flask import abort, request, jsonify, g

from libs.base import *
from models import User


#Auth function
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


#Health check
@app.route('/api', methods=['GET'])
def health_check():
    timestamp = {
    'status': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(timestamp), 200


#Register new user
@app.route('/api/user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'user already exists'}), 400

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201


#Login and get token
@app.route('/api/login', methods=['GET'])
@auth.login_required
def get_auth_token():
    token_exp = 6000
    token = g.user.generate_auth_token(token_exp)

    return jsonify({'token': token.decode('ascii'), 'duration': token_exp}), 200


#Must be logged in for this to work
@app.route('/api/test', methods=['GET'])
@auth.login_required
def test():
    return jsonify({'message': 'it worked!!'}), 200


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()

    app.run(host="0.0.0.0", port=int(app.config['PORT']), debug=True)
