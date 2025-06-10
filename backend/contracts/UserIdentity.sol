
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UserIdentity {
    struct Identity {
        address owner;
        bytes32 imeiRoot;
        bytes32 emailRoot;
        uint256 created;
    }
   
    mapping(bytes32 => Identity) public identities;
    event IdentityRegistered(bytes32 indexed uuid, address owner);

    function registerUser(bytes32 imeiRoot, bytes32 emailRoot) external {
        bytes32 uuid = keccak256(abi.encodePacked(imeiRoot, emailRoot));
        require(identities[uuid].created == 0, "Identity exists");
       
        identities[uuid] = Identity({
            owner: msg.sender,
            imeiRoot: imeiRoot,
            emailRoot: emailRoot,
            created: block.timestamp
        });
       
        emit IdentityRegistered(uuid, msg.sender);
    }
   
    function verifyOwnership(bytes32 uuid, address claimant) external view returns (bool) {
        return identities[uuid].owner == claimant;
    }
} 
