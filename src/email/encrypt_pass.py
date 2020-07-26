#example to show how to encrypt your password
#Reference web link valid as of 07/25/2020
# https://www.mssqltips.com/sqlservertip/5173/encrypting-passwords-for-use-with-python-and-sql-server/#:~:text=The%20Python%20library%20used%20in,is%20required%20to%20decrypt%20it.
from cryptography.fernet import Fernet
import getpass
#how to get keys
#key = Fernet.generate_key()
#print(key)
# you need to generate it once and just use it
key = b'lHwEPPG06WDsWCGC1HjgqtQzOuvvn2c5K1iUok7qiKs='
cipher_suite = Fernet(key)
pass_text=getpass.getpass("enter password to generated encrypted password binary file:")
pass_text_bytes = bytes(pass_text, 'utf-8')
ciphered_text = cipher_suite.encrypt(pass_text_bytes)
with open ("encrypted_pass.txt", "wb") as fp_w: fp_w.write(ciphered_text)
fp_w.close()
with open ("encrypted_pass.txt", "rb") as fp_r:
	for line in fp_r:
		encrypted_pwd = line



uncipher_text = (cipher_suite.decrypt(encrypted_pwd))
plain_text_encrypted_password = bytes(uncipher_text).decode("utf-8")
print(plain_text_encrypted_password)
fp_r.close()

