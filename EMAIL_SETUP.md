# Email Setup for Pricely

## Overview
Pricely uses email notifications to alert users when product prices drop below their target. To enable email notifications, you need to configure SMTP settings.

## Quick Setup (Gmail)

### 1. Create App Password
1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to "Security" → "2-Step Verification"
3. Scroll down to "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password

### 2. Create .env File
Create a `.env` file in your project root with these settings:

```env
# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
```

### 3. Restart the Application
After creating the `.env` file, restart your Pricely application for the changes to take effect.

## Alternative Email Providers

### Outlook/Hotmail
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

### Yahoo Mail
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

### Custom SMTP Server
```env
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587
MAIL_USE_TLS=true
```

## Testing Email Notifications

1. **Add a product** to track with a high target price
2. **Use the "Create Test Notification" button** on the Notifications page
3. **Check your email** for the test notification
4. **Monitor real-time notifications** when prices drop

## Troubleshooting

### Common Issues

1. **"Email credentials not configured"**
   - Check that your `.env` file exists and has correct values
   - Ensure no extra spaces or quotes around values

2. **"Authentication failed"**
   - Verify your email and app password are correct
   - Make sure 2FA is enabled on your Google account
   - Use app password, not your regular password

3. **"Connection refused"**
   - Check your firewall settings
   - Verify the SMTP server and port are correct
   - Try different ports (587, 465, 25)

### Debug Mode
Enable debug logging by adding this to your `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=true
```

## Security Notes

- **Never commit** your `.env` file to version control
- **Use app passwords** instead of your main account password
- **Regularly rotate** your app passwords
- **Monitor** your email account for unusual activity

## Support

If you continue having issues:
1. Check the application logs for error messages
2. Verify your email provider's SMTP settings
3. Test with a different email provider
4. Contact support with specific error messages

---

**Note**: Email notifications are optional. Pricely will continue to work without email configuration, but users won't receive price drop alerts via email.
