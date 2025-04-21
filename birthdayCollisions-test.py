#!/bin/python3
#According to the birthday paradox, we don't need to test EVERY input. Just some of them.

import random
import string
from cycone import hash, str2hex

used_inputs=[]
seen_hashes=[]
tweak="3re6Gbl3QQR4obuf"

tests=100000 #2**64 is the optimal amount, but I'm running on a 4GB RAM laptop so...

for _ in range(tests):
	rand_input=''.join(random.choices(string.ascii_letters + string.digits, k=8))
	while rand_input in used_inputs:
		rand_input=''.join(random.choices(string.ascii_letters + string.digits, k=8))
		used_inputs.append(rand_input)
	
	hash_val=str2hex(hash(rand_input,tweak=tweak)[0])
	print(f"Operating on {rand_input}\t{hash_val}\t{round(100*(_/tests),10)}% done")
	
	# Check if we've seen this hash before (collision)
	if hash_val in seen_hashes:
		print(f"Collision found with input: {rand_input}")
	seen_hashes.append(hash_val)
