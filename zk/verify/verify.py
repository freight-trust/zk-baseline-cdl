import codecs
import subprocess
from Crypto.Hash import keccak
from main import readProof
import json


def public_to_hash(ids):
    keccak_hash = keccak.new(digest_bits=256)
    for i in ids:
        keccak_hash.update(get_public_key(i))
    keccak_digest = keccak_hash.hexdigest()
    return keccak_digest


def get_public_key(pk_id):
    args = ["baseline", "get_key_info", str(pk_id)]
    output, error = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
    search = "SEC1): "
    l = str(output)
    add = l[l.find(search) + 7 :]
    public_key = add[:-3]
    print(public_key)
    return codecs.decode(public_key, "hex")


hashOfPublicKeys = public_to_hash([3, 4, 5])
print(hashOfPublicKeys)

f = open("public.json", "w")
f.write('["1", ' + '"0x' + str(hashOfPublicKeys) + '"]\n')
f.close()

args = ["baseline", "get_key_info", "1"]
output, error = subprocess.Popen(
    args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
).communicate()
search = "SEC1): "
l = str(output)
add = l[l.find(search) + 7 :]
public_key = add[:-3]
print(public_key)
public_key = codecs.decode(public_key, "hex")
keccak_hash = keccak.new(digest_bits=256)
keccak_hash.update(public_key)
keccak_digest = keccak_hash.hexdigest()
wallet_len = 40
address = "0x" + keccak_digest[-wallet_len:]
checksum = "0x"
# Remove ‘0x’ from the address
address = address[2:]
address_byte_array = address.encode("utf-8")
keccak_hash = keccak.new(digest_bits=256)
keccak_hash.update(address_byte_array)
keccak_digest = keccak_hash.hexdigest()

for i in range(len(address)):
    address_char = address[i]
    keccak_char = keccak_digest[i]
    if int(keccak_char, 16) >= 8:
        checksum += address_char.upper()
    else:
        checksum += str(address_char)

public_address = checksum
print("Public Address: ", public_address)


f = open("proof.json", "w")
json.dump(readProof(public_address), f)
f.close()

result = subprocess.call("snarkjs verify", shell=True)
exit(result)
