// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IToken {
    function transfer(address recipient, uint256 amount) external returns (bool);
}

contract MessageReward {

    address public owner;
    IToken public token;
    mapping(address => uint256) public rewards;

    event MessageReceived(address indexed user, string message, uint256 reward);

    constructor(address _tokenAddress) {
        owner = msg.sender;
        token = IToken(_tokenAddress);
    }

    // Function to reward user with 0.01 tokens
    function sendMessageAndReward(string memory message) public {
        // Store the message in decentralized storage (IPFS or similar)
        string memory storedMessage = storeMessage(message);
        
        // Reward the user with 0.01 tokens (adjust token decimals accordingly)
        uint256 rewardAmount = 0.01 * 10**18; // Example for 18 decimals
        require(token.transfer(msg.sender, rewardAmount), "Transfer failed");

        // Emit event with the user's address, message, and reward
        emit MessageReceived(msg.sender, storedMessage, rewardAmount);
    }

    // Function to simulate decentralized storage (IPFS or decentralized storage API)
    function storeMessage(string memory message) internal pure returns (string memory) {
        // Here, you would interact with IPFS or other decentralized storage APIs
        // For simplicity, we just return the message.
        return message;
    }

    // Allow owner to withdraw tokens if needed
    function withdrawTokens(address to, uint256 amount) public {
        require(msg.sender == owner, "Only owner can withdraw");
        require(token.transfer(to, amount), "Withdrawal failed");
    }
}
