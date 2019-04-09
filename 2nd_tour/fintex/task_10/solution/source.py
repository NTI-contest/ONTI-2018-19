from ethereum.utils import privtoaddr

from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://sokol.poa.network'))
p_size = 1

uuid = 'f4a0a066-527e-4b44-92c4-b1c71fb3d0ce'
pin = '7530'

id = web3.toBytes(hexstr='0x' + uuid.replace('-', ''))

a = web3.sha3(bytes(0))
b = web3.sha3(a + id + bytes([int(pin[0])]))
c = web3.sha3(b + id + bytes([int(pin[1])]))
d = web3.sha3(c + id + bytes([int(pin[2])]))
e = web3.sha3(d + id + bytes([int(pin[3])]))

addr = web3.toChecksumAddress(privtoaddr(e).hex())

print(web3.eth.getBalance(addr))
