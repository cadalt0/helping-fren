import React, { useState } from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import GetDetails from './getDetails';
import GetPortfolio from './GetPortfolio'; // Import the new component

const App = () => {
  const [user, setUser] = useState(null);
  const [authToken, setAuthToken] = useState(null);

  const responseGoogle = async (credentialResponse) => {
    const { credential } = credentialResponse;
    const userInfo = parseJwt(credential);
    setUser(userInfo);

    try {
      const response = await fetch('https://sandbox-api.okto.tech/api/v2/authenticate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Api-Key': 'feb3f1d9-6e5e-49d1-8756-34fa07b15a76',
        },
        body: JSON.stringify({ id_token: credential }),
      });

      const data = await response.json();

      if (data.status === 'success' && data.data && data.data.auth_token) {
        setAuthToken(data.data.auth_token);
        console.log('Auth Token:', data.data.auth_token);
      } else {
        console.warn('auth_token is missing in response');
        setAuthToken(null);
      }
    } catch (error) {
      console.error('Error during API call:', error);
      alert('Error during API call. Please try again.');
    }
  };

  const handleError = (error) => {
    console.error('Login failed:', error);
    alert('Login failed. Please try again.');
  };

  const parseJwt = (token) => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = decodeURIComponent(atob(base64Url).split('').map((c) => `%${('00' + c.charCodeAt(0).toString(16)).slice(-2)}`).join(''));
      return JSON.parse(base64);
    } catch (error) {
      console.error('Error parsing JWT:', error);
      return null;
    }
  };

  return (
    <GoogleOAuthProvider clientId="717715214790-btuiq4rfur25hj9jd72ep0sd6c65k1pe.apps.googleusercontent.com">
      <div style={{ textAlign: 'center', marginTop: '50px' }}>
        <h1>Okto  </h1>
        {user ? (
          <div>
            <h2>Welcome, {user.name}!</h2>
            <img src={user.picture} alt={user.name} />
            <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
              <GetDetails authToken={authToken} />
              <GetPortfolio authToken={authToken} />
            </div>
          </div>
        ) : (
          <GoogleLogin
            onSuccess={responseGoogle}
            onFailure={handleError}
            cookiePolicy={'single_host_origin'}
          />
        )}
      </div>
    </GoogleOAuthProvider>
  );
};

export default App;
