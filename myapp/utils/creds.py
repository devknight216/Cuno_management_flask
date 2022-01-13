import boto3
import botocore
import os
import json
import google.cloud.storage
from google.oauth2 import service_account
from azure.storage.blob import BlockBlobService, PublicAccess

# These paths imply these are conventional credentials files that we are expecting to read in. 
# What we actually need is to be able to read cunomgr generated cred files, because we want to use this only on credentials that have been imported already (and imported using the UI - which itself will depend on cunomgr)
S3CREDPATH = "/tmp/creds/conventional/s3creds"
MINIOCREDPATH = "/tmp/creds/conventional/minio.creds"
AWS_REGION = "us-east-2"
GSCREDPATH = "/tmp/creds/conventional/gskey.json"
AZCREDPATH = "/tmp/creds/conventional/azure.export"


def readMiniocred():
    try:
        key = ""
        secret = ""
        region = AWS_REGION
        endpoint = ""
        skipssl = False
        pathstyle = False
        print("Reading CREDS:" + MINIOCREDPATH)
        with open(MINIOCREDPATH, "r") as f:
            for x in f:
                parts = x.split("=")
                if len(parts) == 2:
                    if parts[0].strip() == "aws_secret_access_key":
                        secret = parts[1].strip()
                    elif parts[0].strip() == "aws_access_key_id":
                        key = parts[1].strip()
                    elif parts[0].strip() == "region":
                        region = parts[1].strip()
                    elif parts[0].strip() == "endpoint":
                        endpoint = parts[1].strip()
                    elif parts[0].strip() == "skipssl":
                        skipssl = True
                    elif parts[0].strip() == "pathstyle":
                        pathstyle = True
        return {'aws_access_key_id':key, 'aws_secret_access_key':secret, 'region': region, 'endpoint': endpoint, 'pathstyle': pathstyle, 'skipssl': skipssl}
    except:
        return {}


def createMinioclient():
    botoconfig_pathstyle = botocore.config.Config(s3={'addressing_style': 'path'}, read_timeout=1200, connect_timeout=60, retries={"max_attempts": 1})
    botoconfig = botocore.config.Config(read_timeout=1200, connect_timeout=60, retries={"max_attempts": 1})
    #print("################### createMinioClient config: ", botoconfig)
    creds = readMiniocred()
    if len(creds) != 0 and creds['aws_access_key_id'] != "" and creds['aws_secret_access_key'] != "" and creds['region'] != "":
        print("[Python modules for cloud access] Using Minio credentials from " + MINIOCREDPATH)
        print("aws_access_key_id: " + creds['aws_access_key_id'])
        print("aws_secret_access_key: " + creds['aws_secret_access_key'])
        print("region: " + creds['region'])
        print("endpoint: " + creds['endpoint'])
        print("pathstyle: " + str(creds['pathstyle']))
        print("skipssl: " + str(creds['skipssl']))
         
        if(creds['pathstyle']):
            return boto3.client(
                "s3",
                aws_access_key_id = creds['aws_access_key_id'],
                aws_secret_access_key = creds['aws_secret_access_key'],
                region_name = creds['region'],
                use_ssl = not creds['skipssl'],
                endpoint_url = creds['endpoint'],
                config=botoconfig_pathstyle)
        
        return boto3.client(
            "s3",
            aws_access_key_id = creds['aws_access_key_id'],
            aws_secret_access_key = creds['aws_secret_access_key'],
            region_name = creds['region'],
            use_ssl = not creds['skipssl'],
            endpoint_url = creds['endpoint'],
            config=botoconfig)

    print("[Python modules for cloud access] Using the default Minio credentials, e.g. ~/.aws/credentials or using ENV variables")
    return boto3.client("s3", botoconfig)


def createMinioresource():
    botoconfig_pathstyle = botocore.config.Config(s3={'addressing_style': 'path'}, read_timeout=1200, connect_timeout=60, retries={"max_attempts": 1})
    botoconfig = botocore.config.Config(read_timeout=1200, connect_timeout=60, retries={"max_attempts": 1})
    creds = readMiniocred()
    if len(creds) != 0 and creds['aws_access_key_id'] != "" and creds['aws_secret_access_key'] != "" and creds['region'] != "":
        print("[Python modules for cloud access] Using Minio credentials from " + MINIOCREDPATH)
        print("aws_access_key_id: " + creds['aws_access_key_id'])
        print("aws_secret_access_key: " + creds['aws_secret_access_key'])
        print("region: " + creds['region'])
        print("endpoint: " + creds['endpoint'])
        print("pathstyle: " + str(creds['pathstyle']))
        print("skipssl: " + str(creds['skipssl']))
        if(creds['pathstyle']):
            return boto3.resource(
                "s3",
                aws_access_key_id = creds['aws_access_key_id'],
                aws_secret_access_key = creds['aws_secret_access_key'],
                region_name = creds['region'],
                use_ssl = not creds['skipssl'],
                endpoint_url = creds['endpoint'],
                config=botoconfig_pathstyle)
        return boto3.resource(
            "s3",
            aws_access_key_id = creds['aws_access_key_id'],
            aws_secret_access_key = creds['aws_secret_access_key'],
            region_name = creds['region'],
            use_ssl = not creds['skipssl'],
            endpoint_url = creds['endpoint'],
            config=botoconfig)


    print("[Python modules for cloud access] Using the default Minio credentials, e.g. ~/.aws/credentials or using ENV variables")
    return boto3.resource("s3", config=botoconfig)

def readS3cred():
    try:
        key = ""
        secret = ""
        region = AWS_REGION
        with open(S3CREDPATH, "r") as f:
            for x in f:
                parts = x.split("=")
                if len(parts) == 2:
                    if parts[0].strip() == "aws_secret_access_key":
                        secret = parts[1].strip()
                    elif parts[0].strip() == "aws_access_key_id":
                        key = parts[1].strip()
                    elif parts[0].strip() == "region":
                        region = parts[1].strip()
        return {'aws_access_key_id':key, 'aws_secret_access_key':secret, 'region': region}
    except:
        return {}


def createS3client():
    botoconfig = botocore.config.Config(read_timeout=1200, connect_timeout=60, retries={"max_attempts": 1})
    #print("################### createS3Client config: ", botoconfig)
    creds = readS3cred()
    if len(creds) != 0 and creds['aws_access_key_id'] != "" and creds['aws_secret_access_key'] != "" and creds['region'] != "":
        print("[Python modules for cloud access] Using S3 credentials from " + S3CREDPATH)
        # print("aws_access_key_id: " + creds['aws_access_key_id'])
        # print("aws_secret_access_key: " + creds['aws_secret_access_key'])
        return boto3.client(
            "s3",
            aws_access_key_id = creds['aws_access_key_id'],
            aws_secret_access_key = creds['aws_secret_access_key'],
            region_name = creds['region'],
            config=botoconfig)

    print("[Python modules for cloud access] Using the default S3 credentials, e.g. ~/.aws/credentials or using ENV variables")
    return boto3.client("s3", config=botoconfig)


def createS3resource():
    botoconfig = botocore.config.Config(read_timeout=1200, connect_timeout=60, retries={"max_attempts": 1})
    creds = readS3cred()
    if len(creds) != 0 and creds['aws_access_key_id'] != "" and creds['aws_secret_access_key'] != "" and creds['region'] != "":
        print("[Python modules for cloud access] Using S3 credentials from " + S3CREDPATH)
        return boto3.resource(
            "s3",
            aws_access_key_id = creds['aws_access_key_id'],
            aws_secret_access_key = creds['aws_secret_access_key'],
            region_name = creds['region'],
            config=botoconfig)

    print("[Python modules for cloud access] Using the default S3 credentials, e.g. ~/.aws/credentials or using ENV variables")
    return boto3.resource("s3")


def createGSclient():
    try:
        with open(GSCREDPATH, "r") as source:
            info = json.load(source)
        cred = service_account.Credentials.from_service_account_info(info)
        if info["project_id"] != "":
            print("[Python modules for cloud access] Using GS credentials from " + GSCREDPATH)
            return google.cloud.storage.Client(project = info["project_id"], credentials = cred)
        else:
            print("[Python module for cloud access] Creating an anonymous client")
            return google.cloud.storage.Client()
    except:
        print("[Python modules for cloud access] Using the default GS credentials as set in the corresponding ENV variable")
        return google.cloud.storage.Client()


def readAZcred():
    try:
        account = ""
        key = ""
        with open(AZCREDPATH, "r") as f:
            for x in f:
                parts = x.split("=")
                if len(parts) >= 2:
                    if "AZURE_STORAGE_ACCOUNT" in parts[0].strip():
                        account = parts[1].strip()
                    elif "AZURE_STORAGE_ACCESS_KEY" in parts[0].strip():
                        key = x[len(parts[0]) + 1:].strip()
        return {'account':account.strip('\"'), 'key':key.strip('\"')}
    except:
        return {}


def createAZclient():
    creds = readAZcred()
    if len(creds) != 0 and creds['account'] != "" and creds['key'] != "":
        print("[Python modules for cloud access] Using AZURE credentials from " + AZCREDPATH)
        # print("account: " + creds['account'])
        # print("key: " + creds['key'])
        return BlockBlobService(account_name = creds['account'], account_key = creds['key'])
    else:
        print("[Python modules for cloud access] Using the default AZ credentials as set in the corresponding ENV variables")
        return BlockBlobService(account_name = os.environ["AZURE_STORAGE_ACCOUNT"], account_key = os.environ["AZURE_STORAGE_ACCESS_KEY"])


def getAZaccount():
    creds = readAZcred()
    if len(creds) != 0 and creds['account'] != "" and creds['key'] != "":
        return creds['account']
    else:
        return os.environ.get("AZURE_STORAGE_ACCOUNT", None)


def getAZkey():
    creds = readAZcred()
    if len(creds) != 0 and creds['account'] != "" and creds['key'] != "":
        return creds['key']
    else:
        return os.environ.get("AZURE_STORAGE_ACCESS_KEY", None)
