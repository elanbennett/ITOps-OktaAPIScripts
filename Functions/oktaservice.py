from okta.client import Client as OktaClient

# Instantiating with a Python dictionary in the constructor
config = {
    'orgUrl': 'https://acme.okta.com',
    'token': ''
}
okta_client = OktaClient(config)
