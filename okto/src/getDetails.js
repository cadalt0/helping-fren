import React, { useEffect, useState } from 'react';
import './GetDetails.css'; // Import CSS file for styling

const GetDetails = ({ authToken }) => {
  const [details, setDetails] = useState(null);
  const [error, setError] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [showCode, setShowCode] = useState(false);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const response = await fetch('https://sandbox-api.okto.tech/api/v1/user_from_token', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${authToken}`,
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        setDetails(data.data); // Accessing the data field where email and user_id are located
      } catch (error) {
        console.error('Error fetching details:', error);
        setError(error.message);
      }
    };

    if (authToken) {
      fetchDetails();
    }
  }, [authToken]);

  return (
    <div className="details-container">
      <button onClick={() => setShowDetails(!showDetails)} className="toggle-details">
        {showDetails ? 'Hide User Details' : 'Show User Details'}
      </button>
      {error && <p className="error-message">Error: {error}</p>}
      {showDetails && details && (
        <div className="details-box">
          <h3>User Details</h3>
          <ul>
            <li><strong>Email:</strong> {details.email}</li>
            <li><strong>User ID:</strong> {details.user_id}</li>
          </ul>
          <button onClick={() => setShowCode(!showCode)} className="toggle-code">
            {showCode ? 'Hide Code Data' : 'Show Code Data'}
          </button>
          {showCode && (
            <div className="code-data">
              <pre>{JSON.stringify(details, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default GetDetails;
