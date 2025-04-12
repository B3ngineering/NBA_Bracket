from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API is working!"})