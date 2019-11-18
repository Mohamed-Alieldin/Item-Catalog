import json

SECRETS_FILE = 'client_secrets.json'
CLIENT_ID = json.loads(open(SECRETS_FILE, 'r').read())['web']['client_id']