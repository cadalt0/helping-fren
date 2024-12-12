import React, { useState } from 'react';
import './GetPortfolio.css'; // Import the CSS file

const GetPortfolio = ({ authToken }) => {
  const [portfolio, setPortfolio] = useState([]);
  const [showPortfolio, setShowPortfolio] = useState(false);
  const [showCode, setShowCode] = useState(false);
  const [error, setError] = useState(null);

  const fetchPortfolio = async () => {
    try {
      const response = await fetch('https://sandbox-api.okto.tech/api/v1/supported/tokens', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });

      const data = await response.json();
      if (data.status === 'success') {
        setPortfolio(data.data.tokens); // Set the portfolio data
        setError(null);
        setShowPortfolio(true); // Show portfolio data after fetching
      } else {
        setError('Failed to fetch portfolio data.');
      }
    } catch (err) {
      setError('Error fetching portfolio: ' + err.message);
    }
  };

  return (
    <div className="portfolio-container">
      <button onClick={fetchPortfolio} className="toggle-code">Show Portfolio</button>
      {showPortfolio && (
        <div className="portfolio-box">
          <h3>Portfolio Tokens</h3>
          <ul>
            {portfolio.map((token, index) => (
              <li key={index}>
                <strong>Token Name:</strong> {token.token_name}<br />
                <strong>Token Address:</strong> {token.token_address}<br />
                <strong>Network Name:</strong> {token.network_name}
              </li>
            ))}
          </ul>
          <button onClick={() => setShowCode(!showCode)} className="toggle-code">
            {showCode ? 'Hide Code Data' : 'Show Code Data'}
          </button>
          {showCode && (
            <div className="code-data">
              <pre>{JSON.stringify(portfolio, null, 2)}</pre> {/* Display code data */}
            </div>
          )}
          <button onClick={() => setShowPortfolio(false)} className="toggle-code">
            Hide Portfolio
          </button>
        </div>
      )}
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default GetPortfolio;
