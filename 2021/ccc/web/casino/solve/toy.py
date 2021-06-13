import requests

# url = "http://localhost:3000"
url = "http://192.168.0.21:3000"


def register(user, balance):
    res = requests.get(f"{url}/add_user", params={"user": user})
    print(res.status_code)
    res = requests.get(f"{url}/set_balance", params={"user": user, "balance": balance})
    print(res.status_code)


register("john#1234", 200)
register("jane#4321", 300)
register("bob#9876", 501)
register("twit#9999", 800)
