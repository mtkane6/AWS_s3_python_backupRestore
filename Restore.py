import boto3
import sys
import os

# dowloads files from s3 bucket to local drive
def restore(directory):
    s3 = boto3.resource("s3")
    for bucket in s3.buckets.all():
        s3 = boto3.client("s3")
        print("From bucket: %s" % bucket.name)
        for nextkey in bucket.objects.all():
            # dowloads file, maintaining file names and file structure
            if directory in nextkey.key:
                if not os.path.exists(os.path.dirname(nextkey.key)):
                    os.makedirs(os.path.dirname(nextkey.key))
                s3.download_file(bucket.name, nextkey.key, nextkey.key)
                print("Downloaded file: %s" % nextkey.key)

pathway = sys.argv[1] # take in file path from user
if pathway.endswith("/") or pathway.endswith("\\"):
    pathway = pathway[:-1]
slash = "/" if os.name == 'posix' else "\\"
splitPathway = pathway.split(slash)
pathway = slash + splitPathway[len(splitPathway)-1]
try:
    restore(pathway)
except:
    print("Restore failed")