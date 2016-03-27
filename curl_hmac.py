import hashlib, hmac, base64
import argparse
import os

# Parse cli parameters
parser = argparse.ArgumentParser(description='Tool for calculating AimBrain\'s API HMAC signature using curl. '\
    'Example usage: python2 curl_hmac.py test secret POST /v1/sessions \'{"userId": "lol-user", "device":"lol device", "system":"lol system"}\' -r')
parser.add_argument('apikey', metavar='APIKey', type=str, help='AimBrain API Key')
parser.add_argument('apisecret', metavar='APISecret', type=str, help='AimBrain API Secret')
parser.add_argument('method', metavar='Method', type=str, help='API Method')
parser.add_argument('endpoint', metavar='Endpoint', type=str, help='API Endpoint')
parser.add_argument('request', metavar='Request', type=str, help='API request body')
parser.add_argument('-r', '--run', action='store_true', help='Run the outputed curl command automatically')
parser.add_argument('-s', '--staging', action='store_true', help='Use staging endpoint')
args = parser.parse_args()

# Construct curl request
base = 'https://api-staging.aimbrain.com:443' if args.staging else 'https://api.aimbrain.com:443'

signature = base64.b64encode(hmac.new(bytes(args.apisecret).encode('utf-8'),
    bytes(args.method.upper() + '\n' + args.endpoint.lower() + '\n' + args.request + '').encode('utf-8'),
    digestmod=hashlib.sha256).digest())

curlReq = 'curl '\
    + base + args.endpoint + ' '\
    '-H \'Content-Type: application/json\' '\
    '-H \'X-aimbrain-apikey: ' + args.apikey + '\' '\
    '-H \'X-aimbrain-signature: ' + signature + '\' '\
    '-d \'' + args.request + '\' '

if args.run:
    print(curlReq + "\n")
    os.system(curlReq)
    print("")
else:
    print('-----CURL COMMAND-----\n' + curlReq + '\n-----CURL COMMAND-----')
