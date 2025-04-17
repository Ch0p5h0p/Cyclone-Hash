# Cyclone Hashing Algorithm
A hashing algorithm. Testing is still in progress, but the results are promising!

## Stats:
- Hamming distance between small changes ("Hello, World!" vs "Hfllo, World!" vs "Hello, Wprld!") averages ~49%
- In a trial running "msg0000" to "msg9999", the changes in the hash bytes were almost fully evenly distributed. The amount of changes (per byte) were [9962, 9964, 9956, 9957, 9953, 9965, 9958, 9971, 9965, 9963, 9949, 9961, 9964, 9952, 9965, 9960]
- With a birthday-paradox-influenced collision detection test with randomly generated input strings, no collisions were found.

## Why did you do this?
I did this to give myself an introduction to hashing algorithms and how they work internally.

## Specs / Whitepaper coming soon!!!
