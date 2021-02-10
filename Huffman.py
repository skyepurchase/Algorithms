import math


def generateHuffman(text):
    """
    Takes a string an generates a Huffman code for that string
    :param text: a string of characters to act as the basis of the Huffman Code
    :return: a tuple containing a dictionary representing the Huffman Code and the average bits per character
    """
    frequencies = {}
    code = {}
    total_bits = 0
    total_chars = len(text)

    for char in text:  # Create a frequency map
        if char not in frequencies.keys():
            count = text.count(char)
            frequencies[char] = count

    sorted_chars = sorted(frequencies.keys(), key=frequencies.get, reverse=True)  # The symbols in smallest-largest
    # order

    while len(sorted_chars) > 1:
        # ASSERT smallest two items are at the end
        smallest = sorted_chars.pop()
        second_smallest = sorted_chars.pop()
        frequencies[smallest + second_smallest] = frequencies[smallest] + frequencies[
            second_smallest]  # Add new frequency
        total_bits += frequencies[smallest] + frequencies[second_smallest]  # Bits weighted by occurrence
        frequencies.pop(smallest)
        frequencies.pop(second_smallest)  # Remove old frequencies
        sorted_chars = sorted(frequencies.keys(), key=frequencies.get, reverse=True)  # Bring smallest to the front

        # ASSERT we have created a branch so can prepend new code to each char
        for char in smallest:
            if char in code.keys():
                curr = code[char]
                new = '1' + curr
                code[char] = new
            else:
                code[char] = '1'

        for char in second_smallest:
            if char in code.keys():
                curr = code[char]
                new = '0' + curr
                code[char] = new
            else:
                code[char] = '0'

    return code, total_bits / total_chars


def generateBin(text):
    """
    Takes a string an generates a Binary code for that string
    :param text: a string of characters to act as the basis of the Binary Code
    :return: a tuple containing a dictionary representing the Binary Code and the bits per character
    """
    unique_chars = set()
    code = {}

    for char in text:  # Create a frequency map
        unique_chars.add(char)

    bits_per_char = math.ceil(math.log(len(unique_chars), 2))

    i = 0
    for char in unique_chars:
        binary = str(bin(i)).replace('0b', '').zfill(bits_per_char)
        code[char] = binary
        i += 1

    return code, bits_per_char


def generateAscii(text):
    """
    Takes a string an generates the ASCII code for that string
    :param text: a string of characters to act as the basis of the ASCII Code
    :return: a tuple containing a dictionary representing the Binary Code and the bits per character
    """
    unique_chars = set()
    code = {}

    for char in text:  # Create a frequency map
        unique_chars.add(char)

    i = 0
    for char in unique_chars:
        binary = str(bin(ord(char))).replace('0b', '').zfill(7)
        code[char] = binary
        i += 1

    return code, 7


def encode(text, code):
    """
    Takes a string and then encodes into bits based on a provided code
    :param text: a string to encode
    :param code: a code to use in the encoding
    :return: a string of bits
    """
    result = ""

    for char in text:
        result += code[char]

    return result


def decode(bits, code):
    """
    Takes a bit string and then decodes into a string based on a provided code
    :param bits: a bit string to decode
    :param code: a code to use in the decoding
    :return: a string
    """
    result = ""
    running_bits = ""

    for bit in bits:
        running_bits += bit  # ASSERT: The bits so far do not define a character
        for char, bit_code in code.items():
            if running_bits == bit_code:
                # ASSERT: We now have a character (Huffman guarantees no prefixes and bin/ascii are equal length)
                result += char
                running_bits = ""
            elif len(running_bits) > max([len(x) for x in code.values()]):
                # ASSERT: This bit string does not define a character so we shall mark it as unknown
                result += '?'
                running_bits = ""

    return result


def compressionRate(text, generator, type):
    """
    Takes a text and calculates compression rate assuming binary encoding (rather than ascii)
    :param text: String to be compressed
    :param generator: String used to create huffman code
    :param type: The type of base encoding
    :return: The compression rate
    """
    if (type == 'A'):
        base_code, _ = generateAscii(generator)
    else:
        base_code, _ = generateBin(generator)

    huff_code, _ = generateHuffman(generator)

    base_encoded = encode(text, base_code)
    huff_encoded = encode(text, huff_code)

    return len(base_encoded) / len(huff_encoded)


text1 = "I know what you're thinking ... 'Enough beating around the bush. Just tell us whether you liked it.' " \
            "Consider this, which I will say in terms this movie would understand, if you were on an airplane, " \
            "'The Other Woman' might not be preferable to simply staring into your empty airsick bag, but it has " \
            "enough nicely executed physical comedy that in the event you become ill, it is definitely preferable to " \
            "staring into your occupied airsick bag."
text2 = "This is a movie about how words aren't cool, but you can still expect a girl to fall at your feet in " \
        "response to mild wordplay. Please keep up. Or throw whatever device you're reading this on into the ocean. " \
        "Send me a postcard ... tell me what it's like to be free."
generator = "While I had the misfortune to see 'Bright' in a theater, most people will simply press 'play' out of " \
        "curiosity on their Roku remote. I am willing to concede that this might elevate the experience a little ... " \
        "the ability to take a quick trip to the kitchen or restroom after shouting 'no, don't pause it' to your " \
        "partner on the couch will be liberating.j"

generator = generator.lower()
text1 = text1.lower()
text2 = text2.lower()

huff_code, huff_bit_rate = generateHuffman(generator)
bin_code, bin_bit_rate = generateBin(generator)
ascii_code, ascii_bit_rate = generateAscii(generator)

print("Using " + generator + ":")
print("Huffman avg bit rate:\t", huff_bit_rate)
print("Binary bit rate:\t\t", bin_bit_rate)
print("Ascii bit rate:\t\t\t", ascii_bit_rate)
print("\n")

for text in [generator, text1, text2]:
    huff_encoded = encode(text, huff_code)
    bin_encoded = encode(text, bin_code)
    ascii_encoded = encode(text, ascii_code)
    decoded = decode(ascii_encoded, huff_code)
    print(text + ":")
    print("Huffman Encode:\t\t\t", huff_encoded)
    print("Binary Encode:\t\t\t", bin_encoded)
    print("Ascii Encode:\t\t\t", ascii_encoded)
    print("Huffman Decode:\t\t\t", decoded)
    print("Bin Compression Rate:\t", compressionRate(text, generator, 'B'))
    print("Ascii Compression Rate:\t", compressionRate(text, generator, 'A'))
    print()
