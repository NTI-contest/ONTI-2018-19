import requests

from time import sleep
from ethereum.utils import privtoaddr
from checkers import check_pin_code
from config import get
from subprocess import check_output
import re
from web3 import Web3

from output_util import print_error

RPC_URL = get('network.rpcUrl')

web3 = Web3(Web3.HTTPProvider(RPC_URL))

try:
    PRIVATE_KEY = bytes.fromhex(get('network.privKey'))
except:
    PRIVATE_KEY = bytes(1)

DEFAULT_GAS = 100000

EMPTY_ADDRESS = '0x0000000000000000000000000000000000000000'

try:
    GAS_PRICE = int(1000000000 * requests.get(get('network.gasPriceUrl')).json()['fast'])
except requests.exceptions.RequestException:
    GAS_PRICE = get('network.defaultGasPrice')

REGISTRAR_ADDRESS = get('registrar.registrar.address')
CERTIFICATES_ADDRESS = get('registrar.payments.address')

compiled_registrar = check_output(["solc", "--optimize", "--bin", "--abi", "./Registrar.sol"]).decode()
compiled_registrar_abi = re.findall("ABI \\n(.*?)\\n", compiled_registrar)[0]
compiled_registrar_bytecode = re.findall("Binary: \\n(.*?)\\n", compiled_registrar)[0]

compiled_certificates = check_output(["solc", "--optimize", "--bin", "--abi", "Certificates.sol"]).decode()
compiled_certificates_abi = re.findall("ABI \\n(.*?)\\n", compiled_certificates)[0]
compiled_certificates_bytecode = re.findall("Binary: \\n(.*?)\\n", compiled_certificates)[0]

registrar = web3.eth.contract(address=REGISTRAR_ADDRESS,
                              abi=compiled_registrar_abi)
certificates = web3.eth.contract(address=CERTIFICATES_ADDRESS,
                                 abi=compiled_certificates_abi)


def check_registrar():
    if REGISTRAR_ADDRESS is None:
        print_error('No contract address')

    b1 = web3.eth.getCode(REGISTRAR_ADDRESS).hex()[2:]
    b2 = compiled_registrar_bytecode
    if b1 != b2[-len(b1):]:
        print_error('Seems that the contract address is not the registrar contract')


def check_certificates():
    if CERTIFICATES_ADDRESS is None:
        print_error('No contract address')

    b1 = web3.eth.getCode(CERTIFICATES_ADDRESS).hex()[2:]
    b2 = compiled_certificates_bytecode
    if b1 != b2[-len(b1):]:
        print_error('Seems that the contract address is not the certificates contract')


def private_key_to_address(private_key):
    return web3.toChecksumAddress(privtoaddr(private_key).hex())


def build_and_send_tx(private_key, to='', data='', value=0, nonce=None, gas_estimation=True, message=None):
    address = private_key_to_address(private_key)
    if nonce is None:
        nonce = web3.eth.getTransactionCount(address)
    tx = {
        'from': address,
        'to': to,
        'nonce': nonce,
        'data': data,
        'value': value,
        'gasPrice': GAS_PRICE
    }

    tx['gas'] = web3.eth.estimateGas(tx) if gas_estimation else DEFAULT_GAS

    signed = web3.eth.account.signTransaction(tx, private_key)

    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

    if message is not None:
        print(message)

    return wait_tx_receipt(tx_hash)


def encode_int(x, base=10):
    if type(x) == str:
        x = int(x, base)
    return x.to_bytes(32, byteorder='big')


# Waits until transaction is mined
def wait_tx_receipt(tx_hash, sleep_interval=0.5):
    while True:
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        sleep(sleep_interval)


def get_owner_nonce():
    return web3.eth.getTransactionCount(private_key_to_address(PRIVATE_KEY))


# Deploys compiled contract, returns its address
def deploy_contract(contract_name, nonce):
    bytecode = ''
    if contract_name == 'registrar':
        bytecode = compiled_registrar_bytecode
    elif contract_name == 'certificates':
        bytecode = compiled_certificates_bytecode

    tx_receipt = build_and_send_tx(PRIVATE_KEY, data=bytecode, nonce=nonce)

    return {"address": tx_receipt['contractAddress'], "startBlock": tx_receipt['blockNumber']}


def get_owner():
    return registrar.functions.owner().call()


def get_requests(filter_type):
    requests = []

    head_addr = registrar.functions.headAddr().call()
    tail_addr = registrar.functions.tailAddr().call()
    node = registrar.functions.requests(head_addr).call()
    while node[1] != tail_addr:
        address = node[1]
        node = registrar.functions.requests(address).call()
        if filter_type == node[2]:
            requests += [(node[3], address)]
    return requests


def get_reg_requests():
    return get_requests(3)


def get_del_requests():
    return get_requests(4)


def change_owner(new_owner):
    if get_owner() != private_key_to_address(PRIVATE_KEY):
        print_error('Request cannot be executed')

    build_and_send_tx(PRIVATE_KEY, REGISTRAR_ADDRESS,
                      web3.keccak(text='transferOwnership(address)')[:4] + encode_int(new_owner[2:], 16))


def get_request_type(address):
    return registrar.functions.requests(address).call()[2]


def register_request(user_private_key, phone_number):
    try:
        tx_receipt = build_and_send_tx(user_private_key, REGISTRAR_ADDRESS,
                                       web3.keccak(text='registerRequest(uint256)')[:4] + encode_int(phone_number))

        return tx_receipt['transactionHash'].hex()
    except ValueError as err:
        if err.args[0]['code'] == -32016:
            request_type = get_request_type(private_key_to_address(user_private_key))
            if request_type == 3:
                print_error('Registration request already sent')
            else:
                print_error('Such phone number already registered')
        if err.args[0]['code'] == -32010:
            print_error('No funds to send the request')


def delete_request(user_private_key):
    request_type = get_request_type(private_key_to_address(user_private_key))
    try:
        tx_receipt = build_and_send_tx(user_private_key, REGISTRAR_ADDRESS, web3.keccak(text='deleteRequest()')[:4])

        return tx_receipt['transactionHash'].hex()
    except ValueError as err:
        if err.args[0]['code'] == -32016:
            if request_type == 4:
                print_error('Unregistration request already sent')
            else:
                print_error('Account is not registered yet')
        if err.args[0]['code'] == -32010:
            print_error('No funds to send the request')


def cancel_request(user_private_key):
    request_type = get_request_type(private_key_to_address(user_private_key))
    try:
        tx_receipt = build_and_send_tx(user_private_key, REGISTRAR_ADDRESS, web3.keccak(text='cancelRequest()')[:4])

        return request_type, tx_receipt['transactionHash'].hex()
    except ValueError as err:
        if err.args[0]['code'] == -32016:
            if request_type == 0:
                print_error('No requests found')
        if err.args[0]['code'] == -32010:
            print_error('No funds to send the request')


def confirm(address):
    if get('network.privKey') is None:
        print_error('No admin account found')

    try:

        tx_receipt = build_and_send_tx(PRIVATE_KEY,
                                       REGISTRAR_ADDRESS,
                                       web3.keccak(text='confirm(address)')[:4] + encode_int(address[2:], 16),
                                       gas_estimation=False)

        return tx_receipt['status'], tx_receipt['transactionHash'].hex()
    except ValueError as err:
        if err.args[0]['code'] == -32010:
            print_error('No funds to confirm the request')


def create_approval(user_private_key, value, time_to_expire):
    try:
        tx_receipt = build_and_send_tx(user_private_key, CERTIFICATES_ADDRESS,
                                       web3.keccak(text='approve(uint256)')[:4] + encode_int(time_to_expire),
                                       value)

        id_hex = tx_receipt['logs'][0]['topics'][1]

        message = web3.eth.account.signHash(id_hex, user_private_key)

        return id_hex.hex()[2:] + message['signature'].hex()[2:]
    except ValueError as err:
        if err.args[0]['code'] == -32010:
            print_error('No funds to create a certificate')


def use_approval(user_private_key, message):
    id = message[:64]
    r = message[64:128]
    s = message[128:192]
    v = message[192:]

    build_and_send_tx(user_private_key, CERTIFICATES_ADDRESS,
                      web3.keccak(text='useApproval(bytes32,uint8,bytes32,bytes32)')[:4]
                      + bytes.fromhex(id)
                      + encode_int(v, 16)
                      + bytes.fromhex(r)
                      + bytes.fromhex(s))

    return id


def cancel_approvals(user_private_key):
    build_and_send_tx(user_private_key, CERTIFICATES_ADDRESS,
                      web3.keccak(text='cancel()')[:4])


def send_transaction(user_private_key, to, value):
    try:
        addr = phone_to_address(to)
        if addr is None:
            print_error('No account with the phone number +%s' % to)
        tx_receipt = build_and_send_tx(user_private_key, to=addr, value=value,
                                       message='Payment of %s to +%s scheduled' % (normalize_value(value), to))
        return tx_receipt['transactionHash'].hex()
    except ValueError as err:
        if err.args[0]['code'] == -32010:
            print_error('No funds to send the payment')


def pin_code_to_private_key(pin_code):
    pin_code = check_pin_code(pin_code)
    person_id = get('person.id')
    if person_id is None:
        print_error('ID is not found')
    return get_private_key(person_id, pin_code)


# Evaluate private key by id and pin_code
def get_private_key(person_id, pin_code):
    id = bytes.fromhex(person_id.replace('-', ''))

    a = web3.keccak(bytes(0))
    b = web3.keccak(a + id + bytes([int(pin_code[0])]))
    c = web3.keccak(b + id + bytes([int(pin_code[1])]))
    d = web3.keccak(c + id + bytes([int(pin_code[2])]))
    return web3.keccak(d + id + bytes([int(pin_code[3])]))


def normalize_value(value, custom_currency=None):
    if custom_currency is not None:
        return ('%.6f' % web3.fromWei(value, custom_currency)).rstrip('0').rstrip('.') \
               + ' %s' % (custom_currency if custom_currency != 'ether' else 'poa')

    for currency in ['ether', 'finney', 'szabo', 'gwei', 'mwei', 'kwei', 'wei']:
        if web3.fromWei(value, currency) >= 1:
            return ('%.6f' % web3.fromWei(value, currency)).rstrip('0').rstrip('.') \
                   + ' %s' % (currency if currency != 'ether' else 'poa')
    return '0 poa'


def phone_to_address(phone):
    address = registrar.functions.db(int(phone)).call()
    if address == EMPTY_ADDRESS:
        return None
    return address


def address_to_phone(address, block='latest'):
    phone = registrar.functions.db_rev(web3.toChecksumAddress(address)).call(block_identifier=block)

    if phone == 0:
        return 'UNKNOWN'
    return '+%d' % phone


def get_balance(address):
    return web3.eth.getBalance(address)


def check_address(address):
    if not web3.isChecksumAddress(address):
        print_error('Wrong address format')
    return address


def get_tx_list(address):
    return requests.get(
        'https://blockscout.com/poa/sokol/api?module=account&action=txlist&address=%s&startblock=%s' % (
            address, get('registrar.registrar.startBlock'))
    ).json()['result']
