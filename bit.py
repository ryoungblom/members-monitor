
import requests
import json
import time
from datetime import datetime

now = datetime.now()
lastBlockNow = datetime.now()


def jprint(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

#coindesk = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
#print(coindesk.status_code)
#jprint(coindesk.json())

newHeight = 0
eta = 0
cdInfo = 5
passedBool = False

while (True):

	coindesk = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
	#print (coindesk)
	coindeskFeed = coindesk.json()

	if (cdInfo == 5):
		cdInfo = 0
		currentPrice = coindeskFeed["bpi"]["USD"]["rate"]
		timeX = coindeskFeed["time"]["updated"]
		mCapReq = requests.get("https://blockchain.info/q/marketcap")
		mCap = mCapReq.json()
		totalBtcReq = requests.get("https://blockchain.info/q/totalbc")
		totalBTC = totalBtcReq.json()
		txn24Req = requests.get("https://blockchain.info/q/24hrtransactioncount")
		txn24 = txn24Req.json()
		hashrateReq = requests.get("https://blockchain.info/q/hashrate")
		hashrate = hashrateReq.json()
		intervalReq = requests.get("https://blockchain.info/q/interval")
		interval = intervalReq.json()
		btc24Req = requests.get("https://blockchain.info/q/24hrbtcsent")
		btc24 = btc24Req.json()
		txnSizeReq = requests.get("https://blockchain.info/q/avgtxsize")
		txnSize = txnSizeReq.json()
		txnValueReq = requests.get("https://blockchain.info/q/avgtxvalue")
		txnValue = txnValueReq.json()
		unconfReq = requests.get("https://blockchain.info/q/unconfirmedcount")
		unconf = unconfReq.json()
		tpbReq = requests.get("https://blockchain.info/q/avgtxnumber")
		tpb = tpbReq.json()

		print ("")
		print ("*****************************************************************")
		print ("* NETWORK STATUS")
		print ("*****************************************************************")
		print ("*         ")
		print ("* Current Bitcoin price: $" + str(currentPrice))
		print ("* Bitcoin market cap: $" + str(mCap))
		print ("* Total Bitcoins in circulation: " + str(totalBTC))
		print ("* Transactions in last 24 hours: " + str(txn24))
		print ("* Estimated hashrate: " + str(hashrate) + " gigahashes")
		print ("* Average time between blocks: " + str(interval))
		print ("* Bitcoins sent in last 24 hours: " + str((btc24/100000000)))
		print ("* Avg. transaction size (last 1000): " + str(txnSize))
		print ("* Avg. transaction value (last 1000): " + str(txnValue))
		print ("* Pending (unconfirmed) transactions: " + str(unconf))
		print ("* Avg. number of transactions per block: " + str(tpb))
		print ("* Time: " + str(timeX))
		print ("*         ")
		print ("*****************************************************************")
		print ("")



	now = datetime.now().timestamp()
	seconds = now - lastBlockNow.timestamp()
	seconds = round(seconds)
	intervalReq = requests.get("https://blockchain.info/q/interval")
	interval = intervalReq.json()
	interval = round(interval)

	if (seconds <= interval):
		eta = interval - seconds
		passedBool = False
	else:
		eta = seconds - interval
		passedBool = True

	print (" ")
	if (passedBool == False):
		print ("...checking for new block... Next block expected in " + str(eta) + " seconds")
	else:
		print ("...checking for new block... Next block expected ~" + str(eta) + " seconds ago")
	print (" ")
	print (" ")

	currentHeight = newHeight

	blockSearch = requests.get("https://blockchain.info/latestblock")

	#jprint(response.json())

	#print(response.status_code)

	blockFeed = blockSearch.json()

	newHeight = blockFeed["height"]
	if (currentHeight != newHeight and currentHeight != 0):
		lastBlockNow = datetime.now()
		timeX = lastBlockNow.strftime("%H:%M:%S")

		diffReq = requests.get("https://blockchain.info/q/getdifficulty")
		diff = diffReq.json()
		bhReq = requests.get("https://blockchain.info/q/getblockcount")
		bh = bhReq.json()
		rewardReq = requests.get("https://blockchain.info/q/bcperblock")
		reward = rewardReq.json()
		htwReq = requests.get("https://blockchain.info/q/hashestowin")
		htw = htwReq.json()

		print ("")
		print ("***************************************************")
		print ("* NEW BLOCK FOUND!")
		print ("***************************************************")
		print ("")
		print ("                                    .''.       ")
		print ("        .''.      .        *''*    :_\/_:     . ")
		print ("       :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.")
		print ("   .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-")
		print ("  :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'")
		print ("  : /\ : :::::     *_\/_*     -= o =-  /)\    '  *")
		print ("   '..'  ':::'     * /\ *     .'/.\'.   '")
		print ("       *            *..*         :")
		print ("        *")
		print ("         *")
		print ("")
		print ("***************************************************")
		print ("* BLOCK STATS")
		print ("* Time: " + str(timeX))
		print ("* New Bitcoins created: " + str(reward))
		print ("* Difficulty: " + str(diff))
		print ("* Block Height: " + str(bh))
		print ("* Average hashes to solve a block: " + str(htw))
		print ("***************************************************")
		print ("")
		print ("")


	cdInfo = cdInfo + 1
	time.sleep(30)
