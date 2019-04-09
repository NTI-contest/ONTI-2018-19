from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://sokol.poa.network'))

contract_address = '0x2C7Cc50973b57b2b03f569643e4e604977D4F7fC'
address = '0x2C7Cc50973b57b2b03f569643e4e604977D4F7fC'

# This huge string is just our contract ABI :)
contract = web3.eth.contract(address=contract_address, abi='''[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_value",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_txHash",
				"type": "bytes32"
			},
			{
				"name": "_vout",
				"type": "uint256"
			},
			{
				"name": "_recipients",
				"type": "address[]"
			},
			{
				"name": "_values",
				"type": "uint256[]"
			}
		],
		"name": "transfer",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"payable": true,
		"stateMutability": "payable",
		"type": "fallback"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "tx_source",
				"type": "bytes32"
			},
			{
				"indexed": true,
				"name": "tx_address",
				"type": "bytes32"
			},
			{
				"indexed": true,
				"name": "recipient",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "value",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "vout",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	}
]''')

# Filtering all Transfer events related to given address
filter = contract.events.Transfer().createFilter(
    fromBlock=0,
    toBlock='latest',
    argument_filters={'recipient': address})
events = filter.get_all_entries()

# utxoPool mapping slot number
slot = (2).to_bytes(32, byteorder='big')

ans = set()

for e in events:
    # Evaluating db_key
    key = web3.sha3(e.args['tx_address'] + e.args['vout'].to_bytes(32, byteorder='big'))
    # Evaluating ethereum storage key
    storage_key = web3.sha3(key + slot)
    # Retrieve utxoPool[db_key]
    storage_value = web3.eth.getStorageAt(contract_address, storage_key)

    # if utxoPool[db_key] exists
    if storage_value != bytes(32):
        # recursively go to the root Transfer event (where tx_source is 0x000...00)
        e1 = e
        while e1.args['tx_source'] != bytes(32):
            filter = contract.events.Transfer().createFilter(
                fromBlock=0,
                toBlock='latest',
                argument_filters={'tx_address': e1.args['tx_source']})
            e1 = filter.get_all_entries()[0]

        ans.add(e1.blockNumber)

for x in sorted(ans):
    print(x, end=' ')
