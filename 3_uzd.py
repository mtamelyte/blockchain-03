from bitcoin.rpc import RawProxy

p = RawProxy()

txid = "4410c8d14ff9f87ceeed1d65cb58e7c7b2422b2d7529afc675208ce2ce09ed7d"

raw_tx = p.getrawtransaction(txid)

decoded_tx = p.decoderawtransaction(raw_tx)

total_input = 0
for vin in decoded_tx['vin']:
      prev_txid = vin['txid']
      prev_vout = vin['vout']
      prev_tx = p.getrawtransaction(prev_txid)
      decoded_prev_tx = p.decoderawtransaction(prev_tx)

      input_value = decoded_prev_tx['vout'][prev_vout]['value']
      total_input += input_value

total_output = sum(vout['value'] for vout in decoded_tx['vout'])

fee = (total_input - total_output)*100000000

print(fee)

