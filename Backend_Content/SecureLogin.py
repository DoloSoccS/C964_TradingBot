import base64
from Backend_Content.Backend import give_passphrase


def test_passphrase(input):
    secureLogin_encoded = base64.b64encode(give_passphrase().encode())

    if input == base64.b64decode(secureLogin_encoded).decode("utf-8"):
        return True
