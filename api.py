import json, requests, time

from requests.auth import HTTPDigestAuth
import urllib

#rmauldin internal
secret = "8b2c1a809f867a915022d6c745d1e72e"
token = "9830cb8f6d90acc4"

endpoint = 'https://api.matterport.com/api/models/graph'

query = {
	"query": '''
		query{
			model(id: "kEWwJzPfNoT") {
				mattertags {
					id
					label
					description
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

