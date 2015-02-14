from flask import Flask, request
from GraphProcessor import GraphProcessor
import BidRiggingDetection
import RelationshipEvaluator

app = Flask("test")

@app.route("/bid/rigging/detection", methods=["POST"])
def query_bid_rigging_detection():
	req = request.get_json()
	id = req["id"]
	company_list = req["company"].split(",")
	return("id: " + id + " company: " + ",".join(company_list))

@app.route("/bid/rigging/list", methods=["POST"])
	req = request.get_json()
	id = req["id"]
	return("id: " + id)
	

if __name__ == '__main__':
	app.run(host="0.0.0.0", port="80", debug=False)
