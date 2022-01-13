from creds import getAZaccount, getAZkey
from azure.storage.blob import BlockBlobService

class Client:
    def __init__(self):
        account_name = getAZaccount()

        if account_name is None:
            raise RuntimeError("Env var AZURE_STORAGE_ACCOUNT has not been set. Please 'source creds/azure.export")

        account_key = getAZkey()
        
        if account_key is None:
            raise RuntimeError("Env var AZURE_STORAGE_ACCESS_KEY has not been set. Please 'source creds/azure.export")

        self.client = BlockBlobService(account_name=account_name, account_key=account_key)

    def create_bucket(self, bucket_name):
        self.client.create_container(bucket_name)
