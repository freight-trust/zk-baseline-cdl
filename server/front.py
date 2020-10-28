from flask import Flask
from flask import render_template
import codecs
import ecdsa
import web3
import subprocess
from Crypto.Hash import keccak
from subprocess import PIPE, run
from web3 import Web3, HTTPProvider
import time

app = Flask(__name__)


def public_to_address(public_key):
    public_key_bytes = codecs.decode(public_key, "hex")
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    keccak_digest = keccak_hash.hexdigest()
    # Take last 20 bytes
    wallet_len = 40
    wallet = "0x" + keccak_digest[-wallet_len:]
    return wallet


app = Flask(__name__, static_url_path="")


@app.route("/test")
def render_static():

    args = ["python3", "verify.py"]
    result = subprocess.call(args, cwd="~/baseline/zkp/verify")
    if result == 0:
        return render_template("CDL.html")
    else:
        return render_template("noCDL.html")


@app.route("/")
def render_statics():
    args = ["baseline", "get_key_info", "1"]
    output, error = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
    search1 = "SEC1): "
    l = str(output)
    add = l[l.find(search1) + 7 :]
    public_key = add[:-3]
    print("public_key: ", public_key)
    address = public_to_address(public_key)
    print("address: ", address)
    print("address len: ", len(public_key))
    if len(public_key) > 0:
        return render_template("Loading.html")
    else:
        return render_template("Startscreen.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
