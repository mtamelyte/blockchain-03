from bitcoin.rpc import RawProxy
from hashlib import sha256
import struct

def swap_order(hex_string):
    reversed_str = hex_string[::-1]
    swapped = ''.join([reversed_str[i:i+2][::-1] for i in range(0, len(reversed_str), 2)])
    return swapped

def little_endian(value):
    return struct.pack('<I', value).hex()


p = RawProxy()

hash ="00000000000000000001baec7dc519cd69868f3f6367ad398077453b4e31c993"

block = p.getblock(hash)

version = little_endian(int(block['version']))
prev_hash = swap_order(block['previousblockhash'])
merkle_root = swap_order(block['merkleroot'])
time = little_endian(int(block['time']))
bits = little_endian(int(block['bits'],16))
nonce = little_endian(int(block['nonce']))

hex = version+prev_hash+merkle_root+time+bits+nonce

binary = bytes.fromhex(hex)

sha1 = sha256(binary).digest()
sha2 = sha256(sha1).hexdigest()

final_hash = swap_order(sha2)
