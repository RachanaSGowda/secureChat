# TODO: Fix Decryption Issue in SecureChat

## Information Gathered
- The "same issue" refers to decryption failures when messages are received.
- Private keys are stored in localStorage with key 'priv_' + username.
- If multiple users sign up in the same browser, the private key of the first user is overwritten by the second.
- When the first user receives a message, decryption fails because the private key doesn't match.
- Current error handling shows "[Failed to decrypt message]" without explanation.

## Plan
- [x] Modify the ws.onmessage handler in frontend/chat.html to add better error handling for decryption failures.
- [x] Check if the private key (priv) is null or undefined, and alert the user to log in again.
- [x] If AES key decryption fails, alert that the message may be corrupted or for a different user.
- [x] Enhance the catch block to provide more specific error messages.

## Dependent Files to be edited
- [x] frontend/chat.html: Update the ws.onmessage handler for improved error handling.

## Followup steps
- Test the fix by signing up two users in the same browser.
- Send a message from one user to the other and verify the error message is informative.
- Run Flask backend and WebSocket server as per README.
- Ensure messages decrypt correctly when users are in different browsers or incognito mode.
