from time import sleep

from argparse import ArgumentParser

from blockchain import deploy_contract, get_owner, change_owner, get_owner_nonce
from config import set

parser = ArgumentParser(prog='Setup')

parser.add_argument('--deploy',
                    action='store_true',
                    help='Deploys registrar and certificates contracts to the blockchain')
parser.add_argument('--owner',
                    nargs=1,
                    metavar='CONTRACT',
                    help='Prints current owner of the contract')
parser.add_argument('--chown',
                    nargs=2,
                    metavar=('CONTRACT', 'NEW_OWNER'),
                    help='Changes owner of the specified contract')


args = parser.parse_args()

if args.deploy:
    nonce = get_owner_nonce()
    registrar = deploy_contract('registrar', nonce)
    print('KYC Registrar: %s' % registrar['address'])
    set('registrar.registrar', registrar)

    certificates = deploy_contract('certificates', nonce + 1)
    print('Payment Handler: %s' % certificates['address'])
    set('registrar.payments', certificates)

if args.owner:
    contract = args.owner[0]

    if contract == 'registrar':
        print('Admin account: %s' % get_owner())

if args.chown:
    contract = args.chown[0]
    new_owner = args.chown[1]

    if contract == 'registrar':
        change_owner(new_owner)

        print('New admin account: %s' % new_owner)
