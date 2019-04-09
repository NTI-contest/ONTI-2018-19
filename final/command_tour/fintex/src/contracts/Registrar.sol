pragma solidity ^0.5.2;


contract Registrar {
    event Register(uint indexed phone_number, address addr);
    event Unregister(uint indexed phone_number);
    event RegistrationRequest(address indexed sender);
    event UnregistrationRequest(address indexed sender);
    event RegistrationCanceled(address indexed sender);
    event UnregistrationCanceled(address indexed sender);
    event RegistrationConfirmed(address indexed sender);
    event UnregistrationConfirmed(address indexed sender);

    struct Account {
        uint phone;
        address addr;
    }

    enum NodeType {
        NONE, HEAD, TAIL, REG, DEL
    }

    struct Node {
        address prev;
        address next;
        NodeType t;
        uint data;
    }

    // Double linked list
    address public headAddr = address(0);
    address public tailAddr = address(2 ** 160 - 1);
    // Sender => Request node
    mapping(address => Node) public requests;

    address public owner;

    // Phone number => Address
    mapping(uint => address) public db;

    // Address => Phone number
    mapping(address => uint) public db_rev;

    constructor() public {
        owner = msg.sender;
        // head
        requests[headAddr] = Node(headAddr, tailAddr, NodeType.HEAD, 0);
        // tail
        requests[tailAddr] = Node(headAddr, tailAddr, NodeType.TAIL, 0);
    }

    // Only contract owner can call these methods
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function transferOwnership(address _owner) onlyOwner public {
        owner = _owner;
    }


    function registerRequest(uint phone) public {
        require(phone <= 1e12);
        require(db[phone] == address(0));
        require(requests[msg.sender].t == NodeType.NONE);

        requests[msg.sender].t = NodeType.REG;
        requests[msg.sender].data = phone;

        requests[msg.sender].next = tailAddr;
        requests[requests[tailAddr].prev].next = msg.sender;
        requests[msg.sender].prev = requests[tailAddr].prev;
        requests[tailAddr].prev = msg.sender;

        emit RegistrationRequest(msg.sender);
    }

    function deleteRequest() public {
        require(db_rev[msg.sender] != 0);
        require(requests[msg.sender].t == NodeType.NONE);

        requests[msg.sender].t = NodeType.DEL;

        requests[msg.sender].next = tailAddr;
        requests[requests[tailAddr].prev].next = msg.sender;
        requests[msg.sender].prev = requests[tailAddr].prev;
        requests[tailAddr].prev = msg.sender;

        emit UnregistrationRequest(msg.sender);
    }

    function confirm(address addr) onlyOwner public {
        require(requests[addr].t == NodeType.REG || requests[addr].t == NodeType.DEL);

        if (requests[addr].t == NodeType.REG) {
            db_rev[addr] = requests[addr].data;
            db[db_rev[addr]] = addr;
            emit RegistrationConfirmed(addr);
        }
        else {
            delete db[db_rev[addr]];
            delete db_rev[addr];
            emit UnregistrationConfirmed(addr);
        }
        requests[addr].t = NodeType.NONE;
        requests[requests[addr].prev].next = requests[addr].next;
        requests[requests[addr].next].prev = requests[addr].prev;
    }

    function cancelRequest() public {
        require(requests[msg.sender].t != NodeType.NONE);

        if (requests[msg.sender].t == NodeType.REG)
            emit RegistrationCanceled(msg.sender);
        if (requests[msg.sender].t == NodeType.DEL)
            emit UnregistrationCanceled(msg.sender);

        requests[msg.sender].t = NodeType.NONE;
        requests[requests[msg.sender].prev].next = requests[msg.sender].next;
        requests[requests[msg.sender].next].prev = requests[msg.sender].prev;
    }
}
