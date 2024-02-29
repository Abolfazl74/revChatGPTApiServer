from subprocess import Popen
from typing import Optional
from revChatGPT.V1 import Chatbot
from fastapi import FastAPI, Response, status, Request
import json
from urllib.parse import urlparse

import uvicorn


#app = FastAPI()
app = FastAPI(docs_url=None, redoc_url=None)

from pydantic import BaseModel

class MessageItems(BaseModel):
    role: Optional[str]
    content: str

class Item(BaseModel):
    model: Optional[str]
    #messages: list[MessageItems]
    prompt: str
    max_tokens: Optional[str]
    temperature: Optional[str]
    top_p: Optional[str]
    n: Optional[str]
    stream: Optional[str]
    frequency_penalty: Optional[str]
    presence_penalty: Optional[str]
    best_of: Optional[str]
    credit_status: Optional[str]
    
def get_available_token(access_token_usage_limit):
    with open("tokens_status.json", "r+") as g:
        tokens_status = json.load(g)
        for access_token in tokens_status:
            if tokens_status[access_token] < access_token_usage_limit:
                return access_token
    return False

with open("config.json", "r") as f:
    chatbot_config = json.load(f)
chatbot = Chatbot(config=chatbot_config)
@app.post("/")
async def read_root(request: Request, body: Item, response: Response):
    
    usage_limit = 15
    access_token_usage_limit = 50
    using_token_name = "access_token"
    
    http_referer = urlparse(request.headers.get('REFERER')).netloc
    with open("users_status.json", "r+") as g:
        users_status = json.load(g)
        if http_referer in users_status:
            if(body.credit_status):
                return {
                    "credit": users_status[http_referer]
                }   
            if int(users_status[http_referer]) < usage_limit:  
                users_status[http_referer] = int(users_status[http_referer]) + 1
                g.seek(0)  # rewind
                json.dump(users_status, g)
                g.truncate()
            else:
                return {
                    "id": "stuxan-ashiyan3@gmail.com",
                    "object": "text_completion",
                    "created": 1589478378,
                    "model": "text-davinci-003",
                    "choices": [
                        {
                        "text": "\n\متاسفانه اعتبار روزانه شما به اتمام رسیده است",
                        "index": 0,
                        "logprobs": "null",
                        "finish_reason": "length"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 5,
                        "completion_tokens": 7,
                        "total_tokens": 12
                    }
                }
        else:
            return {
                "id": "stuxan-ashiyan3@gmail.com",
                "object": "text_completion",
                "created": 1589478378,
                "model": "text-davinci-003",
                "choices": [
                    {
                    "text": "\n\nحساب کاربری شما یافت نشد",
                    "index": 0,
                    "logprobs": "null",
                    "finish_reason": "length"
                    }
                ],
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 7,
                    "total_tokens": 12
                }
            }   
    
    # api_prompt = body.messages[0].content
    api_prompt = body.prompt
    
    with open("tokens_status.json", "r+") as g:
        tokens_status = json.load(g)
        if tokens_status[using_token_name] >= access_token_usage_limit:
            using_token_name = get_available_token(access_token_usage_limit)
            if(using_token_name):
                with open("alt_access_tokens.json", "r") as f:
                    alt_access_tokens = json.load(f)
                chatbot.set_access_token(alt_access_tokens[using_token_name])
            else:
                return {
                    "id": "stuxan-ashiyan3@gmail.com",
                    "object": "text_completion",
                    "created": 1589478378,
                    "model": "text-davinci-003",
                    "choices": [
                        {
                        "text": "\n\متاسفانه سرویس به سقف محدودیت ساعتی رسیده است. لطفا دقایقی دیگر مجددا تلاش نمایید.",
                        "index": 0,
                        "logprobs": "null",
                        "finish_reason": "length"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 5,
                        "completion_tokens": 7,
                        "total_tokens": 12
                    }
                }
        tokens_status[using_token_name] = int(tokens_status[using_token_name]) + 1
        g.seek(0)  # rewind
        json.dump(tokens_status, g)
        g.truncate()
                
    
    result = ""
    
    try:
        for data in chatbot.ask(api_prompt):
            result = data["message"]
        if result:
            return {
                "id": "stuxan-ashiyan3@gmail.com",
                "object": "text_completion",
                "created": 1589478378,
                "model": "text-davinci-003",
                "choices": [
                    {
                    "text": result,
                    "index": 0,
                    "logprobs": "null",
                    "finish_reason": "length"
                    }
                ],
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 7,
                    "total_tokens": 12
                }
            }
        else:
            raise Exception("No response:")
    except Exception as e:
        chatbot.set_access_token(chatbot_config["access_token"])
        try: 
            for data in chatbot.ask(api_prompt):
                result = data["message"]
            if result:
                return {
                    "id": "stuxan-ashiyan3@gmail.com",
                    "object": "text_completion",
                    "created": 1589478378,
                    "model": "text-davinci-003",
                    "choices": [
                        {
                        "text": result,
                        "index": 0,
                        "logprobs": "null",
                        "finish_reason": "length"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 5,
                        "completion_tokens": 7,
                        "total_tokens": 12
                    }
                }
            else:
                raise Exception("No response")
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"response": str(e)}


if __name__ == '__main__':
    #Popen(['python', '-m', 'https_redirect'])
    uvicorn.run(
        'main:app', port=443, host='0.0.0.0',
        reload=True, reload_dirs=['html_files'], reload_includes=['*.json'], 
        ssl_keyfile='/etc/letsencrypt/live/my_domain/privkey.pem', #replace my_domain with your endpoint domain. example : /etc/letsencrypt/live/sv1.stuxan.top/privkey.pem
        ssl_certfile='/etc/letsencrypt/live/my_domain/fullchain.pem') #replace my_domain with your endpoint domain. example : /etc/letsencrypt/live/sv1.stuxan.top/fullchain.pem