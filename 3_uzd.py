# `rpc_transaction.py` example
from bitcoin.rpc import RawProxy
# Create a connection to local Bitcoin Core node
p = RawProxy(btc_conf_file=r'D:\LocalData\bitcoin.conf')

txid = "0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2"

raw_tx = p.getrawtransaction(txid)
# Decode the transaction hex into a JSON object
decoded_tx = p.decoderawtransaction(raw_tx)

fee = decoded_tx.calculate_fee()

print(fee)