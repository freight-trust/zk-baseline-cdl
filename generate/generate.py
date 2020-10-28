from subprocess import call
import codecs
import subprocess
from Crypto.Hash import keccak


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

f = open("input.json", "w")
f.write('{"hash":' + '"0x' + str(hashOfPublicKeys) + '", "age":' + str(20) + "}\n")
f.close()

call("snarkjs calculateWitness", shell=True)
call("snarkjs proof", shell=True)
