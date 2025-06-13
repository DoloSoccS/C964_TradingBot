import base64
from Backend_Content.Backend import give_passphrase

# Take in input passphrase, encode and compare to backend passphrase.
def test_passphrase(pass_input):
    secureLogin_encoded = base64.b64encode(give_passphrase().encode())

    if pass_input == base64.b64decode(secureLogin_encoded).decode("utf-8"):
        return True
