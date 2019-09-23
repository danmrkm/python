#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii

_b32hexalphabet = b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
_b32hextab2 = None
_b32hexrev = None

bytes_types = (bytes, bytearray)  # Types acceptable as binary data


def _bytes_from_decode_data(s):
    if isinstance(s, str):
        try:
            return s.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError(
                'string argument should contain only ASCII characters')
    if isinstance(s, bytes_types):
        return s
    try:
        return memoryview(s).tobytes()
    except TypeError:
        raise TypeError("argument should be a bytes-like object or ASCII "
                        "string, not %r" % s.__class__.__name__)


def base32hex_encode(s):
    """Encode the bytes-like object s using Base32 with Hex Alphabet and return a bytes object.
    """
    global _b32hextab2
    # Delay the initialization of the table to not waste memory
    # if the function is never called
    if _b32hextab2 is None:
        b32hextab = [bytes((i,)) for i in _b32hexalphabet]
        _b32hextab2 = [a + b for a in b32hextab for b in b32hextab]
        b32hextab = None

    if not isinstance(s, bytes_types):
        s = memoryview(s).tobytes()
    leftover = len(s) % 5
    # Pad the last quantum with zero bits if necessary
    if leftover:
        s = s + b'\0' * (5 - leftover)  # Don't use += !
    encoded = bytearray()
    from_bytes = int.from_bytes
    b32hextab2 = _b32hextab2
    for i in range(0, len(s), 5):
        c = from_bytes(s[i: i + 5], 'big')
        encoded += (b32hextab2[c >> 30] +           # bits 1 - 10
                    b32hextab2[(c >> 20) & 0x3ff] +  # bits 11 - 20
                    b32hextab2[(c >> 10) & 0x3ff] +  # bits 21 - 30
                    b32hextab2[c & 0x3ff]           # bits 31 - 40
                    )
    # Adjust for any leftover partial quanta
    if leftover == 1:
        encoded[-6:] = b'======'
    elif leftover == 2:
        encoded[-4:] = b'===='
    elif leftover == 3:
        encoded[-3:] = b'==='
    elif leftover == 4:
        encoded[-1:] = b'='
    return bytes(encoded)


def base32hex_decode(s, casefold=False, map01=None):
    """Decode the Base32 encoded bytes-like object or ASCII string s.
    Optional casefold is a flag specifying whether a lowercase alphabet is
    acceptable as input.  For security purposes, the default is False.
    RFC 3548 allows for optional mapping of the digit 0 (zero) to the
    letter O (oh), and for optional mapping of the digit 1 (one) to
    either the letter I (eye) or letter L (el).  The optional argument
    map01 when not None, specifies which letter the digit 1 should be
    mapped to (when map01 is not None, the digit 0 is always mapped to
    the letter O).  For security purposes the default is None, so that
    0 and 1 are not allowed in the input.
    The result is returned as a bytes object.  A binascii.Error is raised if
    the input is incorrectly padded or if there are non-alphabet
    characters present in the input.
    """
    global _b32hexrev
    # Delay the initialization of the table to not waste memory
    # if the function is never called
    if _b32hexrev is None:
        _b32hexrev = {v: k for k, v in enumerate(_b32hexalphabet)}
    s = _bytes_from_decode_data(s)
    if len(s) % 8:
        raise binascii.Error('Incorrect padding')
    # Handle section 2.4 zero and one mapping.  The flag map01 will be either
    # False, or the character to map the digit 1 (one) to.  It should be
    # either L (el) or I (eye).
    if map01 is not None:
        map01 = _bytes_from_decode_data(map01)
        assert len(map01) == 1, repr(map01)
        s = s.translate(bytes.maketrans(b'01', b'O' + map01))
    if casefold:
        s = s.upper()
    # Strip off pad characters from the right.  We need to count the pad
    # characters because this will tell us how many null bytes to remove from
    # the end of the decoded string.
    l = len(s)
    s = s.rstrip(b'=')
    padchars = l - len(s)
    # Now decode the full quanta
    decoded = bytearray()
    b32hexrev = _b32hexrev
    for i in range(0, len(s), 8):
        quanta = s[i: i + 8]
        acc = 0
        try:
            for c in quanta:
                acc = (acc << 5) + b32hexrev[c]
        except KeyError:
            raise binascii.Error('Non-base32 digit found')
        decoded += acc.to_bytes(5, 'big')
    # Process the last, partial quanta
    if l % 8 or padchars not in {0, 1, 3, 4, 6}:
        raise binascii.Error('Incorrect padding')
    if padchars and decoded:
        acc <<= 5 * padchars
        last = acc.to_bytes(5, 'big')
        leftover = (43 - 5 * padchars) // 8  # 1: 4, 3: 3, 4: 2, 6: 1
        decoded[-5:] = last[:leftover]
    return bytes(decoded)


if __name__ == '__main__':
    # 直接起動のみ実行
    sample = '7!2S&^V$Mxe4{o&N'
    result = base32hex_encode(sample.encode())
    print(result)
    result = base32hex_decode(result)
    print(result)
