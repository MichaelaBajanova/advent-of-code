import math

HEXA_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


class LiteralValuePacket:
    def __init__(self, version, value, length):
        self.version = version
        self.type_id = 4
        self.value = value
        self.length = length


class OperatorPacket:
    def __init__(self, version, type_id, length_type_id, length_field, subpackets, length):
        self.version = version
        self.type_id = type_id
        self.length_type_id = length_type_id
        self.length_field = length_field
        self.subpackets = subpackets
        self.length = length


def parse_input():
    with (open("./input.txt")) as input_file:
        return input_file.readline().strip()


def hexa_to_bin(hexa):
    bin = ""
    for char in hexa:
        bin += HEXA_TO_BIN[char]
    return bin


def bin_to_dec(binary):
    reversed = binary[::-1]
    decimal = 0
    for i in range(len(reversed)):
        bit = int(reversed[i])
        decimal += bit * math.pow(2, i)
    return int(decimal)


def get_groups(bit_stream):
    groups = []
    value_start = 6
    bits_read = 0
    while bit_stream[value_start] == '1':
        groups.append(bit_stream[value_start+1:value_start+5])
        bits_read += 5
        value_start += 5
    # read last group
    groups.append(bit_stream[value_start+1:value_start+5])

    return groups


def get_version(bit_stream):
    return bit_stream[:3]


def get_type_id(bit_stream):
    return bit_stream[3:6]


def get_length_type_id(bit_stream):
    return bit_stream[6:7]


def get_literal_value(bit_stream):
    groups = get_groups(bit_stream)
    value_bin = ""
    for group in groups:
        value_bin += group

    return {"len": len(value_bin) + len(groups), "value": bin_to_dec(value_bin)}


def print_packet(packet):
    if isinstance(packet, LiteralValuePacket):
        print("Literal value")
        print("Version: ", packet.version)
        print("Type ID: ", packet.type_id)
        print("Value: ", packet.value)
        print("Length: ", packet.length)
    if isinstance(packet, OperatorPacket):
        print("Operator")
        print("Version: ", packet.version)
        print("Type ID: ", packet.type_id)
        print("Length type: ", packet.length_type_id)
        print("Length field: ", packet.length_field)
        print("Length: ", packet.length)
        print("Subpackets:")
        for i in range(len(packet.subpackets)):
            print(i+1, ". ", end="")
            print_packet(packet.subpackets[i])


def get_version_sum(packet):
    if isinstance(packet, LiteralValuePacket):
        return packet.version
    elif isinstance(packet, OperatorPacket):
        sum = packet.version
        for subpacket in packet.subpackets:
            sum += get_version_sum(subpacket)
        return sum


def is_end(bit_stream):
    for bit in bit_stream:
        if bit == '1':
            return False
    return True


def parse_packet(binary):
    version = bin_to_dec(get_version(binary))
    type = bin_to_dec(get_type_id(binary))

    if type == 4:
        literal_value = get_literal_value(binary)
        literal_value_dec = literal_value["value"]
        # version + type id + literal value
        packet_length = 3 + 3 + literal_value["len"]
        packet = LiteralValuePacket(
            version, value=literal_value_dec, length=packet_length)
    else:
        length_type = int(get_length_type_id(binary))
        subpackets_start = 22 if length_type == 0 else 18
        # length type ID ends on index 6, therefore we start on 7
        length_field = bin_to_dec(binary[7:subpackets_start])

        i = subpackets_start
        subpackets = []
        if type == 4:
            while i < len(binary):
                if is_end(binary[i:]):
                    break
                subpacket = parse_packet(binary[i:])
                subpackets.append(subpacket)
                i += subpacket.length
        else:
            if length_type == 0:
                while i < subpackets_start + length_field:
                    if is_end(binary[i:]):
                        break
                    subpacket = parse_packet(binary[i:])
                    subpackets.append(subpacket)
                    i += subpacket.length
            elif length_type == 1:
                while len(subpackets) < length_field:
                    if is_end(binary[i:]):
                        break
                    subpacket = parse_packet(binary[i:])
                    subpackets.append(subpacket)
                    i += subpacket.length

        packet = OperatorPacket(
            version, type, length_type, length_field, subpackets, length=i)

    return packet


def part_1(binary):
    packet = parse_packet(binary)
    return get_version_sum(packet)


def calculate(packet):
    if isinstance(packet, LiteralValuePacket):
        return packet.value
    if isinstance(packet, OperatorPacket):
        values = []
        for subpacket in packet.subpackets:
            values.append(calculate(subpacket))

        if packet.type_id == 0:
            return sum(values)
        elif packet.type_id == 1:
            return math.prod(values)
        elif packet.type_id == 2:
            return min(values)
        elif packet.type_id == 3:
            return max(values)
        elif packet.type_id == 5:
            return 1 if values[0] > values[1] else 0
        elif packet.type_id == 6:
            return 1 if values[0] < values[1] else 0
        elif packet.type_id == 7:
            return 1 if values[0] == values[1] else 0


def part_2(binary):
    packet = parse_packet(binary)
    return calculate(packet)


if __name__ == "__main__":
    hexa = parse_input()

    result_1 = part_1(hexa_to_bin(hexa))
    print("Part 1: ", result_1)
    result_2 = part_2(hexa_to_bin(hexa))
    print("Part 2: ", result_2)
