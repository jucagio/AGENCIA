const { google } = require('googleapis');
const fs = require('fs');
const readline = require('readline');
require('dotenv').config();

const SCOPES = [
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/calendar.readonly',
  'https://www.googleapis.com/auth/drive.readonly',
  'https://www.googleapis.com/auth/tasks.readonly',
];

async function generateToken() {
  // Credentials from environment or command line
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  const redirectUrl = 'urn:ietf:wg:oauth:2.0:oob'; // For desktop apps

  if (!clientId || !clientSecret) {
    console.error('ERROR: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in .env');
    console.error('Get these from Google Cloud Console > Credentials > OAuth 2.0 Client ID');
    process.exit(1);
  }

  const auth = new google.auth.OAuth2(clientId, clientSecret, redirectUrl);

  const authUrl = auth.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });

  console.log('\n=== Google OAuth Authorization ===\n');
  console.log('1. Open this URL in your browser:\n');
  console.log(authUrl);
  console.log('\n2. Grant permission and copy the authorization code\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  rl.question('Paste the authorization code here: ', async (code) => {
    try {
      const { tokens } = await auth.getToken(code);

      console.log('\n✅ Token obtained successfully!\n');
      console.log('Add these values to your .env file:\n');
      console.log(`GOOGLE_CLIENT_ID=${clientId}`);
      console.log(`GOOGLE_CLIENT_SECRET=${clientSecret}`);
      console.log(`GOOGLE_REFRESH_TOKEN=${tokens.refresh_token}`);
      console.log(`GOOGLE_ACCESS_TOKEN=${tokens.access_token}`);
      console.log('\nExpiry:', new Date(tokens.expiry_date).toISOString());

      rl.close();
    } catch (err) {
      console.error('❌ Error obtaining token:', err.message);
      rl.close();
      process.exit(1);
    }
  });
}

generateToken();
