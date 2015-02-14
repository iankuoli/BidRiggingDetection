from flask import Flask, request
from GraphProcessor import GraphProcessor
import BidRiggingDetection
import RelationshipEvaluator

app = Flask("test")

@app.route("/", methods=["POST"])
def query_rig_bid_detection():
	req = request.get_json()
	id = req["id"]
	company_list = req["company"].split(",")
	return("id: " + id + " company: " + ",".join(company_list))

if __name__ == '__main__':
	app.run(host="0.0.0.0", port="80", debug=False)
