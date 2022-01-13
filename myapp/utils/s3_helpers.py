#!/usr/bin/env python3

import boto3
import botocore
import creds
import os
    
class Client:
    def __init__(self, use_minio=False):
        self.minio = use_minio
        if(use_minio):
            self.s3_resource = creds.createMinioresource()
            self.s3_client = creds.createMinioclient()
        else:
            self.s3_resource = creds.createS3resource()
            self.s3_client = creds.createS3client()
        print("Loading Minio Resources")
