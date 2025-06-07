#!/bin/python3
import random
import string
import sys

def generateTweak(length=16):
	return ''.join(random.choices(string.ascii_letters+string.digits, k=length))

def msg2ord(msg):
	return list(map(ord,[*msg]))


def rotListLeft(data):
	data.append(data.pop(0))

	
def mix(state, chunk, tweak):
	new_state=[0]*len(state)
	
	#print(f"Stats:\n  Current state: {state}\n  Selected chunk: {chunk}\n  State length: {len(state)}\n  Chunk length: {len(chunk)}")
	for i in range(len(state)):
		#print("--------------------")
		#Add state and chunk (mod 256)
		s=(state[i]+chunk[i])%256
		#print(f"Added {state[i]} and {chunk[i]} (mod 256) to get {s}")
		
		#XOR the tweak with the accumulation to cause the tweak to diffuse widely
		s=s^tweak[i]
		
		#Use neighbor value to introduce non-linearity into the hash and create dependency across the hash..
		#Use (i+1)%len(state) to wrap around.
		neighbor=state[(i+1)%len(state)]
		#print(f"Collected neighbor value {neighbor}")
		
		#Rotate the neighbor left by (i&8)
		rotation=((neighbor << (i % 8)) & 0xFF) | (neighbor >> (8 - (i % 8)))
		#print(f"Generated left rotation from {neighbor} to {rotation}")
		'''
		The code above effectively demonstrates a bitwise left rotation, which is a shift with preservation of the high bits by wrapping them around instead of allowing them to go past the 8th bit.
		1. (i % 8) : ensures the number of bits to rotate is between 0 and 7
		2. (neighbor << (i % 8)) & 0xFF : shifts bits in neighbor left by the above (i%8) value. The & 0xFF following ensures that, after the shift, only the lower 8 bits are kept. Any past 8 are temporarily discarded. This is called a mask.
		3. (8 - (i % 8)) : Calculates how many positions to shift right in order to catch the bits that "fell off" the left end
		4. neighbor >> (8 - (i % 8)) shifts the original value to the right by the above amount. With the right shift, they're now in the lower bits
		5. | : merge both the masked left shift and the right shift
		
		reminder of bitwise operators:
		>> : shift right
		<< : shift left
		&  : Bitwise AND
		|  : Bitwise OR
		
		'''
		new_state[i]=s^rotation
		#print(f"Setting new hash[{i}] to {s}^{rotation} ({s^rotation})")
	return new_state

def chunk(byteList, msg_length, chunkByteSize=16):
	# pad message
	data=byteList
	if len(data)%chunkByteSize!=0:
		data.append(128)
	while len(data)%chunkByteSize!=0:
		data.append(0)
	#print(f"Padded message to {len(data)} ({data})")
	# chunk message
	chunked=[data[(i*chunkByteSize):(i*chunkByteSize)+chunkByteSize] for i in range(len(data)//chunkByteSize)]
	chunked+=[[msg_length]*chunkByteSize]
	return chunked
	
def hashAlg(chunkList, tweak, rounds=40):
	# initialize hash
	hash=[]
	for i in range(len(chunkList[0])):
		hash.append(0)
	# shift each chunk
	for i in range(len(chunkList)):
		for j in range(i):
			rotListLeft(chunkList[i])
		#print(f"Shifted {orig} to {chunkList[i]} (Shift rounds: {i})")
	#print("----------")
	
	# Hash
	for r in range(rounds):
		for i in range(len(chunkList)):
			#print(f"XORing {chunkList[i]} with hash ({hash})")
			hash=mix(hash,chunkList[i],tweak)
	return hash

def cleanupHash(hash:list):
	cleaned=list(map(chr,hash))
	cleaned=''.join(cleaned)
	return cleaned

def hash(message, chunkLength=32, tweak=None):
	message=msg2ord(message)
	#print(f"Converted message into {message}")
	if tweak!=None and len(tweak)!=chunkLength:
		raise Exception(f"Tweak length must be {chunkLength} bytes long (Tweak {tweak} is {len(tweak)})")
	if tweak==None:
		tweak=generateTweak(chunkLength)

	tweakOrds=msg2ord(tweak)
	
	chunks=chunk(message, len(message), chunkLength)
	#print(f"Chunked message to {chunks}")
	return (cleanupHash(hashAlg(chunks, tweakOrds)),tweak)

def str2hex(string):
	return bytes([ord(i) for i in string]).hex()

def toInt(hash_string):
	data=list(map(lambda x: format(ord(x),'08b'), [*hash_string]))
	return int(''.join(data),2)

help='''Usage: ./hash.py <message> <tweak>

Takes in a string message parameter and an optional string tweak parameter and produces a hash output. If a tweak isn't provided, one is generated.
	
Examples:\n\t./hash.py \"Hello World!\"\n\t./hash.py \"Foo\" \"3GZO9NUL67pABvIZ\"

'''

if __name__ == "__main__":
	msg=None
	
	try:
		msg=sys.argv[1]
	except:
		try:
			msg=sys.stdin.read()
		except KeyboardInterrupt:
			pass
	try:
		tweak=sys.argv[2]
	except:
		tweak=None

	h=hash(msg, chunkLength=32, tweak=tweak)
	print(f"cyclone:{str2hex(h[0])}:{(h[1])}")
	
	#Old formatting
	#out=hash(msg, chunkLength=32, tweak=tweak)
	#print(f"Hash: {str2hex(out[0])}\nTweak: {out[1]}")
	
'''
How it works:
	1. Did we get a tweak value? If not, generate one.
	2. Pad the input data until it's a multiple of 16 bytes
	3. Split the data into 16 byte chunks
	4. Rotate the data left by the index it's at in the list of chunks
	5. For every byte, add the current chunk byte at index i to the current state byte at index i modulo 256 and save as s
	6. XOR the tweak byte at index i with the value from above. This causes it to diffuse widely.
	7. Use the neighboring value in the state at index i to introduce interdependecy among bytes, and create a temporary left rotation from that byte by i mod 8
	8. Set state[i] to the XOR of the rotation above and the s value
	9. Repeat steps 5-8 40 times
'''
