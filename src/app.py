import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get all family members
@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

# retrieve one member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    memberId = jackson_family.get_member(member_id)
    return jsonify(memberId), 200

# add new member
@app.route('/member', methods=['POST'])
def post_one_member():
    body_id = request.json.get("id")
    body_first_name = request.json.get("first_name")
    body_last_name = request.json.get("last_name")
    body_age = request.json.get("age")
    body_lucky_numbers = request.json.get("lucky_numbers")

    memberAdd = {
        "id": body_id or jackson_family._generateId(),
        "first_name": body_first_name,
        "last_name": body_last_name,
        "age": body_age,
        "lucky_numbers": body_lucky_numbers,
    }
    jackson_family.add_member(memberAdd)
    return jsonify(None), 200

# delete one member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_single_member(member_id):
    memberId = jackson_family.delete_member(member_id)
    return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
