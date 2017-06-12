"""
A Python module implementing the alternate base32 encoding as described
by Douglas Crockford using Damm checksums.

------------------
Crockford Alphabet
------------------
Crockford designed the alphabet to be:

   * human and machine readable,
   * compact,
   * lexically sortable keeping the numeric order,
   * error resistant and
   * pronounceable.

A symbol set of 10 digits and 22 letters is chosen (excluding 4 of the 26
letters: I L O U). When decoding, upper and lower case letters are accepted,
and i and l will be treated as 1 and o will be treated as 0. When encoding,
only upper case letters are used. Hyphens may be used in symbol strings
to improve readability.

------------------
Damm CRC algorithm
------------------
The Damm algorithm is used to efficiently calculate a single symbol checksum.
Since the checksum is calculated using the same base as the actual number
no additional symbol-characters are required, whereas the Crockford Algorithm
checksum did require a base37 symbol using the additinal characters '*~$=U'.

Wikipedia extract::

    The Damm algorithm is similar to the Verhoeff algorithm. It too will detect all
    occurrences of the two most frequently appearing types of transcription errors,
    namely altering one single digit, and transposing two adjacent digits (including
    the transposition of the trailing check digit and the preceding digit).
    But the Damm algorithm has the benefit that it makes do without the dedicatedly
    constructed permutations and its position specific powers being inherent in the
    Verhoeff scheme. Furthermore, a table of inverses can be dispensed with provided
    all main diagonal entries of the operation table are zero.
    
    The Damm algorithm does not suffer from exceeding the number of 10 possible values,
    resulting in the need for using a non-digit character (as the X in the 10-digit ISBN check
    digit scheme).
    
    Prepending leading zeros does not affect the check digit.

.. seealso::

  http://www.crockford.com/wrmg/base32.html
  
  https://en.wikipedia.org/wiki/Damm_algorithm
  
  http://www.md-software.de/math/DAMM_Quasigruppen.txt
"""
from .base32 import decode, encode, normalize, pretty
from .damm import damm_checksum, damm_validate, damm_matrix32