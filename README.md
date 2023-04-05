# API Server Fast API for revChatGPT

Use
[localhost:port/docs](localhost:8000/docs)
for docs endpoint.
# Querying

Querying a prompt

```bash
curl -X 'POST' \
  'http://localhost:8000' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Can you explain the current situation of Iran?"
}'
```

This will return some return a JSON that looks like this

```json
{
  "response": {
    "message": "Iran is a country located in middle east ...",
    "conversation_id": "conversation-id",
    "parent_id": "parent-id"
  }
}
```
This project has been designed to handle all of available parameters in original [revChatGPT](https://github.com/acheong08/ChatGPT) as an api and the models are designed to catch them all. In this version the only functional parameter is `prompt` but you can easily add rest of them by changing the input structure in 
``` 
api_prompt = body.prompt 
``` 
Also all of the real OpenAi API parameters for completion section has been captured so you can edit and enhance the prompt according to the input parameters for better responses.

# Setup

Enter your config file with your username, password and access token

```
{
  "email": "<example>",
  "password": "<example>",
  "access_token": "<example>"
}
```
You can limit certain domains' number of requests per day so you need to enter your domains in user_status.json

```
{
  "stuxan.ir": 3,
  "google.com": 4
}
```
** Note **: This method is using REFERER header which is not a reliable parameter for identifying user but it has a good certainty on user limit rate. If you are providing a paid subscription for your users you need to use a valid method to identify them (like api keys) so their credit can not be abused easily.

```
virtualenv env
source env/bin/activate

pip install -r requirements.txt

# Run locally
uvicorn main:app --reload

# Run in prod
python main.py

# Run in background (Linux)
nohup python main.py & 

# Run cron job
crontab -e
00 00 * * * python /path-to-script/credit_reset.py
```
# Credits

https://github.com/chitalian/revChatGPTServer
