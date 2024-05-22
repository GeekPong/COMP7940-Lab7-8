# ChatGPT_HKBU.py
import configparser
import requests
import os

class HKBU_ChatGPT():
    def __init__(self,config_= './config.ini'):
        pass
        # if type(config_path) == str:
        # Lab8P2Step1 as below:
        # -----------------------------
        # self.config = configparser.ConfigParser()
        # self.config.read(config_path)
        # -----------------------------
        # Lab8P2Step1 as above:
        # elif type(self.config) == configparser.ConfigParser:
        #     self.config = config_path

    def submit(self,message):
        # print(self.config['CHATGPT']['MODELNAME'])
        conversation = [{"role": "user", "content": message}]
        # modifying following code from Lab8 Recording P2Step1
        url = ('https://chatgpt.hkbu.edu.hk/general/rest') + "/deployments/" + ('gpt-35-turbo') + "/chat/completions/?api-version=" + ('2024-02-15-preview')
        # modifying following code correspondingly
        headers = { 'Content-Type': 'application/json', 'api-key': (os.environ['ACCESS_TOKEN_CHATGPT']) }
        #The api-key reference to line 8 in part2.yaml
        #If your want to run in local machine, Plz run 'export ACCESS_TOKEN_CHATGPT=c813af90-2980-4c99-9bf5-8cf8e0eaa493' to define this in terminal.
        
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            print(response.text)
            return 'Error:', response
            
if __name__ == '__main__':
    ChatGPT_test = HKBU_ChatGPT()
    while True:
        user_input = input("Typing anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)