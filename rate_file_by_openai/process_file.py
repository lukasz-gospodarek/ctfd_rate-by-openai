"""
Extend the standard api to add several useful endpoints
    Challenges: Add special attempt and solve for the FileUploadChallenges
    Submissions: Add endpoint to get the status of file submissions
"""

import os, requests
from CTFd.plugins import bypass_csrf_protection
from flask_restx import Namespace
from flask import request
from CTFd.utils.user import get_current_user

script_namespace = Namespace(
    "scripts", description="Endpoint to post and view script uploads"
)

def read_file_content(file_path):
    with open(file_path, 'r',) as file:
        return file.read()

def process_file(rates_directory,file_path,user_id):

    if not os.path.exists(rates_directory):
        os.makedirs(rates_directory)

    if os.path.isfile(rates_directory+str(user_id)+".html"):
        with open(rates_directory+str(user_id)+".html", 'r') as file:
            content = file.read()
            return content
    else:
        url = "http://ctfd_openai_1:8888/upload"

        # Open the file in binary mode
        with open(file_path, "rb") as file:
            # Create a dictionary with the file data
            files = {"file": (file_path, file, "multipart/form-data")}
            
            # Send the POST request with the file
            response = requests.post(url, files=files)
            
            with open(rates_directory+str(user_id)+".html", 'w') as file:
                file.write(str(response.text).replace("\\n","")[1:-1])

            return str(response.text).replace("\\n","")[1:-1]

@bypass_csrf_protection
def upload_file():
    user = get_current_user()
    rates_directory = "/var/uploads/6a8605fb3aa6388173326d04b/"

    # if rate file already exist return it
    if os.path.isfile(rates_directory+str(user.id)+".html"):
        with open(rates_directory+str(user.id)+".html", 'r') as file:
            content = file.read()
            return content


    if 'file' not in request.files:
        return 'No file attached'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No file attached'
    if file:
        filename = file.filename
        patch=str("/tmp/")
        filepath = os.path.join(patch, filename)
        try:
            file.save(filepath)
            return str(process_file(rates_directory,filepath,user.id))
        except Exception as e:
            return str(e)
    
    return "OK"