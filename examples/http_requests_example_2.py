from flask import Blueprint, jsonify, request
from threading import Thread
import uuid, json, base64
from .http_requests import *

http_requests = Blueprint('http_requests', __name__, url_prefix='/api/v1/http-requests')

@http_requests.post('/webhook')
def webhook():
  # Webhook data
  data = request.json

  # Confirm webhook reception
  event_id = data['event_id']
  Thread(target=confirm_reception, args=[event_id]).start()
  
  event_type = data['event_type']

  # Process only completed webhook
  if event_type != 'cdd_complete':
    return

  ################################# HID ##########################################
  result = hid_create_user()

  error_code = result['error_code']

  if error_code != 0:
    return

  user_id          = result['user']['user_id']

  error_message    = result['error_message']
  custom_content   = result['user']['custom_content']
  user_status      = result['user']['status']
  user_created_at  = result['user']['created_at']
  user_modified_at = result['user']['modified_at']

  result = hid_add_user_credential(user_id, user_selfie['image_data'], user_selfie['image_type'])

  error_code = result['error_code']

  if error_code != 0:
    return


  # Seguimos...

    # Get submission status llamada API
      # Insert in SELECT * FROM idpal_submission_status;

    # Get submission detail
      # Insert in idpal_submission_detail

    # Insert datos en idpal_mobiles(Usar la info que viene de detail(get submission detail))
    
    # Ahora en documentos 
      # Insertar en documents main informacion del documento que viene de api detail y api status
      # Insertar documentos en idpal_documents(Pedir documento por documento e insertar)

  # Buscar primero esto: Select identity postgress sql

  credential_id       = result['credential']['credential_id']
  credential_modality = result['credential']['modality']

  biometric_modality  = result['extracted_data']['biometric_data']['modality']
  biometric_data      = result['extracted_data']['biometric_data']['data']
  biometric_datatype  = result['extracted_data']['biometric_data']['datatype']

  quality_score       = result['extracted_data']['quality']['quality_score']

  ############################### HID ############################################

  # Submission data
  submission_id = data['submission_id']
  submission    = get_submission(submission_id)['submissions'][0]
  submission_status = submission['status']
  
  # rejected_status = [2, 3, 5]

  # # Reject invalid process states
  # if submission_status in rejected_status:
  #   return

  # Generate UUID for the log
  identifier = uuid.uuid1()

  # status, step, event, identifier, metadata
  insert_log(1, 1, 1, identifier, None)

  # Set log metadata
  metadata = json.dumps(data)

  # status, step, event, identifier, metadata(event updated: 1 -> 2)
  insert_log(1, 1, 2, identifier, metadata)

  #-------------------------------- End of Step 1 ------------------------------------#

  # Client documents
  documents = submission['documents']
  documents_data = []

  user_selfie = {}

  for i in range(len(documents)):
    document_type = documents[i]['document_type'] 
    document_id   = documents[i]['document_id']
    documents_data.append({ 'document_type': document_type, 'document_id': document_id })

  # Get client documents and convert to base64, them insert to db
  for i in range(len(documents_data)):
    response      = get_document(submission_id, documents_data[i]['document_id'])
    document_type = response.headers['Content-Type']

    base64_image   = base64.b64encode(response.content).decode('utf-8')
    base64_content = f"data:{document_type};base64,{base64_image}"
    metadata       = json.dumps({ 'document_type': documents_data[i]['document_type'], 'document': base64_content })

    # status, step, event, identifier, metadata(step updated: 1 -> 3, event updated: 2 -> 3, metadata updated)
    insert_log(1, 2, 3, identifier, metadata)

    if documents_data[i]['document_type'] == 'selfie':
      user_selfie['image_data'] = base64_image
      user_selfie['image_type'] = document_type.split('/')[1].lower()

  # -------------------------------- End of Step 2 ------------------------------------#

  result = hid_create_user()

  error_message    = result['error_message']
  custom_content   = result['user']['custom_content']
  user_status      = result['user']['status']
  user_id          = result['user']['user_id']
  user_created_at  = result['user']['created_at']
  user_modified_at = result['user']['modified_at']

  if error_message:
    return

  result = hid_add_user_credential(user_id, user_selfie['image_data'], user_selfie['image_type'])

  credential_id       = result['credential']['credential_id']
  credential_modality = result['credential']['modality']

  biometric_modality  = result['extracted_data']['biometric_data']['modality']
  biometric_data      = result['extracted_data']['biometric_data']['data']
  biometric_datatype  = result['extracted_data']['biometric_data']['datatype']

  quality_score       = result['extracted_data']['quality']['quality_score']

  render = { 'user_id': user_id, 'credential_id': credential_id, 'credential_modality': credential_modality, 'biometric_modality': biometric_modality, 'biometric_data': biometric_data, 'quality_score': quality_score }

  idpal_uuid = data['uuid']
  insert_hid_user(idpal_uuid, user_id, custom_content, user_status, credential_id, biometric_modality, biometric_datatype, biometric_data, quality_score, user_created_at, user_modified_at) 

  return jsonify(render)

  # -------------------------------- End of Step 3 ------------------------------------#

  # IdpalUserID, HidUserId, CustomContent, Status, CredentialId, Modality, DataType, DataHfTemplate, QualityScore, UserCreatedAt, UserModifiedAt