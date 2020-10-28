import ipfsapi
import requests
from web3 import Web3
import json

contract_address = "${CONTRACT_ADDRESS}"
contract_abi = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_tokenId","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0x095ea7b3"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x18160ddd"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0x23b872dd"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"tokenCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x56225a09"},{"constant":true,"inputs":[{"name":"_tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"name":"owner","type":"address"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x6352211e"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"count","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x70a08231"},{"constant":true,"inputs":[],"name":"verificationKey","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x7ddc907d"},{"constant":false,"inputs":[{"name":"_owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"name":"tokenIds","type":"uint256[]"}],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0x8462151c"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x8da5cb5b"},{"constant":true,"inputs":[],"name":"isOwner","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x8f32d59b"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"proofs","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x9ddaf5aa"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_tokenId","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0xa9059cbb"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"tokenOwners","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function","signature":"0xf8a14f46"},{"inputs":[{"name":"_verificationKey","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"constructor","signature":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"from","type":"address"},{"indexed":false,"name":"to","type":"address"},{"indexed":false,"name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event","signature":"0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"},{"anonymous":false,"inputs":[{"indexed":false,"name":"owner","type":"address"},{"indexed":false,"name":"approved","type":"address"},{"indexed":false,"name":"tokenId","type":"uint256"}],"name":"Approval","type":"event","signature":"0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_proof","type":"string"}],"name":"issueIdentityToken","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0x97c55e7f"}]'

w3 = Web3(Web3.HTTPProvider("http://${WEB3_PROVIDER_IP}"))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

"""
Upload a proof file in json format to IPFS and issue a new identitiy token which includes the IPFS hash
to the specified wallet which can be used to fetch the proof from the IPFS network.
@:returns None 
"""


def uploadProof(filename, wallet_address):
    content = json.loads(open(filename, "r").read())

    api = ipfsapi.connect("${PERSISTANCE_IP}", 5001)
    proofIpfsId = api.add_json(content)

    tx_hash = contract.functions.issueIdentityToken(
        wallet_address, proofIpfsId
    ).transact({"from": w3.eth.accounts[0]})
    w3.eth.waitForTransactionReceipt(tx_hash)


"""
Get the proof from the IPFS network for a specific wallet address in json format.
@:returns Proof in JSON format or None
"""


def readProof(wallet_address):
    try:
        contract.functions.balanceOf(wallet_address).call()
    except:
        return None

    proofId = contract.functions.tokensOfOwner(wallet_address).call()[0]
    proofIpfsId = contract.functions.proofs(proofId).call()

    response = requests.get("http://${PERSISTANCE_IP}:8080/ipfs/" + proofIpfsId)
    proof = json.loads(response.content.decode("utf8").replace("'", '"'))

    return proof


"""
Get the public verification key from the IPFS network.
@:returns Verification key in JSON format
"""


def readVerificationKey():
    verificationKeyIpfsId = contract.functions.verificationKey().call()

    response = requests.get(
        "http://${PERSISTANCE_IP}:8080/ipfs/" + verificationKeyIpfsId
    )
    verificationKey = json.loads(response.content.decode("utf8").replace("'", '"'))

    return verificationKey


# Wallet Address
wallet_address = "${SIGNING_ADDRESS}"

# uploadProof("proof.json", wallet_address)

print(readProof(wallet_address))

# print(readVerificationKey())
