import random
import string

def generateSalt(length=16):
	return ''.join(random.choices(string.ascii_letters+string.digits, k=length))

def msg2ord(msg):
	return list(map(ord,[*msg]))

def shiftListRight(data):
	data.insert(0,data.pop())

def chunk(byteList, chunkByteSize=16):
	# pad message
	data=byteList
	while len(data)%16!=0:
		data.append(0)
	#print(f"Padded message to {len(data)} ({data})")
	# chunk message
	chunked=[data[(i*chunkByteSize):(i*chunkByteSize)+chunkByteSize] for i in range(len(data)//chunkByteSize)]
	return chunked
	
def hashAlg(chunkList):
	# initialize hash
	hash=[]
	for i in range(len(chunkList[0])):
		hash.append(0)

	# shift each chunk
	for i in range(len(chunkList)):
		orig=chunkList[i].copy()
		for j in range(i):
			shiftListRight(chunkList[i])
		#print(f"Shifted {orig} to {chunkList[i]} (Shift rounds: {i})")
	#print("----------")
	
	# Hash
	for i in range(len(chunkList)):
		#print(f"XORing {chunkList[i]} with hash ({hash})")
		for j in range(len(chunkList[i])):
			hash[j]=hash[j]^chunkList[i][j]
	return hash

def cleanupHash(hash:list):
	cleaned=list(map(chr,hash))
	cleaned=''.join(cleaned)
	return cleaned

def hash(message, chunkLength=16, salt=None):
	message=msg2ord(message)
	#print(f"Converted message into {message}")
	if salt==None:
		salt=generateSalt(chunkLength)

	saltOrds=msg2ord(salt)
	
	salted=message+saltOrds
	
	chunks=chunk(salted, chunkLength)
	#print(f"Chunked message to {chunks}")
	return (cleanupHash(hashAlg(chunks)),salt)

if __name__ == "__main__":
	hash1=hash("Hello, World! How are you on this wonderful (insert day of the week here)?")
	hash2=hash("Hello, WOrld! How are you on this wonderful (insert day of the week here)?")
	print(f"Hash:{hash1[0].encode('utf-8').hex()}\tSalt:{hash1[1]}")
	print(f"Hash:{hash2[0].encode('utf-8').hex()}\tSalt:{hash2[1]}")
