import google.api_core.exceptions
from google.cloud import storage
import creds
import os
class Client:
    def __init__(self):
        self.client = creds.createGSclient()
