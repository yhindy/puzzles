# Python Genetic Mutation

## Introduction

Well done! You've graduated from Knight School and are now ready to venture beyond the castle walls. As soon as you step outside the gate, however, you come to a frightening realization. You forgot about the moat! This moat isn't full of crocodiles like usual - instead, it's full of snakes. A very deadly, venomous species of snake - the `Python2`. If you could somehow transform those evil dastardly `Python2` snakes into friendly, lovable `Python3` snakes, then you would be able to pass through the moat and keep questing.

Suddenly, you remember something from your sophomore year biology class. If you can modify the DNA of a dangerous `Python2` snake, it will turn into a harmless `Python3` snakes!

## Overview

For this part of the puzzle, you will write a program to efficiently determine the fewest number of edits required to transform a strand of `Python2` DNA to `Python3` DNA. A edit is defined as either an insertion, deletion, or substitution, and the DNA strands are modeled as strings comprised exclusively from the character set `{'A', 'C', 'G', 'T'}`. In order to get past the moat (and unlock the next zip file), you'll need to count the total number of edits to perform all the transformations in `dna.txt`.

Let's get started.

## General Algorithm

In order to transform one DNA string into another, you could delete all letters in the input and then insert all letters in the output. However, this approach is not efficient, and while this algorithm is running the snakes would bite and poison you. So, you'll need to be more efficient.

The problem of efficiently transforming one string into another requires finding the "minimum edit distance" (also known as Levenshtein distance). For example, the edit distance between `'GATTACA'` and `'CATCAT'` is 4:

```
GATTACA --> GATTAC  (deletion)
GATTAC  --> GATTAT  (substitution)
GATTAT  --> GATCAT  (substitution)
GATCAT  --> CATCAT  (substitution)
```

You can approach this problem recursively. Suppose you're trying to find the minimum edit distance between `start = 'CAAT'` and `end = 'AGT'` - you can use a brute force approach as follows:

1. We could delete the last character of `start` (costing 1) and add the minimum edit distance between `start[:-1]` and `end`(e.g. `('CAAT', 'AGT') -> ('CAA', 'AGT')`)
2. We could delete the last character of `end` (costing 1), and add the minimum edit distance between `start` and `end[:-1]` (e.g. `('CAAT', 'AGT') -> ('CAAT', 'AG')`)
3. We could substitute the last character of `start` for the last character of `end` (costing 1 if the characters are different and 0 if they're the same) and add the minimum edit distance between `start[:-1]` and `end[:-1]` (e.g. `('CAAT', 'AGT') -> ('CAA', 'AG')`)

At a high-level, we're recursing on substrings of the original strings until we hit a base case. This implementation, as written, is inefficient - it computes the Levenshtein distance of the same substrings many times.

### Hints

* The best way to get from the empty string to any other string is to insert all the characters in the non-empty string.
* If the last characters of 2 sequences are the same, the cost of a substitution is 0!

## Starter Code

```
dna/
├── completed-knightschool.txt
├── README.md
├── dna-small.txt
├── dna.txt
└── dna.py
```

First, fill out the Google form linked in `completed-knightschool.txt` to get credit for finishing up the Knight School puzzle.

Both `dna-small.txt` and `dna.txt` are sample input files, where each line contains an input DNA string and an output DNA string separated by a tab. For reference, your program should produce the output `19` on `dna-small.txt`. Implement your solution in `dna.py`.

## Development Strategy

First, get your program to work on `dna-small.txt`. For the larger `dna.txt`, you may need to implement memoization to speed up your code to reasonable execution times. In a sentence, memoization is caching the result of a deterministic function, and may be useful because several recursive calls could result in the same arguments to `min_distance`, and it would be wasteful to recompute return values you already know.

You can implement intelligent caching/memoization yourself, but recall that there exists a cache builtin to the language. [`lru_cache`](https://docs.python.org/3.4/library/functools.html#functools.lru_cache), in the `functools` module, is a decorator that implements an LRU cache, and can be applied to any function with hashable arguments. By default, the cache holds 128 entries, but you can pass `maxsize=None` as a keyword argument to allow the cache to grow without bound. As an example applied to our `fib` function from lab:

```
@functools.lru_cache(maxsize=None)
def fib(n):
    return fib(n-1) + fib(n-2) if n > 2 else 1
```

> By @csmith95 and @sredmond