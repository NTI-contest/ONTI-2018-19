pragma solidity ^0.5.2;


contract Certificates {
    event CertificateCreated(bytes32 indexed id);
    event CertificateUsed(bytes32 indexed id);
    event CertificateWithdrew(bytes32 indexed id);

    struct Approval {
        address sender;
        uint value;
        uint expire_time;
        bytes32 prev;
        bytes32 next;
    }

    mapping(address => uint) public lastN;

    // sha(sender, id) => approval
    mapping(bytes32 => Approval) public approvals;

    // address => last approval ticket
    mapping(address => bytes32) public lastTicket;

    function approve(uint time) public payable {
        require(msg.value > 0);

        bytes32 prevId = lastTicket[msg.sender];
        if (prevId == bytes32(0))
            prevId = keccak256(abi.encodePacked(msg.sender, uint(0)));

        uint n = ++lastN[msg.sender];

        bytes32 id = keccak256(abi.encodePacked(msg.sender, n));
        lastTicket[msg.sender] = id;

        approvals[prevId].next = id;
        approvals[id] = Approval(msg.sender, msg.value, now + time, prevId, bytes32(0));

        emit CertificateCreated(id);
    }

    function cancel() public {
        bytes32 id = keccak256(abi.encodePacked(msg.sender, uint(0)));
        while (approvals[id].next != bytes32(0)) {
            id = approvals[id].next;
            if (now > approvals[id].expire_time)
                cancelApproval(id);
        }
    }

    function cancelApproval(bytes32 ticket) public {
        require(approvals[ticket].value > 0);
        require(approvals[ticket].sender == msg.sender);
        require(now > approvals[ticket].expire_time);

        approvals[approvals[ticket].prev].next = approvals[ticket].next;
        if (approvals[ticket].next != bytes32(0))
            approvals[approvals[ticket].next].prev = approvals[ticket].prev;
        else
            lastTicket[msg.sender] = approvals[ticket].prev;

        msg.sender.transfer(approvals[ticket].value);

        delete approvals[ticket];

        emit CertificateWithdrew(ticket);
    }

    function useApproval(bytes32 ticket, uint8 v, bytes32 r, bytes32 s) public {
        require(approvals[ticket].value > 0);
        require(ecrecover(ticket, v, r, s) == approvals[ticket].sender);
        require(now <= approvals[ticket].expire_time);

        approvals[approvals[ticket].prev].next = approvals[ticket].next;
        if (approvals[ticket].next != bytes32(0))
            approvals[approvals[ticket].next].prev = approvals[ticket].prev;
        else
            lastTicket[msg.sender] = approvals[ticket].prev;

        msg.sender.transfer(approvals[ticket].value);

        delete approvals[ticket];

        emit CertificateUsed(ticket);
    }
}
