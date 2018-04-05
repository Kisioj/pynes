import binascii
import struct

FLOAT = '<d'  # 8 bytes
STRING = '<{}s'  # {} bytes

SHORT_INT = '<B'  # 1 byte
INT = '<l'  # 4 bytes
LONG_INT = '<q'  # 8 bytes


def unpack(file, bytes=None, data_type=None):
    result = file.read(bytes)
    if bytes is None:
        if data_type == SHORT_INT:
            bytes = 1
        elif data_type == INT:
            bytes = 4
        elif data_type in (FLOAT, LONG_INT):
            bytes = 8
        elif data_type == STRING:
            raise AttributeError('bytes argument is required for string data_type')

    elif data_type is None:
        if bytes == 1:
            data_type = SHORT_INT
        elif bytes == 4:
            data_type = INT
        elif bytes == 8:
            data_type = LONG_INT
        else:
            data_type = STRING

    if data_type == STRING:
        data_type = STRING.format(bytes)

    result = struct.unpack(data_type, result)[0]
    return result

def show_file(fname):
    with open(fname, "rb") as file:
        """Should contain the string ‘NES’ to identify the file as an iNES file"""
        nes = unpack(file, bytes=3, data_type=STRING)

        """Should contain the value $1A, also used to identify file format. """
        format_identifier = unpack(file, bytes=1, data_type=SHORT_INT)

        """Number of 16 KB PRG-ROM banks. The PRG-ROM
        (Program ROM) is the area of ROM used to store the
        program code."""
        program_rom_banks = unpack(file, bytes=1, data_type=SHORT_INT)

        """Number of 8 KB CHR-ROM / VROM banks. The names
        CHR-ROM (Character ROM) and VROM are used
        synonymously to refer to the area of ROM used to store
        graphics information, the pattern tables. """
        character_rom_banks = unpack(file, bytes=1, data_type=SHORT_INT)


        """ROM Control Byte 1:
            •   Bit 0 - Indicates the type of mirroring used by the game
                where 0 indicates horizontal mirroring, 1 indicates
                vertical mirroring.

            •   Bit 1 - Indicates the presence of battery-backed RAM at
                memory locations $6000-$7FFF.

            •   Bit 2 - Indicates the presence of a 512-byte trainer at
                memory locations $7000-$71FF.

            •   Bit 3 - If this bit is set it overrides bit 0 to indicate fourscreen
                mirroring should be used.

            •   Bits 4-7 - Four lower bits of the mapper number"""
        rom_control_byte1 = unpack(file, bytes=1, data_type=SHORT_INT)

        """ROM Control Byte 2:
        •   Bits 0-3 - Reserved for future usage and should all be 0.
        •   Bits 4-7 - Four upper bits of the mapper number. """
        rom_control_byte2 = unpack(file, bytes=1, data_type=SHORT_INT)

        """Number of 8 KB RAM banks. For compatibility with previous
        versions of the iNES format, assume 1 page of RAM when
        this is 0. """
        ram_banks = unpack(file, bytes=1, data_type=SHORT_INT)

        """Reserved for future usage and should all be 0. """
        zeros = unpack(file, bytes=7, data_type=STRING)

        print('nes', nes)
        print('format_identifier', format(format_identifier, '02x'))
        print('program_roms', program_rom_banks)
        print('character_roms', character_rom_banks)
        print('rom_control_byte1', rom_control_byte1)
        print('rom_control_byte2', rom_control_byte2)
        print('ram_banks', ram_banks)
        print('zeros', zeros)


if __name__ == '__main__':
    show_file('gekishinfreeza.nes')