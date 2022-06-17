from flask import Blueprint, request
from threading import Thread
import uuid, json, base64

from .http_requests import insert_log, confirm_reception, get_submission, get_document

http_requests = Blueprint('http_requests', __name__, url_prefix='/api/v1/http-requests')

@http_requests.post('/webhook')
def webhook():
  data = request.json

  # Confirm webhook reception
  event_id = data['event_id']
  Thread(target=confirm_reception, args=[event_id]).start()

  event_type = data['event_type']

  if event_type != 'submission_complete':
    return

  submission_id = data['submission_id']
  submission   = get_submission(submission_id)['submissions'][0]
  submission_status = submission['status']
  
  rejected_status = [2, 3, 5]

  if submission_status in rejected_status:
    return

  # Generate UUID for log
  identifier = uuid.uuid1()

  # Insert default values to db
  insert_log(1, 1, 1, identifier, None)

  # Update neccesary data
  metadata = json.dumps(data)

  # Insert log data with new status id
  insert_log(1, 1, 2, identifier, metadata)

  #-------------------------------- End Step 1 ------------------------------------#

  documents = submission['documents']
  documents_data = []

  for i in range(len(documents)):
    document_type = documents[i]['document_type'] 
    document_id   = documents[i]['document_id']
    documents_data.append({ 'document_type': document_type, 'document_id': document_id })

  for i in range(len(documents_data)):
    response      = get_document(submission_id, documents_data[i]['document_id'])
    document_type = response.headers['Content-Type'] 

    base64_content = f"data:{document_type};base64,{base64.b64encode(response.content).decode('utf-8')}"
    metadata       = json.dumps({ 'document_type': documents_data[i]['document_type'], 'document': base64_content })

    insert_log(1, 2, 3, identifier, metadata)

  return 'Successfully'

  # -------------------------------- End Step 2 ------------------------------------#

# API
# @http_requests.post('/app-link/send')
# def applink_send():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/app-link/send'
#   payload = {
#     'client_key':       os.environ.get('CLIENT_KEY'),
#     'access_key':       os.environ.get('ACCESS_KEY'),
#     'information_type': os.environ.get('INFORMATION_TYPE'),
#     'contact':          os.environ.get('CONTACT'),
#     'profile_id':       os.environ.get('PROFILE_ID')
#   }

#   response = requests.post(url, data=payload)

#   return response.json()

# @http_requests.post('/event/acknowledge')
# def event_acknowledge():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/event/acknowledge'
#   payload = {
#     'client_key': os.environ.get('CLIENT_KEY'),
#     'access_key': os.environ.get('ACCESS_KEY'),
#     'event_id':   os.environ.get('EVENT_ID')
#   }

#   response = requests.post(url, data=payload)

#   return response.json()

# @http_requests.post('/app-link/status')
# def applink_status():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/app-link/status'
#   payload = {
#     'client_key': os.environ.get('CLIENT_KEY'),
#     'access_key': os.environ.get('ACCESS_KEY'),
#     'uuid':       os.environ.get('UUID'),
#     'detailed_status': os.environ.get('DETAILED_STATUS')  
#   }

#   # ca29f492
#   # b57111cc
#   response = requests.post(url, data=payload).json()

#   if not 'submissions' in response or not len(response['submissions']):
#     return 'No existe submissions'

#   submissions = response['submissions']
#   submission_id = None

#   rejected_status = [2, 3, 5]
#   for i in range(len(submissions)):
#     try:
#       submission    = submissions[i] 
#       status        = submission['status']
#       document      = submission['documents']
#       submission_id = submission['submission_id']
    
#       if len(document) > 0:
#         if status in rejected_status:
#           return 'El documento tiene alertas'
#     except NameError:
#       return 'Internal error'

#   # Send correct response
#   return jsonify(submission_id)

# @http_requests.post('/submission/status')
# def submission_status():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/submission/status'
#   payload = {
#     'client_key':    os.environ.get('CLIENT_KEY'),
#     'access_key':    os.environ.get('ACCESS_KEY'),
#     'submission_id': "1875677",
#   }

#   response = requests.post(url, data=payload).json()

#   if not 'submissions' in response or not len(response['submissions']):
#     return 'No existe submissions'

#   submissions = response['submissions']
#   document_ids = []

#   rejected_status = [2, 3, 5]
#   for i in range(len(submissions)):
#     try:
#       submission = submissions[i] 
#       status     = submission['status']
#       documents  = submission['documents']

#       if status in rejected_status:
#         return 'El documento tiene alertas'

#       documents_length = len(documents)

#       if documents_length < 1:
#         return 'No hay documentos'

#       for document_index in range(documents_length):
#         document    = documents[document_index]
#         document_id = document['document_id']

#         if document_id:
#           document_ids.append(document_id)

#     except NameError:
#       return 'Internal error'

#     if len(document_ids) > 0:
#       # Send correct response
#       return jsonify(document_ids)

#   return jsonify(None)

# @http_requests.post('/submission/details')
# def submission_details():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/submission/details'
#   payload = {
#     'client_key':    os.environ.get('CLIENT_KEY'),
#     'access_key':    os.environ.get('ACCESS_KEY'),
#     'submission_id': "1875677",
#   }

#   response = requests.post(url, data=payload).json()

#   return response

# @http_requests.post('/submission/document')
# def submission_document():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/submission/document'
#   payload = {
#     'client_key':    os.environ.get('CLIENT_KEY'),
#     'access_key':    os.environ.get('ACCESS_KEY'),
#     'submission_id': "1875677",
#     'document_id': '3533856'
#   }

#   response = requests.post(url, data=payload)

#   return Response(response.content, headers={ 'Content-Type': 'image/jpeg' })

# @http_requests.post('/submission/cdd-report')
# def submission_ccdreport():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/submission/cdd-report'
#   payload = {
#     'client_key':    os.environ.get('CLIENT_KEY'),
#     'access_key':    os.environ.get('ACCESS_KEY'),
#     'submission_id': "1875677"
#     # 1875677
#   }

#   response = requests.post(url, data=payload)

#   return Response(response.content, headers={ 'Content-Type': 'application/pdf' })

# @http_requests.post('/')
# def submission_complete():
#   # Request neccesary data
#   url = 'https://client.id-pal.com/3.0.0/api/submission/complete'
#   payload = {
#     'client_key':    os.environ.get('CLIENT_KEY'),
#     'access_key':    os.environ.get('ACCESS_KEY'),
#     'id': "1875677" # submission_id
#     # 1875677
#   }
  
#   response = requests.post(url, data=payload).json()

#   return response
 