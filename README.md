# Cyclone Hash Algorithm
A modular, state-interdependent hash algorithm with tweak-based diffusion.

## Security Test Stats:
- Hamming distance between small changes ("Hello, World!" vs "Hfllo, World!" vs "Hello, Wprld!") averages ~49%
- In a trial running "msg0000" to "msg9999", the changes in the hash bytes were almost fully evenly distributed. The amount of changes (per byte) were [9962, 9964, 9956, 9957, 9953, 9965, 9958, 9971, 9965, 9963, 9949, 9961, 9964, 9952, 9965, 9960]
- With multiple birthday-paradox-influenced collision detection tests with randomly generated input strings, no collisions have been found

For reference: the best scores for each test are the following:
- Hamming distance: 50%.
- Byte Diffusion: graphs of the amount of changes per byte should be flat or almost flat.
- Birthday paradox collisions: 0 collisions.

Note: tests were performed with a constant tweak value, which indicates that the use of a tweak value increases the strength of the hash beyond the test results above.

## Background
Originally, I did this to give myself an introduction to hash algorithms and how they work internally, but through multiple hours of wondering what I could do better and the occasional eureka moment, my "introductory exercise" became Cyclone.

---

*Developed independently by Samuel Joseph Poyner (Blooper7) and licensed under the MIT license*
