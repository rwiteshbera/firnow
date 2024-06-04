// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FIRManagement {
    
    struct FIR {
        string victimName;
        string accusedNames;
        string subject;
        string description;
        string state;
        string district;
        address thanaAddress;
        string documentHash;
        uint256 firId;
        address lodgedBy;
        uint256 timestamp;
        string status;
    }
    
    FIR[] public firs;
    mapping(address => uint256[]) public firsByVictim;
    mapping(address => uint256[]) public firsByThana;
    mapping(uint256 => FIR) public firById;

    event FIRLodged(
        uint256 firId,
        string victimName,
        string accusedNames,
        string subject,
        string description,
        string state,
        string district,
        address thanaAddress,
        string documentHash,
        address lodgedBy,
        uint256 timestamp,
        string status
    );

    event FIRStatusUpdated(
        uint256 firId,
        string status
    );

    modifier onlyPolice(address _thanaAddress) {
        require(msg.sender == _thanaAddress, "Not authorized");
        _;
    }

    function lodgeFir(
        string memory _victimName,
        string memory _accusedNames,
        string memory _subject,
        string memory _description,
        string memory _state,
        string memory _district,
        address _thanaAddress,
        string memory _documentHash,
        uint256 _firId,
        string memory _status
    ) public {
        FIR memory newFIR = FIR({
            victimName: _victimName,
            accusedNames: _accusedNames,
            subject: _subject,
            description: _description,
            state: _state,
            district: _district,
            thanaAddress: _thanaAddress,
            documentHash: _documentHash,
            firId: _firId,
            lodgedBy: msg.sender,
            timestamp: block.timestamp,
            status: _status
        });
        
        firs.push(newFIR);
        firById[_firId] = newFIR;
        firsByVictim[msg.sender].push(_firId);
        firsByThana[_thanaAddress].push(_firId);

        emit FIRLodged(
            _firId,
            _victimName,
            _subject,
            _accusedNames,
            _description,
            _state,
            _district,
            _thanaAddress,
            _documentHash,
            msg.sender,
            block.timestamp,
            _status
        );
    }

    function getMyFIRs() public view returns (uint256[] memory) {
        return firsByVictim[msg.sender];
    }

    function getThanaFIRs() public view returns (uint256[] memory) {
        return firsByThana[msg.sender];
    }

    function getFIRDetails(uint256 _firId) public view returns (FIR memory) {
        return firById[_firId];
    }

    function updateFIRStatus(uint256 _firId, string memory _status) public onlyPolice(firById[_firId].thanaAddress) {
        FIR storage fir = firById[_firId];
        fir.status = _status;

        emit FIRStatusUpdated(_firId, _status);
    }
}
