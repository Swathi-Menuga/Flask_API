import awsgi

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#Create a Flask app:

app = Flask(__name__)

#Configure the database:

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
db = SQLAlchemy(app)

#Create a model for the account:

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])  
def account(): 
    return 'Welcome to Flask API'

#Create the routes for CRUD operations:
#########Create Account (POST /accounts):############
@app.route('/accounts', methods=['POST'])
def create_account():
    try:
        data = request.get_json()
        new_account = Account(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
        db.session.add(new_account)
        db.session.commit()
        return jsonify({'message': 'Account created successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/accounts', methods=['GET'])
def get_all_accounts():
    accounts = Account.query.all()
    account_list = []
    for account in accounts:
        account_list.append({
            'id': account.id,
            'first_name': account.first_name,
            'last_name': account.last_name,
            'email': account.email,
            'password': account.password
        })
    return jsonify({'accounts': account_list})

#########Get Account by ID (GET /accounts/{id}):#############
@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    if account:
        return jsonify({'id': account.id, 'first_name': account.first_name, 'last_name': account.last_name, 'email': account.email, 'password': account.password})
    return jsonify({'message': 'Account not found'})

##########Update Account by ID (PUT /accounts/{id}):############
@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    if account:
        data = request.get_json()
        account.first_name = data['first_name']
        account.last_name = data['last_name']
        account.email = data['email']
        account.password = data['password']
        db.session.commit()
        return jsonify({'message': 'Account updated successfully!'})
    return jsonify({'message': 'Account not found'})

#############Delete Account by ID (DELETE /accounts/{id}):############
@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    if account:
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully!'})
    return jsonify({'message': 'Account not found'})


def lambda_handler(event, context):
    try:
        print("Event:", event)  # Log the entire event for debugging
        return awsgi.response(app, event, context, base64_content_types={"image/png"})
    except Exception as e:
        print("Error:", str(e))  # Log the error for debugging
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
#Run the Application:
if __name__ == '__main__':
    app.run(debug=True)


