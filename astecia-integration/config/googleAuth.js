/**
 * Google OAuth 2.0 Configuration
 * Setup para Gmail, Calendar, Drive, Tasks APIs
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const SCOPES = [
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/calendar.readonly',
  'https://www.googleapis.com/auth/drive.readonly',
  'https://www.googleapis.com/auth/tasks',
];

/**
 * Load or create OAuth2 client
 * Uses refresh token from .env for automatic re-authentication
 */
function getOAuth2Client() {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  const redirectUrl = process.env.OAUTH_REDIRECT_URL || 'http://localhost:3000/oauth/callback';

  const oauth2Client = new google.auth.OAuth2(
    clientId,
    clientSecret,
    redirectUrl
  );

  // Set refresh token for automatic token refresh
  if (process.env.GOOGLE_REFRESH_TOKEN) {
    oauth2Client.setCredentials({
      refresh_token: process.env.GOOGLE_REFRESH_TOKEN,
    });
  }

  return oauth2Client;
}

/**
 * Generate authorization URL (for first-time setup)
 * User visits this URL to grant permissions
 */
function getAuthUrl() {
  const oauth2Client = getOAuth2Client();

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent',
  });

  return authUrl;
}

/**
 * Exchange authorization code for refresh token
 * Called after user grants permissions
 */
async function getRefreshToken(code) {
  try {
    const oauth2Client = getOAuth2Client();
    const { tokens } = await oauth2Client.getToken(code);

    // ⚠️ SECURITY: Never log actual tokens
    console.log('✅ Refresh token generated successfully');
    console.log('📝 Check your terminal history for the token');
    console.log('💾 Add the token to .env as GOOGLE_REFRESH_TOKEN');

    return tokens.refresh_token;
  } catch (error) {
    console.error('Error getting refresh token:', error);
    throw error;
  }
}

/**
 * Verify credentials are valid
 */
async function verifyAuth() {
  try {
    const oauth2Client = getOAuth2Client();

    // Try to get new access token
    const { credentials } = await oauth2Client.refreshAccessToken();

    console.log('✅ Google OAuth verified');
    return true;
  } catch (error) {
    console.error('❌ Google OAuth invalid:', error.message);
    return false;
  }
}

module.exports = {
  getOAuth2Client,
  getAuthUrl,
  getRefreshToken,
  verifyAuth,
  SCOPES,
};
