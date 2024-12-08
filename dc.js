const axios = require('axios');

const pinMessageToIPFS = async (message) => {
  const apiKey = 'YOUR_PINATA_API_KEY';
  const apiSecret = 'YOUR_PINATA_API_SECRET';
  
  const formData = new FormData();
  formData.append('file', Buffer.from(message), { filename: 'message.txt' });

  try {
    const response = await axios.post('https://api.pinata.cloud/pinning/pinFileToIPFS', formData, {
      headers: {
        'pinata_api_key': apiKey,
        'pinata_secret_api_key': apiSecret
      }
    });

    return response.data.IpfsHash; // Returns the IPFS hash of the stored message
  } catch (error) {
    console.error('Error pinning message to IPFS:', error);
  }
};
