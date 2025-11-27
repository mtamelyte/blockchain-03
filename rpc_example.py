# `rpc_example.py` example
import fix_bitcoin_ssl
from bitcoin.rpc import RawProxy
# Create a connection to local Bitcoin Core node
p = RawProxy(btc_conf_file=r'D:\LocalData\Bitcoin\bitcoin.conf')
# Run the getblockchaininfo command, store the resulting data in info
info = p.getblockchaininfo()
# Retrieve the 'blocks' element from the info
print(info['blocks'])