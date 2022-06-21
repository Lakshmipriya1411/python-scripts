
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    load_dotenv()
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Upload the file
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(file_name, bucket, object_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
import oci
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
# Set up config
config = oci.config.from_file("~\.oci\config.txt","ADMIN_USER")
# Create a service client
identity = oci.identity.IdentityClient(config)
# Get the current user
#user = identity.get_user(config["user"]).data
#print(user)

import oci
import os
				
			
#reporting_namespace = 'ax8hkeiizrq6'
reporting_namespace = 'bling'
                               				
# Download all usage and cost files. You can comment out based on the specific need:
prefix_file = ""                     #  For cost and usage files
#prefix_file = "reports/cost-csv"   #  For cost
#prefix_file = "reports/usage-csv"  #  For usage
				
# Update these values
destintation_path = 'downloaded_reports'
				
# Make a directory to receive reports
if not os.path.exists(destintation_path):
    os.mkdir(destintation_path)
				
# Get the list of reports
config = oci.config.from_file("~\.oci\config.txt","ADMIN_USER")
#reporting_bucket = "bucket1"
reporting_bucket = config['tenancy']
object_storage = oci.object_storage.ObjectStorageClient(config)
report_bucket_objects = object_storage.list_objects(reporting_namespace, reporting_bucket, prefix=prefix_file)
				
for o in report_bucket_objects.data.objects:
    print('Found file ' + o.name)
    
    object_details = object_storage.get_object(reporting_namespace, reporting_bucket, o.name)
    filename = o.name.rsplit('/', 1)[-1]
	
    with open(destintation_path + '/' + filename, 'wb') as f:
        for chunk in object_details.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    
    upload_file(destintation_path + '/' + filename,"oci-data-bucket",filename)

				
    print('----> File ' + o.name + ' Downloaded')
    

    
