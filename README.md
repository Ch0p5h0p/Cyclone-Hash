# Cyclone Hash Algorithm
A modular, state-interdependent hash algorithm with tweak-based diffusion.
[!Note] This is a toy algorithm! It's not intended for real use!
## Usage:
The python script can be run through the terminal with `python3 cyclone.py "message" "tweak"`. 
If no tweak is provided, one will be generated.

You can also import the script and use the provided `hash()` function. The function uses the following parameters:
```
message     : Mandatory, the message you want to hash
chunkLength : The length of chunk to use in bytes. Essentially, this is the length of the output hash in bytes. Default is 32 bytes.
tweak       : The tweak to use with the mixer. If you don't provide one, one will be generated for you.
```
If you just want to quickly hash a message, you can run `hash("Hello, World")`, and a 32 byte (256 bit) hash generated with a random tweak will be returned.

## Security Test Stats:
- Hamming distance between small changes ("Hello, World!" vs "Hfllo, World!" vs "Hello, Wprld!") averages ~49%
- In a trial running "msg0000" to "msg9999", the changes in the hash bytes were almost fully evenly distributed. The amount of changes (per byte) were [9962, 9964, 9956, 9957, 9953, 9965, 9958, 9971, 9965, 9963, 9949, 9961, 9964, 9952, 9965, 9960]
- With multiple birthday-paradox-influenced collision detection tests with randomly generated input strings, no collisions have been found

For reference: the optimal scores for each test are the following:
- Hamming distance: 50%.
- Byte Diffusion: graphs of the amount of changes per byte should be flat or almost flat.
- Birthday paradox collisions: 0 collisions.

Tests were performed with a constant tweak value, which indicates that the use of a tweak value increases the strength of the hash beyond the test results above.

Note: the tests were applied to a 16 byte (128 bit) long hash to increase testing efficiency. The default value is 32 bytes, or 256 bits. Hamming tests and diffusion tests for 32 bytes have similar results (Hamming: ~50.3%, Diffusion: ~99.5% average, or ~9950 average changes)

## Background
Originally, I did this to give myself an introduction to hash algorithms and how they work internally, but through multiple hours of wondering what I could do better and the occasional eureka moment, my "introductory exercise" became Cyclone.

---

*Developed independently by Samuel Joseph Poyner (Blooper7) and licensed under the MIT license*
