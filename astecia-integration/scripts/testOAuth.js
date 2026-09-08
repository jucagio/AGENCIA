const { google } = require('googleapis');
require('dotenv').config();

async function testApis() {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  const refreshToken = process.env.GOOGLE_REFRESH_TOKEN;

  if (!clientId || !clientSecret || !refreshToken) {
    console.error('❌ Missing OAuth credentials in .env file');
    console.error('Run: npm run generate-token first');
    process.exit(1);
  }

  const oauth2Client = new google.auth.OAuth2(clientId, clientSecret);
  oauth2Client.setCredentials({
    refresh_token: refreshToken,
  });

  console.log('\n=== Testing Google APIs ===\n');

  try {
    // Test Gmail API
    console.log('Testing Gmail API...');
    const gmail = google.gmail({ version: 'v1', auth: oauth2Client });
    const messages = await gmail.users.messages.list({ userId: 'me', maxResults: 1 });
    console.log('✅ Gmail API works');

    // Test Calendar API
    console.log('Testing Calendar API...');
    const calendar = google.calendar({ version: 'v3', auth: oauth2Client });
    const events = await calendar.events.list({ calendarId: 'primary', maxResults: 1 });
    console.log('✅ Calendar API works');

    // Test Drive API
    console.log('Testing Drive API...');
    const drive = google.drive({ version: 'v3', auth: oauth2Client });
    const files = await drive.files.list({ pageSize: 1 });
    console.log('✅ Drive API works');

    // Test Tasks API
    console.log('Testing Tasks API...');
    const tasks = google.tasks({ version: 'v1', auth: oauth2Client });
    const tasklists = await tasks.tasklists.list({ maxItems: 1 });
    console.log('✅ Tasks API works');

    console.log('\n🟢 All 4 APIs authenticated and working!');
    console.log('OAuth is ready for Sprint 1\n');
  } catch (err) {
    console.error('❌ Error:', err.message);
    if (err.message.includes('invalid_grant')) {
      console.error('\nYour refresh token may be expired. Run: npm run generate-token');
    }
    process.exit(1);
  }
}

testApis();
