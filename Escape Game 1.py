# A secret message is hidden inside this scrambled list.
# Extract characters using slicing to reveal the first key.
letters = ['x', 'c','w', 'o','k', 'n', 't', 'g', 'l', 'r', 'm', 'a', 'z', 't', 'q','s']

# TODO: Fill in the slicing so the output becomes the secret word.
key = "".join(letters[1::2])   # fill the blank
print(key)
