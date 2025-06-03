#!/bin/python3
#According to the birthday paradox, we don't need to test EVERY input. Just some of them.

import random
import string
from cyclone import hash, str2hex
import timeit
used_inputs=[]
seen_hashes=[]
tweak="iBLXtUfAjUWUN9Y2lXZKTt7VskJYqJkv" #"3re6Gbl3QQR4obuf"
hash_len=len(tweak)

collisions=[]
tests=10000 #2**64 is the optimal amount, but I'm running on a 4GB RAM laptop so...

for _ in range(tests):
	rand_input=''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1,1000)))
	while rand_input in used_inputs:
		rand_input=''.join(random.choices(string.ascii_letters + string.digits, k=8))
	used_inputs.append(rand_input)
	
	hash_val=str2hex(hash(rand_input,hash_len,tweak=tweak)[0])
	print(f"Operating on {rand_input}\t{hash_val}\t{round(100*(_/tests),10)}% done")
	
	# Check if we've seen this hash before (collision)
	if hash_val in seen_hashes:
		print(f"Collision found with input: {rand_input}")
		collisions.append(rand_input)
	seen_hashes.append(hash_val)


print(f"Collision percent: {100*(len(collisions)/tests)}%")
print(f"{len(collisions)} collisions")
print(collisions)
