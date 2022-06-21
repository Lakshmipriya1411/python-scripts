import oci
import os
reporting_namespace = 'ax8hkeiizrq6'
                               
# Download all usage and cost files. You can comment out based on the specific need:
#prefix_file = "reports_cost-csv_0001000000576648.csv.gz"                     
#  For cost and usage files
# prefix_file = "reports/cost-csv"   #  For cost
prefix_file = "reports/usage-csv"  #  For usage
                               
# Update these values
destintation_path = 'downloaded_reports'
                               
# Make a directory to receive reports
if not os.path.exists(destintation_path):
    os.mkdir(destintation_path)
    

#user_ocid = os.environ["USER_OCID"]
#key_file = key_for(user_ocid)

config = {
    "user": "ocid1.user.oc1..aaaaaaaafl4jxczrzgy7tqvm4mmvap4qib3nraqxs2aaad3dmw45ulkexmha",
    "key_file": "C:\\Users\\lgundlapalli\\Videos\\.oci\\oci_api_key.pem",
    "fingerprint": "91:ef:a4:c0:03:8d:f9:a6:1b:db:4b:48:e5:23:8c:36",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaa33ijrbogdsgrvat44py342kyq7pza4yo22q2lkv5xil3a6sby5wq",
    "region": "us-sanjose-1"   
}

from oci.config import validate_config
validate_config(config)
                               
# Get the list of reports
#config = oci.config.from_file(oci.config.DEFAULT_LOCATION, oci.config.DEFAULT_PROFILE)
#reporting_bucket = config['tenancy']
reporting_bucket = "bucket1"
object_storage = oci.object_storage.ObjectStorageClient(config)
report_bucket_objects = oci.pagination.list_call_get_all_results(object_storage.list_objects, reporting_namespace, reporting_bucket, prefix=prefix_file)                          
print(report_bucket_objects.data)
for o in report_bucket_objects.data.objects:
    print('Found file ' + o.name)
    object_details = object_storage.get_object(reporting_namespace, reporting_bucket, o.name)
    filename = o.name.rsplit('/', 1)[-1]
                               
    with open(destintation_path + '/' + filename, 'wb') as f:
        for chunk in object_details.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
                               
    print('----> File ' + o.name + ' Downloaded')