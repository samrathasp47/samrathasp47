import oci
import json
import io
import logging
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from datetime import datetime
import ssl
import email.utils
from email.message import EmailMessage

def handler(ctx, data: io.BytesIO = None):
    funDataStr = data.read().decode('utf-8')

    # Convert the log data to json
    funData =  json.loads(funDataStr)   
    # Ensure the event is from the desired bucket
    #logging.getLogger().info(funData)
    #bucket_name = "sam"
    #if funData["resourceName"] != bucket_name:
       # return {"message": "Ignoring event from a different bucket"}
# Set up OCI configuration using resource principal
    signer = oci.auth.signers.get_resource_principals_signer()
    # Create Object Storage client
    object_storage_client = oci.object_storage.ObjectStorageClient({},signer=signer)

    # Extract object details from the event

    
    object_name = funData['data']['resourceName']
    namespace = funData['data']['additionalDetails']['namespace']
    bucket_name = funData['data']['additionalDetails']['bucketName']

    

    
    # Download the object
    #get_object_response = object_storage_client.get_object(namespace, bucket_name, object_name)
    #object_content = str(get_object_response.data.text)
    create_preauthenticated_request_response = object_storage_client.create_preauthenticated_request(
        namespace_name = namespace,
        bucket_name = bucket_name,
        create_preauthenticated_request_details=oci.object_storage.models.CreatePreauthenticatedRequestDetails(
            name = "prestorage",
            access_type = "ObjectRead",
            time_expires = datetime.strptime(
                "2024-06-05T04:25:22.344Z",
                "%Y-%m-%dT%H:%M:%S.%fZ"),
            object_name = object_name))
    #logging.getLogger().info(create_preauthenticated_request_response.data)
    logging.getLogger().info("created pre authenticated url")
    string = str(create_preauthenticated_request_response.data)
    #response = create_preauthenticated_request_response.data().decode('utf-8')
    url = json.loads(string)
    #temporary_url = f"https://objectstorage.{signer['region']}.oraclecloud.com/n/{namespace}/b/{bucket_name}/opc_p/{create_preauthenticated_request_response.id}/{create_preauthenticated_request_response.name}"
    logging.getLogger().info(url)
    temporary_url = f"{url['full_path']}"
    logging.getLogger().info(temporary_url)
# Get the data from response
    #print(get_preauthenticated_request_response.data)
    #url = str(get_create_preauthenticated_request_response.data.text)
    # Do something with the object content (e.g., print it)
    #logging.getLogger().info(object_content)
    #text_file = open(r'/tmp/Example.csv', 'w')
    # Set your email credentials
    sender_email = "samrathasp@sehna.cloud"
    sender_name = "Samratha S P"

# Set the recipient email address
    recipient_email = "samratha.s.p@oracle.com"
    USERNAME_SMTP = "ocid1.user.oc1..aaaaaaaasvsufxb2wnvzz57vf7tffevb35oldvcktmoj5rv64tzqi2v3btrq@ocid1.tenancy.oc1..aaaaaaaanneylhk3ibv2dmorxqgklcloydwnror5b3fs4ag7dlrbsiwkjdea.hl.com"
    password_smtp = "Vpc]hiq-b)hzW4;_1wm7"
    HOST = "smtp.email.us-ashburn-1.oci.oraclecloud.com"
    PORT = 587

# Create the email content
    subject = "Cost Usage Report"
    body = temporary_url

    message = EmailMessage()
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = recipient_email
    message['Subject'] = subject
    message.set_content(body)
    try: 
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls(context=ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None))
        server.ehlo()
        server.login(USERNAME_SMTP, password_smtp)
        logging.getLogger().info("SMTP server logged in")
        server.sendmail(sender_email, recipient_email, message.as_string())
        #server.send_message(message)
        server.close()
    except Exception as e:
        logging.getLogger().info(f"Error: {e}")
    else:
        logging.getLogger().info('Email sent successfully!')
