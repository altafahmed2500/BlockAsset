// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "C:/Users/altaf/Desktop/Block-Assets-API/BlockAsset/media/contracts/node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract TestCode {
    string public message;

    constructor(string memory _message) {
        message = _message;
    }

    function updateMessage(string memory _newMessage) public {
        message = _newMessage;
    }
}