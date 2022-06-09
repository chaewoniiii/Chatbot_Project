class KakaoTemplate:
    def __init__(self):
        self.version = "2.0"

    def simpleTextComponent(self, text):
        return {
            "simpleText" : {"text": text}
        }

    def send_response(self, bot_resp):
        responseBody ={
            "version" : self.version,
            "template": {
                "outputs" : []
            }
        }

        if bot_resp['Answer'] is not None:
            responseBody['template']['outputs'].append(self.simpleTextComponent(bot_resp['Answer']))
        
        return responseBody
    