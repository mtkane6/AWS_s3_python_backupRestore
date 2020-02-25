import boto3
import os
import time
import datetime
import sys
import string


def backup(rootDir):  
    s3 = boto3.resource("s3")
    try:
        newBucket = "0727916.mtkuw.edu" + str.lower(rootDir)
        newBucket = newBucket.replace("/", "")
        newBucket = newBucket.replace("\\", "")
        print("newBucket: %s" % newBucket)
        s3.create_bucket(Bucket=newBucket, CreateBucketConfiguration={'LocationConstraint':'ap-northeast-1'})
    except:# print(newBucket)
        print("Bucket %s exists, attempting upload" % newBucket)
    uploadSuccess = False
    
    # print("Starting directory: %s" % rootDir)
    for root, dirs, filename in os.walk('.'): # walks files, and directories
        # print("Current directory: %s" % root)
        for currentFile in filename:
            slash = "/" if os.name == 'posix' else "\\"
            currentPath = root+slash+currentFile
            if rootDir in currentPath:
                if not str.startswith(currentFile,'.DS_'): # for MacOS, this skips ".DS_Store" files, which serve indexing purposes.
                    currentFileName = root + slash + currentFile
                    # get last modified time of local file
                    localFileLastModified = datetime.datetime.utcfromtimestamp(os.path.getmtime(currentFileName)).strftime('%Y-%m-%d %H:%M:%S')
                    bucket = s3.Bucket(newBucket)
                    # get last upload time of file in bucket
                    try:
                        obj = bucket.Object(currentFileName).last_modified
                        objectFileLastModified = obj.strftime('%Y-%m-%d %H:%M:%S')
                        # check to see if file modified since last upload
                        if localFileLastModified > objectFileLastModified:
                            s3.Object(newBucket, currentFileName).put(Body=open(root + slash + currentFile,"rb"))
                            print("Performed upload of: %s" % currentFile)
                            uploadSuccess = True
                        else:
                            print("%s not modified, not uploaded." % currentFile)
                            uploadSuccess = True
                    except:
                        s3.Object(newBucket, currentFileName).put(Body=open(root + slash + currentFile,"rb"))
                        print("Performed upload of: %s" % currentFile)
                        uploadSuccess = True
    if not uploadSuccess:
        print("Could not locate that file or folder for upload.")

pathway = sys.argv[1] # take in file path from user
if pathway.endswith("/") or pathway.endswith("\\"):
    pathway = pathway[:-1]
slash = "/" if os.name == 'posix' else "\\"
splitPathway = pathway.split(slash)
pathway = slash + splitPathway[len(splitPathway)-1]

try:
    backup(str(pathway))
except:
    print("Pathway or file not found: %s" % pathway)
# backup(str(pathway))
   
