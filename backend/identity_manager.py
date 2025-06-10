from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from web3 import Web3
import os

class IdentityAnchor:
    def __init__(self, imei: str, email: str):
        self.salt = os.urandom(16)
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=64,
            salt=self.salt,
            iterations=480000
        )
        self.identity_root = self._derive_root(imei, email)
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_RPC_URL')))
       
    def _derive_root(self, *seeds) -> bytes:
        material = b''.join(s.encode() for s in seeds)
        return self.kdf.derive(material)
   
    def register_on_chain(self):
        contract = self.web3.eth.contract(
            address=os.getenv('IDENTITY_CONTRACT_ADDRESS'),
            abi=IDENTITY_CONTRACT_ABI
        )
        tx = contract.functions.registerUser(
            Web3.keccak(self.identity_root[:32]),
            Web3.keccak(self.identity_root[32:])
        ).build_transaction({
            'from': self.web3.eth.accounts[0],
            'nonce': self.web3.eth.get_transaction_count(self.web3.eth.accounts[0])
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
        return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction) 
