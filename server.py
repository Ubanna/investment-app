from flask import Flask, request, jsonify, make_response
import main
from data import inv_class
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

@app.route('/api/user_risk_profile', methods=['GET', 'POST'])
def user_risk_profile():
    try:
        assets = request.json["assets"]

        response = jsonify({
        'profile': main.getCategory(assets, inv_class)
        })

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except:
        response = make_response("The request is invalid", 400)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/api/temp_user', methods=['GET'])
def temp_user():
    response = jsonify({
        'user': main.getUsers()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print('Starting Python Flask Server for Investment App')
    app.run(debug=True)