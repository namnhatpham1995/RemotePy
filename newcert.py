#!/usr/bin/python
from OpenSSL import crypto
import os
import sys
import datetime
import whois

# Variables
TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA
HOME = os.getenv("HOME")
now = datetime.datetime.now()
d = now.date()

# Pull these out of scope
cn = input("Enter the Domain: ")
key = crypto.PKey()
keypath = HOME + "/" + cn + '-' + str(d) + '.key'
csrpath = HOME + "/" + cn + '-' + str(d) + '.csr'
crtpath = HOME + "/" + cn + '-' + str(d) + '.crt'


# Generate the key


def generatekey():
    if os.path.exists(keypath):
        print("Certificate file exists, aborting.")
        print(keypath)
        sys.exit(1)
    # Else write the key to the keyfile
    else:
        print("Generating Key Please standby")
        key.generate_key(TYPE_RSA, 4096)
        f = open(keypath, "w")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        f.close()

    # return key


generatekey()


# Generate CSR

def generatecsr():
    print("How would you like to generate csr data?\n"
          "1) CQB (For Self-Signed Certs).\n"
          "2) Specify your own.\n"
          "3) Attempt Whois Look"
          )
    option = input("Choose (1/2/3): ")
    if option == 1:
        c = 'US'
        st = 'California'
        l = 'Berkley'
        o = 'CQB'
        ou = 'Network Operations'
    elif option == 2:
        c = input('Enter your country(ex. US): ')
        st = input("Enter your state(ex. Nevada): ")
        l = input("Enter your location(City): ")
        o = input("Enter your organization: ")
        ou = input("Enter your organizational unit(ex. IT): ")
    else:
        print("Attempting WHOIS Lookup")
        w = whois.whois(cn)
        c = str(w.get('country'))
        st = str(w.get('state')).lower().title()
        l = str(w.get('city')).lower().title()
        o = str(w.get('org')).lower().title()
        ou = 'Network Operations'

    req = crypto.X509Req()
    req.get_subject().CN = cn
    req.get_subject().C = c
    req.get_subject().ST = st
    req.get_subject().L = l
    req.get_subject().O = o
    req.get_subject().OU = ou
    req.set_pubkey(key)
    req.sign(key, "sha256")

    if os.path.exists(csrpath):
        print("Certificate File Exists, aborting.")
        print(csrpath)
    else:
        f = open(csrpath, "w")
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
        f.close()
        print("Success")

    # Generate the certificate
    reply = str(input('Is this a Self-Signed Cert (y/n): ')).lower().strip()

    if reply[0] == 'y':
        cert = crypto.X509()
        cert.get_subject().CN = cn
        cert.get_subject().C = c
        cert.get_subject().ST = st
        cert.get_subject().L = l
        cert.get_subject().O = o
        cert.get_subject().OU = ou
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, "sha256")

        if os.path.exists(crtpath):
            print("Certificate File Exists, aborting.")
            print(crtpath)
        else:
            f = open(crtpath, "w")
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            f.close()
            print("CRT Stored Here :" + crtpath)


generatecsr()

print("Key Stored Here :" + keypath)
print("CSR Stored Here :" + csrpath)
