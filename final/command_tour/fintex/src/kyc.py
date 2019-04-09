from argparse import ArgumentParser

from blockchain import get_reg_requests, get_del_requests, confirm, phone_to_address, check_address, check_registrar
from checkers import check_phone_number
from output_util import print_error

parser = ArgumentParser(prog='KYC')

parser.add_argument('--list',
                    nargs=1,
                    metavar='REQUEST_TYPE',
                    help='Prints out all requests of given type')
parser.add_argument('--confirm',
                    nargs=1,
                    metavar='ADDRESS',
                    type=check_address,
                    help='Confirms request related to the given address')
parser.add_argument('--get',
                    nargs=1,
                    type=check_phone_number,
                    metavar='PHONE',
                    help='Prints address associated with given phone number')

args = parser.parse_args()

if args.list:
    check_registrar()
    request_type = args.list[0]

    lst = []
    if request_type == 'add':
        lst = sorted(get_reg_requests())
        if len(lst) == 0:
            print_error('No KYC registration requests found')
    elif request_type == 'del':
        lst = sorted(get_del_requests())
        if len(lst) == 0:
            print_error('No KYC unregistration requests found')

    for phone, address in lst:
        print('%s: +%s' % (address, str(phone)))

if args.confirm:
    check_registrar()
    address = args.confirm[0]

    status, tx_hash = confirm(address)

    if status == 1:
        print('Confirmed by %s' % tx_hash)
    else:
        print('Failed but included in %s' % tx_hash)

if args.get:
    check_registrar()
    phone = args.get[0]

    addr = phone_to_address(phone)
    if addr is None:
        print_error('Correspondence not found')
    print('Registered correspondence: %s' % phone_to_address(phone))
