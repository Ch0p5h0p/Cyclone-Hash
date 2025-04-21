#!/bin/python3
from hash import hash, str2hex

hashes=[]
tweak="3re6Gbl3QQR4obuf"
amount=100000
for i in range(1,amount):
	index_str=[*str(i)]

	index_str=''.join(index_str)
	i_hash=str2hex(hash("msg"+index_str, tweak=tweak)[0])
	hashes.append(i_hash)
	print(f"Operated on {i}\t{i_hash}\t(string: \"msg{index_str}\")")

hashes_bytes=[]

for i in range(len(hashes)):
	current=[hashes[i][(j*2):(j*2)+2] for j in range(int(len(hashes[i])/2))]
	hashes_bytes.append(current)

change=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in range(1,len(hashes_bytes)):
	for j in range(len(hashes_bytes[i])):
		if hashes_bytes[i][j]!=hashes_bytes[i-1][j]:
			change[j]+=1

print("\nSTATS:")
print(f"Change amounts per byte: {change}")

change_ratios=[]
for i in change:
	change_ratios.append(round(i/(amount-1),3))
print(f"Change ratios (changes/iterations): {change_ratios}")

avg=0
for i in change:
	avg+=i
avg/=len(change)

print(f"Average change: {avg}")

avg_deviation=0
deviations=[]
for i in change:
	avg_deviation+=(i-avg)
	deviations.append(i-avg)
avg_deviation/=len(change)

print(f"Average deviation from mean: {avg_deviation} ({deviations})")
print()
