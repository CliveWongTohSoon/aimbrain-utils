import hashlib, hmac, base64
import argparse
import os

# Parse cli parameters
parser = argparse.ArgumentParser(description='Tool for calculating AimBrain\'s Authenticator API HMAC signature using curl. '\
    'Example usage: python2 curl_hmac_authenticator.py bank secret POST /v1/requests \'{"ids":["XXXXXXXX"],"timeout":180,"modules":[0],"threshold":0.5,"attempts":3,"title":"Title","summary":"Summary"}\' -r')
parser.add_argument('apikey', metavar='APIKey', type=str, help='AimBrain Authenticator API Key')
parser.add_argument('apisecret', metavar='APISecret', type=str, help='AimBrain Authenticator API Secret')
parser.add_argument('method', metavar='Method', type=str, help='API Method')
parser.add_argument('endpoint', metavar='Endpoint', type=str, help='API Endpoint')
parser.add_argument('request', metavar='Request', type=str, help='API request body or file')
parser.add_argument('-f', '--request-from-file', action='store_true', help='Read request\'s body from a file instead command line')
parser.add_argument('-r', '--run', action='store_true', help='Run the outputed curl command automatically')
args = parser.parse_args()

# Construct curl request
base = 'https://authenticator.aimbrain.com:443'
http_method = args.method.upper()
endpoint = args.endpoint.lower()

request = args.request
if args.request_from_file:
    request = open(args.request,'r').read().strip()

signature = base64.b64encode(hmac.new(bytes(args.apisecret).encode('utf-8'),
    bytes(http_method + '\n' + endpoint + '\n' + request + '').encode('utf-8'),
    digestmod=hashlib.sha256).digest())

curlReq = 'curl '\
    + base + endpoint + ' '\
    '-H \'Content-Type: application/json\' '\
    '-H \'X-aimbrain-apikey: ' + args.apikey + '\' '\
    '-H \'X-aimbrain-signature: ' + signature + '\' '

if args.request_from_file:
    curlReq += '--data \'@' + args.request + '\' '
else:
    curlReq += '-d \'' + request + '\' '

if args.run:
    print(curlReq + "\n")
    os.system(curlReq)
    print("")
else:
    print('-----CURL COMMAND-----\n' + curlReq + '\n-----CURL COMMAND-----')
