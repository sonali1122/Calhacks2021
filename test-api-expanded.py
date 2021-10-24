
import json, requests, time

from requests.auth import HTTPDigestAuth
import urllib

#rmauldin internal
secret = "8b2c1a809f867a915022d6c745d1e72e"
token = "9830cb8f6d90acc4"

endpoint = 'https://api.matterport.com/api/models/graph'

#ID of the model (our study lounge scan)
mid: "kEWwJzPfNoT"

#dictionary - key: hazards, value: possible risk level 
hazards = {
	"Electrical Outlet": None,
	"Exposed Wires": None,
	"Stairs": "HIGH RISK",
	"Appliances": None,
	"Bathrooms": "LOW RISK",
	"Chemicals": None,
	"Door": "MEDIUM RISK",
	"Furniture": "LOW RISK" ,
	"Fireplaces": "HIGH RISK",
	"Small objects": None,
	"Sharp objects": None,
	"Recalled Item": "HIGH RISK",
	"Windows": None
}

#dictionary - key: hazards, value: mitigational advice on how to handle the risk
hazardMitigations = {
	"Electrical Outlet": "Electrical outlets can give children electrical shocks. Keep outlets covered.",
	"Exposed Wires": "Exposed wires can give children electrical shocks. Keep exposed wires out of reach.",
	"Stairs": "Block access to stairs to keep children from falling down them and getting hurt.",
	"Appliances": "Many appliances (ex: kitchen appliances, washing machines, freezers) can hurst children. Keep these appliances blocked or out of reach.",
	"Bathrooms": "Ideally close/lock bathroom doors or keep hazardous items within the bathroom out of reach.",
	"Chemicals": "Children may ingest harmful chemicals. Keep all chemical locked away or out of reach.",
	"Door": "Children may open doors on their own or get hit if someone on the other side opens the door. Lock doors to unsafe places and make sure children are not near the door before open it.",
	"Furniture": "Children may bump into furniture. Move sharp or easily breakable furniture out of the way",
	"Fireplaces": "Children may approach fireplaces, and get hurt by falling or getting burned if there is a fire. Keep children away from live fires and even when there is no fire, block access to the fireplace to avoid injury",
	"Small objects": "Children may injest/choke on small objects. Keep small objects out of reach",
	"Sharp objects": "Children may hurt themselves with sharp objects (ex: knives, scissors, utensils, tacks). Keep sharp objects out of reach.",
	"Recalled Item": "This item has been recalled. Remove it from the area to prevent children from getting hurt.",
	"Windows": "Children may open or climb up to windows amd may falling out of a window. Make sure windows are locked or blocked to prevent children from accessing them."
}

#List of hazards where risk level depends on position (height)
varRiskHazards = ["Electrical Outlet", "Exposed Wires", "Appliances", 
	"Chemicals", "Small objects", "Sharp objects", "Windows"]

'''
risk_assign: takes in the tagLabel and position (height) and generates the associated risk
if the hazard is identified to have variable risk based on position, we assign a risk based on this scheme:
	- within 2 feet = HIGH RISK
	- between 2 to 4 feet = MEDIUM RISK
	- between 4 to 5 fett = LOW RISK
	- above 5 feet = NEGLIGIBLE RISK
If the hazard does not depend on position, it gets assigned the definied risk level
If the hazard is not in the list of hazards, it has NEGLIGIBLE RISK
'''
def risk_assign(tagLabel, zposition):
	if tagLabel in hazards.keys():

		if tagLabel in varRiskHazards:
			# run a var risk assignment algorithm 
			risk = "HIGH RISK"
			if zposition > 1.5:
				risk = "NEGLIGIBLE RISK"
			elif zposition > 1.25:
				risk = "LOW RISK"
			elif zposition > 0.9:
				risk = "MEDIUM RISK"

			return risk

		else:
			# get var risk directly from hazards dict
			return hazards[tagLabel]

	else: # not in hazards list
		return "NEGLIGIBLE RISK"

#function that returns advice based on the tagLabel hazard
def mitigations(tagLabel):
	mitigation_str = ""
	if tagLabel in hazards.keys():
		mitigation_str += "This is a child hazard.\n"

		if tagLabel in varRiskHazards():
			#add: this object should be moved above a height out of reach or locked
			mitigation_str += hazardMitigations[tagLabel] + "\n"
			mitigation_str += "Advice: " + "This object is best kept out of reach of children. This object should be moved above a height of 5 feet for low risk of injury.\n"
	else:
		mitigation_str += "This is not a child hazard.\n"

#function that assigns color based on risk level
def color_assign(riskLevel):
	if riskLevel == "NEGLIGIBLE RISK": # green
		return hex(0x00FF00)
	if riskLevel == "LOW RISK": # yellow
		return hex(0xFF8C00)
	if riskLevel == "MEDIUM RISK": # orange
		return hex(0xFFFF00)
	if riskLevel == "HIGH RISK": # red
		return hex(0xFF0000)
	

#query to obtain Mattertag data from the model
query = {
	"query": '''
		query{
			model(id: "kEWwJzPfNoT") {
				mattertags {
					id
					label
					description
					position{z}
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
print("this should get door descrip")
print(r.json()['data']['model']['mattertags'][0]['description'])
string = "test"
print(string + " added")



tagList = r.json()['data']['model']['mattertags']

# adding information and classification to each tag
for tag in tagList:
	print(tag['label'])
	riskLevel = risk_assign(tag['label'], tag['position']['z'])
	mutation = {
		"mutation": '''
			mutation{
				patchMattertag(
					modelId: mid
					mattertagId: tag['id']
					patch: {
						label: riskLevel
					}
				){
					id
				}
			}

		'''
	}

	m = requests.post(endpoint, json=mutation, auth=auth, headers=headers)





	'''
	mutation{
		patchMattertag(
			modelId: mid
			mattertagId: tag['id']
			patch: {
				riskLevel = risk_assign(tag['label'], tag['position']['z'])
				label: label + " [" + riskLevel + "]"
				#description: description + "\n" + mitigations(tag['label'])
				#color: color_assign(riskLevel)
			}
		){
			id
		}
	}
	'''


