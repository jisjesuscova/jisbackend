import requests

class DteClass:
    def get_total_quantity(user_inputs):

        if user_inputs['rol_id'] == 4 or user_inputs['rol_id'] == 5:
            user_inputs['rol_id'] = 1

        if user_inputs['rol_id'] == 3:
            user_inputs['rol_id'] = 4

        url = "https://jisparking.com/api/dte/receivable/"+ str(user_inputs['rol_id']) +"/"+ str(user_inputs['rut']) +"?api_token="+ str(user_inputs['api_token']) +""

        payload={}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        return response.text
    
    def get_total_amount(user_inputs):

        if user_inputs['rol_id'] == 4 or user_inputs['rol_id'] == 5:
            user_inputs['rol_id'] = 1

        if user_inputs['rol_id'] == 3:
            user_inputs['rol_id'] = 4
            
        url = "https://jisparking.com/api/dte/receivable/"+ str(user_inputs['rol_id']) +"/"+ str(user_inputs['rut']) +"?api_token="+ str(user_inputs['api_token']) +""

        payload={}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        return response.text
