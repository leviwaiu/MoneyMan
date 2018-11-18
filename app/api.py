import requests
import json
apiKey = 'bfae986372a1b6dde456e44b4cad2c38'

def getAccount(customerID, accountID):
    URL ="http://api.reimaginebanking.com/"
    if accountID =="":
        URL += "customers/{}/accounts?key={}".format(customerID, apiKey)
    elif customerID == "":
        URL += "accounts/{}?key={}".format(accountID, apiKey)
    else:
        URL += "customers/{}/accounts/{}?key={}".format(customerID, accountID, apiKey)
        
        
    PARAMS = {}
    req = requests.get(url = URL, params = PARAMS)

    accountData = req.json()
    return accountData

def getCustomerList():
    URL = "http://api.reimaginebanking.com/customers?key={}".format(apiKey)
    PARAMS = {}
    req = requests.get(url = URL, params = PARAMS)
    customerData = req.json()
    return customerData

def wriieAccount(customerID, accountID, payload):
    URL = "http://api.reimaginebanking.com/"
    if accountID == "":
        URL += "customers/{}/accounts?key={}".format(customerID, apiKey)
    elif customerID == "":
        URL += "accounts/{}?key={}".format(customerID, apiKey)
     
    response = requests.put(URL,
                            data = json.dumps(payload),
                            headers={'content-type':'application/json'}
                            )
    if response.status_code == 201:
        print('account created')
