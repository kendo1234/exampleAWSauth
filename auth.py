import boto3

from requests_aws4auth import AWS4Auth
import requests

# Get credentials

boto3.setup_default_session(region_name='REGION')
identity = boto3.client('cognito-identity', region_name='REGION')

account_id = 'ACCOUNT_ID'
identity_pool_id = 'FOUND IN FEDERATED ID POOL AREA'


response = identity.get_id(AccountId=account_id, IdentityPoolId=identity_pool_id)
identity_id = response['IdentityId']
print("Identity ID: %s" % identity_id)

# Print these out if you need to make sure you have the correct values - DO NOT COMMIT THEM PRINTED
resp = identity.get_credentials_for_identity(IdentityId=identity_id)
secretKey = resp['Credentials']['SecretKey']
accessKey = resp['Credentials']['AccessKeyId']
sessionToken = resp['Credentials']['SessionToken']
expiration = resp['Credentials']['Expiration']

# Test

endpoint = 'http://localhost:3000/BLAH'
auth = AWS4Auth(identity_id, accessKey, 'REGION', 'cognito-identity',
                session_token=sessionToken)
response = requests.get(endpoint, auth=auth)
print(response.text)


