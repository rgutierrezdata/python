from routes.database.connection import database, connection, idpal_credentials
from unix_time import *
import requests

requests = requests.Session()
requests.headers.update({
  'Connection':    'keep-alive',
  'Accept':        'application/json'
})

def get_access_token(client_key, client_id, access_key, refresh_token, environment, version):
  url     = f"{environment}/{version}/api/getAccessToken"
  payload = { 'client_key': client_key, 'client_id': client_id, 'access_key': access_key, 'refresh_token': refresh_token }
  response = requests.post(url, payload).json()
  
  return response

def idpal_config():
  query  = database.select(idpal_credentials)
  result = connection.execute(query).fetchone()

  return result

def update_idpal_credentials(credentials_id, token_type, expires_in, access_token, refresh_token, client_id):
  query = database.update(idpal_credentials).where(idpal_credentials.c.IdpalCredentialsID == credentials_id).values(TokenType = token_type, ExpiresIn = expires_in, Token = access_token, RefreshToken = refresh_token, ClientID = client_id)
  connection.execute(query)

def idpal_access_token():
  result = dict(idpal_config())

  # config data
  client_key     = result['ClientKey']
  access_key     = result['AccessKey']
  token_type     = result['TokenType']
  created_at     = result['CreatedAt']
  expires_in     = result['ExpiresIn']
  access_token   = result['Token']

  token = f'{token_type} ' # The space is important!

  # token time validation logic
  now = ts_now() 
  elapse_time    = now - created_at
  remaining_time = (expires_in * 1000) - elapse_time
  # elapse_hour    = elapse_time / 3600000
  remaining_hour = int(remaining_time / 3600000) 

  if remaining_hour < 23:
    client_id      = result['ClientID']
    credentials_id = result['IdpalCredentialsID']
    refresh_token  = result['RefreshToken']
    environment    = result['Environment']
    version        = result['Version']

    response = get_access_token(client_key, client_id, access_key, refresh_token, environment, version)

    token_type    = response['token_type']
    expires_in    = response['expires_in']
    access_token  = response['access_token']
    refresh_token = response['refresh_token']
    client_id     = response['client_id']

    update_idpal_credentials(credentials_id, token_type, expires_in, access_token, refresh_token, client_id)

  return print({ 'client_key': client_key, 'access_key': access_key, 'Authorization': token + access_token }) 

idpal_access_token()