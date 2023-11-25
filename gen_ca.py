# adapted from https://python.plainenglish.io/automate-the-local-certificate-authority-registration-with-python-ced8771b2742
# and https://stackoverflow.com/a/60516812
# WARNING: this script won't make the certificate trusted by the system
import subprocess as sp
import os
import socket

dirname = os.path.dirname(__file__)

# check if folder "ca-cert" exists
# if not, create it
# if yes, delete it
if os.path.exists(os.path.join(dirname, "ca-cert")):
    import shutil

    shutil.rmtree(os.path.join(dirname, "ca-cert"))
os.mkdir(os.path.join(dirname, "ca-cert"))

validDate = input("Enter the expiration (days) of the certificate: ")
_n = "\n"

# 0. create config file
open(os.path.join(dirname, "ca-cert/ca.cnf"), "w").write(
    f"""
[req]
default_bits = 2048
prompt = no
default_md = sha256
encrypt_key = no
distinguished_name = dn
req_extensions = req_ext
[dn]
C = ID
O = Local Digital Cert Authority
OU = www.ca.local
CN = Self-Signed Root CA
[req_ext]
subjectAltName = @alt_names
[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
{_n.join([f"DNS.{i} = {ip[4][0]}" for i, ip in enumerate(socket.getaddrinfo(socket.gethostname(), None), start=3)])}
IP.1 = 127.0.0.1
{_n.join([f"IP.{i} = {ip[4][0]}" for i, ip in enumerate(socket.getaddrinfo(socket.gethostname(), None), start=2)])}
"""
)

open(os.path.join(dirname, "ca-cert/ca.ext"), "w").write(
    f"""
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
{_n.join([f"DNS.{i} = {ip[4][0]}" for i, ip in enumerate(socket.getaddrinfo(socket.gethostname(), None), start=3)])}
IP.1 = 127.0.0.1
{_n.join([f"IP.{i} = {ip[4][0]}" for i, ip in enumerate(socket.getaddrinfo(socket.gethostname(), None), start=2)])}
"""
)


# generate base certificate
sp.call(["openssl", "genrsa", "-des3", "-out", os.path.join(dirname, "ca-cert/temp_ca.key"), "2048"])
sp.call(
    [
        "openssl",
        "req",
        "-x509",
        "-new",
        "-nodes",
        "-key", os.path.join(dirname, "ca-cert/temp_ca.key"),
        "-sha256",
        "-days", validDate,
        "-out", os.path.join(dirname, "ca-cert/temp_ca.pem"),
        "-config", os.path.join(dirname, "ca-cert/ca.cnf"),
    ]
)


# 1. generate a root CA certificate and private key
sp.call(["openssl", "genrsa", "-out", os.path.join(dirname, "ca-cert/ca.key"), "2048"])
# 2. generate CSR with config file
sp.call(
    [
        "openssl",
        "req",
        "-new",
        "-key", os.path.join(dirname, "ca-cert/ca.key"),
        "-out", os.path.join(dirname, "ca-cert/ca.csr"),
        "-config", os.path.join(dirname, "ca-cert/ca.cnf"),
    ]
)

# 3. create a self-signed CA certificate
sp.call(
    [
        "openssl",
        "x509",
        "-req",
        "-days",
        validDate,
        "-in", os.path.join(dirname, "ca-cert/ca.csr"),
        "-CA", os.path.join(dirname, "ca-cert/temp_ca.pem"),
        "-CAkey", os.path.join(dirname, "ca-cert/temp_ca.key"),
        "-CAcreateserial",
        "-out", os.path.join(dirname, "ca-cert/ca.crt"),
        "-sha256",
        "-extfile", os.path.join(dirname, "ca-cert/ca.ext"),
    ]
)
print("CA certificate and private key generated")
