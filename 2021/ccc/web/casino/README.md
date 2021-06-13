# Casino

- Discord bot that lets you bet money
- Also has a web app to view richest users
- Sends badges by taking screenshots of `/badge?user=xxx` on the web app
  - Feature: Users can add custom CSS styles to badges

Goal: Get at least $1000 to get the flag, but this code
```javascript
if (balance + bet >= 1000) myDice = 6
```
makes it impossible.

## Deployment notes

Edit `publicURL` in `deploy/bot/config.json` to be the public URL of the web
server.

During local testing RAM was pretty constant at around 128M. Would probably
want around 512M to be safe when deploying.
