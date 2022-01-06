from config.settings import VASPRO_API
import requests
import json

class sendSms:
    def __init__(self,phon_no,message):
        self.url = "https://sms.vaspro.co/v3/BulkSMS/api/create"
        self.phone_no =  phon_no
        self.message = message


    def send_sms(self):
        headers = {'content-type': 'application/json'}
        payload = json.dumps({
            "apiKey": VASPRO_API,
            "shortCode": "VasPro",
            "message": self.message,
            "recipient": str(self.phone_no),
            "callbackURL": "",
            "enqueue": 0
            })
        headers = {
            'Content-Type': 'application/json'
            }
        response = requests.request("POST", self.url, headers=headers, data=payload)

        return response.json()
