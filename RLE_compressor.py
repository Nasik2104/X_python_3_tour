import os


class RLE_compressor:
    def encode(self, data):
        if not data:
            print("Empty_file")
            return ""

        compressed_data = ''
        count = 1
        pre_char = ''

        for index, char in enumerate(data):
            if index == 0:
                pre_char = char
            if char == pre_char:
                count += 1
            else:
                compressed_data += f"{count}{pre_char}"
                pre_char = char
                count = 1

        compressed_data += f"{count}{pre_char}"

        return compressed_data

    def decode(self, data):
        decompressed_data = ''

        for char in data:
            if char.isdigit():
                count = int(char)
            else:
                if count:
                    decompressed_data += char * count

        return decompressed_data

    def compress_file(self, input_file, output_file):
        with open(input_file, 'r', encoding='UTF-8') as file:
            data = file.read()

        compressed_data = self.encode(data)

        with open(output_file, 'w', encoding="UTF-8") as file:
            file.write(compressed_data)

        return compressed_data

    def compare_file_sizes(self, original_file, compressed_file):
        original_size = os.path.getsize(original_file)
        compressed_size = os.path.getsize(compressed_file)

        print(f"Original file size: {original_size} bytes")
        print(f"Compressed file size: {compressed_size} bytes")
        print(f"Size reduction: {original_size - compressed_size} bytes")


if __name__ == "__main__":
    input_file_path = "123.txt"
    output_file_path = 'compressed.txt'

    compressor = RLE_compressor()

    compressor.compress_file(input_file=input_file_path, output_file=output_file_path)
    compressor.compare_file_sizes(original_file=input_file_path, compressed_file=output_file_path)

    with open(output_file_path, 'r', encoding="UTF-8") as f:
        compressed_data = f.read()

    decompressed_data = compressor.decode(compressed_data)
    print("Decompressed:", decompressed_data)
