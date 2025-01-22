from flask import Flask, request, jsonify
import hashlib
app = Flask(__name__)
@app.get('/')
def read_root():
    return {"message": "hello world"}
@app.route('/validate-md5-password', methods=['POST'])
def validate_password():
    try:
        # Parse the request JSON
        request_data = request.get_json()
        # Extract provided password and stored hash from the request
        provided_password = request_data['data']['context']['password']
        stored_hash = request_data['data']['context']['userProfile']['legacyPasswordHash']
        # Compute MD5 hash of the provided password
        computed_hash = md5_hash(provided_password)
        # Compare hashes
        if stored_hash and stored_hash == computed_hash:
            # Password is verified
            return jsonify(create_response("VERIFIED"))
        else:
            # Password is not verified
            return jsonify(create_response("UNVERIFIED"))
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Internal Server Error", 500
def md5_hash(input_str):
    # Generate MD5 hash of the input string
    md5 = hashlib.md5()
    md5.update(input_str.encode('utf-8'))
    return md5.hexdigest()
def create_response(credential_status):
    # Create response in the required format
    return {
        "commands": [
            {
                "type": "com.okta.action.update",
                "value": {
                    "credential": credential_status
                }
            }
        ]
    }
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)