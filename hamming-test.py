#!/bin/python3
from bitstring import BitArray
from cyclone import hash, str2hex

tweak="3re6Gbl3QQR4obuf"

# Define your 4 hashes as hex strings
test_hashes = []

test_string="Hello, World!"

for i in range(len(test_string)):
	string=[*test_string]
	string[i]=chr(ord(string[i])+1)
	string=''.join(string)
	print(string)
	test_hashes.append(str2hex(hash(string,tweak=tweak)[0]))


# Convert hex strings to BitArray (128 bits each)
hashes_bits = [BitArray(hex=h) for h in test_hashes]

# Function to calculate Hamming distance
def hamming_distance(bits1, bits2):
	return (bits1 ^ bits2).count(1)

differences=[]

# Compare all pairs and print results
for i in range(len(hashes_bits)):
	for j in range(i + 1, len(hashes_bits)):
		dist = hamming_distance(hashes_bits[i], hashes_bits[j])
		percent = (dist / len(hashes_bits[i])) * 100
		differences.append(percent)
		print(f"Pair {i+1} vs {j+1}: {dist} bits different ({percent:.2f}%)")

avg=0
for i in differences:
	avg+=i
avg/=len(differences)

print(f"Average percent difference: {round(avg,3)}% (Optimal: ~50%)")
