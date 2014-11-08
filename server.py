# -----------------------------------------------------------------------------------------
# SBS - Stub Brand Server
# implemented in Flask (Python MicroFramework) and MongoDB
# -----------------------------------------------------------------------------------------

from flask import Flask, jsonify, make_response
from flask.ext.pymongo import PyMongo
import re

# Initialise Flask App
app = Flask(__name__)

# Connect to Mongo
app.config['MONGO_DBNAME'] = 'dealers'
mongo = PyMongo(app)

# -----------------------------------------------------------------------------------------
# API Routes

# @ /
# Introduce API
@app.route('/')
def intro():
	return jsonify({'whoami' : 'I am the REST API for GetBrand'})
	
# @ /dealers
# Return a list of available DealerIDs
@app.route('/dealers')
def list_dealers():
	dealers = mongo.db.brands.find({}, {'DealerID': True, '_id': False})
	dids = [r['DealerID'] for r in dealers]
	return jsonify({'DealerIDs' : dids})
	
# @ /brand/<FQDN> or /brand/<DealerID>
# Return brand for given FQDN or Dealer ID, or an error message if it's not found
@app.route('/brand/<ID>')
def get_brand(ID):
	if re.match(r'^\d+$', ID):
		brand = mongo.db.brands.find_one_or_404({'DealerID': ID}, {'_id': False})
	else:
		brand = mongo.db.brands.find_one_or_404({'FQDN': ID}, {'_id': False})
	return jsonify(brand)
        
#-----------------------------------------------------------------------------------------
# Listen for incoming HTTP requests on Port 5000
if __name__ == '__main__':
    app.run(debug=True)