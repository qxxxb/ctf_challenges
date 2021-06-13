# Puppet

**Category**: Web \
**Difficulty**: Medium-hard \
**Author**: qxxxb

The flag has a random name in `~/Documents/`. Pwn my browser:
```javascript
const browser = await puppeteer.launch({
  dumpio: true,
  args: [
    '--disable-web-security',
    '--user-data-dir=/tmp/chrome',
    '--remote-debugging-port=5000',
    '--disable-dev-shm-usage', // Docker stuff
    '--js-flags=--jitless' // No Chrome n-days please
  ]
})
```
