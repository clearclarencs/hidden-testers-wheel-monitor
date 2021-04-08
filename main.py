import requests, json, datetime, time

def error(message):
    try:
        with open("accounts.json","r") as r:
            webhook = json.loads(r.read())["webhook"]
        data = {
            "content": "Hidden Wheel Error:\n"+str(message)
        }
        requests.post(webhook, json=data, headers={"Content-Type": "application/json"})
    except:
        print(str(message))
    return

def get(acc):
    try:
        acc_num = str(acc["accnum"])
        headers = {"Cookie":acc["cookies"], "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        res = requests.get("https://products.ahiddensociety.com/"+str(acc_num), headers=headers)
        game_key = res.json()["game_key"]
        if game_key == "nospins":
            return False
        res2 = requests.get("https://products.ahiddensociety.com/"+str(acc_num)+"/"+str(game_key), headers=headers)
        prizeNum = int(json.loads(res2.json()["json"])["spinDestinationArray"][-1])
        send(json.loads(res2.json()["json"])["segmentValuesArray"][prizeNum]["resultText"], acc["webhook"], "https://products.ahiddensociety.com/"+str(acc_num)+"/"+str(game_key))
        return True
    except Exception as e:
        print(e)
        return False

def send(prize, webhook, whole):
    if prize == "LOSER":
        return
    try:
        data={
            "embeds": [
            {
            "author": {
            "name": "",
            "url": "",
            "icon_url": ""
            },  
            "title": prize,
            "timestamp":datetime.datetime.now().isoformat(),
            "url": "https://products.ahiddensociety.com/wheel",
            "description": "||"+str(whole)+"||",
            "color": "16740039",
            "footer":{"text":"A Clearclarencs scraper"},
            }
        ]
        }
        requests.post(webhook, json=data, headers={"Content-Type": "application/json"})
    except Exception as e:
        error(e)
    return

while True:
    with open("accounts.json","r") as r:
        accounts = json.loads(r.read())["accounts"]
    if datetime.datetime.now(datetime.timezone.utc).strftime("%H") == "05":
        success = False
        for acc in accounts:
            for i in range(3):
                if get(acc):
                    success = True
                    break
                else:
                    error("Error on account "+acc["accnum"])
                    time.sleep(300)
            time.sleep(5) # account delay
        if success:
            time.sleep(82800) # wait 23 hours if worked
        else:
            time.sleep(600) # Wait 10 mins if none worked
    else:
        time.sleep(300) #5 min retry

    
    