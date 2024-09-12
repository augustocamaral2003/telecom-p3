def decode(sig):
    current_state = 0
    frame_data = []
    previous_symbol = 0
    bit_count = 0
    byte_accumulator = 0

    for current_symbol in extract_symbols(sig):
        if current_state == 0:
            if previous_symbol == 1 and current_symbol == 1:
                current_state = 1
            previous_symbol = current_symbol
        elif current_state == 1:
            byte_accumulator |= (current_symbol << bit_count)

            if bit_count == 7:
                frame_data.append(byte_accumulator)
                byte_accumulator = 0

            bit_count = (bit_count + 1) % 8

    return bytes(frame_data)

def extract_symbols(sample_sequence):
    count_position = 1
    level = sample_sequence[0]

    for sample in sample_sequence[1:]:
        if sample == level:
            count_position += 1
        else:
            if count_position >= 20:
                return
            if count_position >= 6:
                count_position = 0
                yield sample

            level = sample