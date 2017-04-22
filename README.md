# 15-Puzzle

A [15-Puzzle](https://en.wikipedia.org/wiki/15_puzzle) is a simple game where the player must reorganize a scrambled picture into its original shape. However, this game comes with a twist: Stegonography.

[Steganography](https://en.wikipedia.org/wiki/Steganography) is a method of concealing information inside a seemingly innocuous piece of information. For example, a piece of text inside an image. This 15-Puzzle does this by rewriting the low order bits in the color imformation of the image. This allows the message to be stored with minimal, imperceptible visual changes to the image.

To read a message, press the down key five consecutive moves. The write a message, press the up key five consecutive times. Any PNG image can store a message containing any combination of characters in the string `qwertyuiopasdfghjklzxcvbnm7894561230,./;'-=<>?:_+!@#$%^&*()" \`, with storage density of one character per pixel in the image. An image can have a message written to it, then be emailed to a third party to "secretly" send the message.

## Requirements

1. [Pygame](https://www.pygame.org/news)
2. [PIL](http://www.pythonware.com/products/pil/)