# Utilidades de conversión de formatos
def hex_to_bin(hex_string):
    """Convierte un string hexadecimal a un string binario."""
    # Convierte hexadecimal a entero y de entero a binario
    return bin(int(hex_string, 16))[2:]

def bin_to_hex(bin_string):
    """Convierte un string binario a un string hexadecimal."""
    # Convierte binario a entero y de entero a hexadecimal
    return hex(int(bin_string, 2))[2:].upper()


def bin_plus_one(bin_string):
    """Incrementa un valor binario en uno, considerando el acarreo."""
    n = len(bin_string)
    result = list(bin_string)
    for i in range(n-1, -1, -1):
        if result[i] == '0':
            result[i] = '1'
            return ''.join(result)
        result[i] = '0'
    return '1' + ''.join(result)