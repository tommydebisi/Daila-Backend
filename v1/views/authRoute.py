from v1.views import daila
from flask import abort, jsonify, request, json
from validation.userValidation import validateEmail
from auth.authorize import AUTH

@daila.route('/register', methods=['POST'], strict_slashes=False)
def registerUser():
    """
        register users
    """
    # convert to mutable dict
    obj = dict(request.form)
    if not obj:
        abort(400)
    email = obj.get('email')
    if not validateEmail(email):
        abort(400)

    try:
        AUTH.registerUser(obj)
        return jsonify({ 'message': 'success' }), 202
    except ValueError:
        # user already exists
        abort(400)

@daila.route('/login', methods=['GET'], strict_slashes=False)
def loginUser():
    """
        login users and returns a token
        unique to each user
    """
    # to be safer, load data to json
    data = request.get_json()
    if not data:
        abort(400)

    email = data.get('email')
    if not validateEmail(email):
        abort(400)

    try:
        token = AUTH.loginUser(data)

        return jsonify(token=token), 200
    except ValueError:
        abort(400)
