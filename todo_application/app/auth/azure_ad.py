import requests
from fastapi import HTTPException
from config import Config

class AzureADAuth:
    def __init__(self):
        self.client_id = Config.AZURE_CLIENT_ID
        self.client_secret = Config.AZURE_CLIENT_SECRET
        self.tenant_id = Config.AZURE_TENANT_ID

    def get_user_info(self, token: str):
        """ Get user information from Azure AD by validating the token """
        url = f'https://graph.microsoft.com/v1.0/me'
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return response.json()
