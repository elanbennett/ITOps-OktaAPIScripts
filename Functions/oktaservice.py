from okta.client import Client as OktaClient

# Instantiating with a Python dictionary in the constructor
config = {
    'orgUrl': 'https://canoo.okta.com',
    'token': '00nLbLQWGABxr7tcdCxd8ES4d5JWs9_VpcDJC_nOaM'
}
okta_client = OktaClient(config)
