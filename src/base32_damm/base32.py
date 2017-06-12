from .damm import damm_checksum, damm_matrix32
import itertools

_b32alphabet = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
'''
base32 alphabet according to crockford
import itertools
'''

_b32translation = str.maketrans('IiLlOo', '111100')
'''
letter translation according to crockford
'''

_b32decode = dict(zip(_b32alphabet, range(len(_b32alphabet))))
'''
reverse lookup-table
'''

_b32bits = 5
_b32mask = 0x1f

def normalize(symbols):
    '''
    Normalization provides error correction and prepares the
    string for decoding. These transformations are applied:
    
       1. Hyphens are removed
       2. 'I', 'i', 'L' or 'l' are converted to '1'
       3. 'O' or 'o' are converted to '0'
       4. All characters are converted to uppercase
       
    Returns:
        str: normalized string
    '''
    return symbols.replace('-', '').translate(_b32translation).upper()
    
def encode(number, checksum=True, groupsize=99, width=0):
    """
    Encode an integer into a symbol string.
    
    Args:
        crc: wether a checksum (1 symbol) is to be generated and appended
             to the result
             
        groupsize: divide the resulting symbols into groups of groupsize
                   plus a separate group for the checksum (if any)
    
    Raises:
        ValueError: 
        
    Returns:
        str: base32 formatted number
    """    
    
    if number is None:
        return None
    if isinstance(number, float):
        raise ValueError()

    number = int(number)
    if number < 0:
        raise ValueError('negative numbers are not supported')
    
    if number == 0:
        symbols = [0]
    
    else:
        symbols = []
        while number > 0:
            digit = number & _b32mask
            number >>= _b32bits
            symbols.append(digit)
        
    width -= len(symbols)
    if width > 0:
        symbols.extend(itertools.repeat(0, width))
    
    symbols.reverse()

    if checksum:
        checksymbol = damm_checksum(damm_matrix32, symbols)
        symbols.append(checksymbol)

    symbols = [_b32alphabet[x] for x in symbols]

    if groupsize:
        return pretty(symbols, checksum, groupsize)

    else:
        return ''.join(symbols)    

def decode(value, checksum=True):
    """
    Decode an encoded symbol string.
    
    Args:
        crc: if set to True, the string is assumed to have a trailing check symbol
        which will be validated.
        
    Raises:
        ValueError: if value contains invalid symbols or the crc check fails 
        
    Returns:
        int: the decoded number if returned
    """
        
    symbols = normalize(value)
    try:
        symbols = [_b32decode[x] for x in symbols]
    except KeyError as e:
        raise ValueError("{}".format(e))
    
    if checksum:
        check = damm_checksum(damm_matrix32, symbols)
        if check != 0:
            raise ValueError("Ungültige Prüfsumme: {}".format(value))
        symbols = symbols[:-1]
    
    number = 0
    for x in symbols:
        number <<= _b32bits
        number += x
        
    return number

def pretty(symbols, checksum, groupsize, sep='-'):
    groups = []
    
    if checksum:
        checksymbol = symbols[-1]
        symbols = symbols[:-1]
    else:
        checksymbol = None
    
    i = len(symbols) % groupsize
    if i > 0:
        groups.append(''.join(symbols[0:i]))
    while i < len(symbols):
        j = i + groupsize
        groups.append(''.join(symbols[i:j]))
        i = j
    
    if checksymbol is not None:
        groups.append(checksymbol)    
    
    return sep.join(groups)
    
