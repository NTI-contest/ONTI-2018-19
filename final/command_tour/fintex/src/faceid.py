from argparse import ArgumentParser
from datetime import datetime

from blockchain import register_request, delete_request, cancel_request, get_balance, \
    private_key_to_address, send_transaction, create_approval, use_approval, cancel_approvals, pin_code_to_private_key, \
    normalize_value, check_registrar, check_certificates, get_tx_list, address_to_phone
from config import get, set, clear
from output_util import print_error
from validators import PINPhoneValidate, TransactValidate, ApproveValidate, PINTicketValidate
from video_detector import simple_identify, identify

parser = ArgumentParser(prog='Faceid service')

parser.add_argument('--find',
                    nargs=1,
                    metavar='VIDEO',
                    help='Identifies person, stores person id in person.json')
parser.add_argument('--actions',
                    action='store_true',
                    help='Generates needed face actions')
parser.add_argument('--add',
                    nargs=2,
                    metavar=('PIN_CODE', 'PHONE_NUMBER'),
                    action=PINPhoneValidate,
                    help='Sends register request')
parser.add_argument('--del',
                    nargs=1,
                    metavar='PIN_CODE',
                    type=pin_code_to_private_key,
                    dest='delete',
                    help='Sends delete request')
parser.add_argument('--cancel',
                    nargs=1,
                    metavar='PIN_CODE',
                    type=pin_code_to_private_key,
                    help='Cancels register or unregister request')
parser.add_argument('--balance',
                    nargs=1,
                    metavar='PIN_CODE',
                    type=pin_code_to_private_key,
                    help='Prints user balance')
parser.add_argument('--send',
                    nargs=3,
                    metavar=('PIN_CODE', 'PHONE_NUMBER', 'VALUE'),
                    action=TransactValidate,
                    help='Sends money to another user')
parser.add_argument('--gift',
                    nargs=3,
                    metavar=('PIN_CODE', 'VALUE', 'EXPIRE_DATE'),
                    action=ApproveValidate,
                    help='Creates approval ticket')
parser.add_argument('--receive',
                    nargs=2,
                    metavar=('PIN_CODE', 'TICKET'),
                    action=PINTicketValidate,
                    help='Receives money via given ticket')
parser.add_argument('--withdraw',
                    nargs=1,
                    metavar='PIN_CODE',
                    type=pin_code_to_private_key,
                    help='Withdraw money from unused ticket')
parser.add_argument('--ops',
                    nargs=1,
                    metavar='PIN_CODE',
                    type=pin_code_to_private_key,
                    help='Prints all operations')
parser.add_argument('--opsall',
                    nargs=1,
                    metavar='PIN_CODE',
                    type=pin_code_to_private_key,
                    help='Prints all operations including certificates')

args = parser.parse_args()

if args.find:
    clear('person')
    video = args.find[0]

    actions = get('actions')
    if actions is None:
        person_id = simple_identify(video)
        set('person.id', person_id)
        print('%s identified' % person_id)
    else:
        person_id = identify(video, actions)
        set('person.id', person_id)
        print('%s identified' % person_id)

if args.actions:
    import json, random

    actions = random.choice([
        {'actions': ["OpenMouth", "YawLeft", "CloseLeftEye"]},
        {'actions': ["OpenMouth", "YawLeft", "CloseRightEye"]},
        {'actions': ["OpenMouth", "CloseRightEye", "YawLeft"]},
        {'actions': ["OpenMouth", "YawRight", "CloseRightEye"]}
    ])
    with open('actions.json', 'w') as out:
        json.dump(actions, out)

if args.add:
    check_registrar()
    private_key = args.add[0]
    phone = args.add[1]

    tx_hash = register_request(private_key, phone)

    print('Registration request sent by %s' % tx_hash)

if args.delete:
    check_registrar()
    private_key = args.delete[0]

    tx_hash = delete_request(private_key)

    print('Unregistration request sent by %s' % tx_hash)

if args.cancel:
    check_registrar()
    private_key = args.cancel[0]

    type, tx_hash = cancel_request(private_key)

    if type == 3:
        print('Registration canceled by %s' % tx_hash)
    else:
        print('Unregistration canceled by %s' % tx_hash)

if args.balance:
    private_key = args.balance[0]
    address = private_key_to_address(private_key)

    print('Your balance is %s' % normalize_value(get_balance(address)))

if args.send:
    check_registrar()
    private_key = args.send[0]
    to = args.send[1]
    value = args.send[2]

    tx_hash = send_transaction(private_key, to, value)

    print('Transaction Hash: %s' % tx_hash)

if args.gift:
    check_certificates()
    private_key = args.gift[0]
    value = args.gift[1]
    expire_time = args.gift[2]

    certificate = create_approval(private_key, value, expire_time)

    print(certificate)

if args.receive:
    check_certificates()
    private_key = args.receive[0]
    certificate = args.receive[1]

    ticket = use_approval(private_key, certificate)

    print(ticket)

if args.withdraw:
    check_certificates()
    private_key = args.withdraw[0]

    cancel_approvals(private_key)

    print('Cancelled approvals')

if args.ops:
    check_registrar()
    check_certificates()

    address = private_key_to_address(args.ops[0]).lower()

    tx_list = get_tx_list(address)

    if len(tx_list) == 0:
        print_error('No operations found')

    print('Operations:')
    for tx in tx_list:
        date = datetime.fromtimestamp(int(tx['timeStamp']))

        if int(tx['blockNumber']) >= get('registrar.registrar.startBlock'):
            if tx['to'] == address:
                from_phone = address_to_phone(tx['from'], int(tx['blockNumber']))
                if from_phone != 'UNKNOWN':
                    print('%s FROM: %s %s' % (
                    date.strftime('%H:%M:%S %d.%m.%Y'), from_phone, normalize_value(int(tx['value']), 'ether')))
            else:
                to_phone = address_to_phone(tx['to'], int(tx['blockNumber']))
                if to_phone != 'UNKNOWN':
                    print('%s   TO: %s %s' % (
                    date.strftime('%H:%M:%S %d.%m.%Y'), to_phone, normalize_value(int(tx['value']), 'ether')))
