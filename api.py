import json, requests, time

from requests.auth import HTTPDigestAuth
import urllib

#rmauldin internal
secret = "8b2c1a809f867a915022d6c745d1e72e"
token = "9830cb8f6d90acc4"

endpoint = 'https://api.matterport.com/api/models/graph'

hazards = {
	"Electrical outlets": ["HIGH RISK"
	"Exposed wires": 
	"Stairs": ["HIGH RISK"
	"Appliances": 
	"Bathrooms": 
	"Chemicals": 
	"Doors": 
	"Furniture": "LOW RISK"
	"Fireplaces": []
	"Small objects": ["HIGH RISK"
	"Sharp objects": 
	"Recalled Item":
	"Windows":
}

def risk_assign(tagLabel, tagID, position){
	if tagLabel == "Appliances":
		if (position.z > ):
	elif tagLabel == "Chemicals":
	
	elif tagLabel == "Small objects":
	
	elif tagLabel == "Sharp objects":
	
	elif tagLabel == "Windows":
	
	else:
		return #the specific hazard's risk
	
		
}

def mitigations(tagLabel, tagID, position){
	if (tagLabel == 
	
}


query = {
	"query": '''
		query{
			model(id: "kEWwJzPfNoT") {
				mattertags {
					id
					label
					description
					position
				}
			}

		} 
	'''

}

auth = (token, secret)
headers = {'content-type': 'application/json', 'accept': 'gzip'}

r = requests.post(endpoint, json=query, auth=auth, headers=headers)
print("DATA LEN:")
print(len(r.json()['data']['model']['mattertags']))
print("DATA:")
print(r.json()['data']['model']['mattertags'])

mutation{
	patchMattertag(
		#change tag color
		#in title, add risk level in brackets
		#in description, add mitigations
	
}

