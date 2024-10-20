import heapq
import os
from collections import Counter
from typing import Dict


class HuffmanNode:
    def __init__(self, char: str = None, freq: int = 0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCompressor:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    def _build_frequency_table(self, text: str) -> Dict[str, int]:
        return Counter(text)

    def _build_huffman_tree(self, frequency: Dict[str, int]) -> HuffmanNode:
        priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)

            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right

            heapq.heappush(priority_queue, merged)

        return priority_queue[0]

    def _generate_codes(self, node: HuffmanNode, current_code: str):
        if not node:
            return

        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_mapping[current_code] = node.char
            return

        self._generate_codes(node.left, current_code + "0")
        self._generate_codes(node.right, current_code + "1")

    def compress(self, text: str) -> str:
        frequency_table = self._build_frequency_table(text)
        huffman_tree = self._build_huffman_tree(frequency_table)
        self._generate_codes(huffman_tree, "")

        return ''.join(self.codes[char] for char in text)

    def decompress(self, compressed_text: str) -> str:
        current_code = ""
        decoded_text = []

        for bit in compressed_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text.append(self.reverse_mapping[current_code])
                current_code = ""

        return ''.join(decoded_text)

    def save_compressed_file(self, input_file: str, output_file: str):
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        compressed_text = self.compress(text)

        # Перетворимо бінарний рядок на байти і збережемо їх у .bin файл
        binary_data = int(compressed_text, 2)
        with open(output_file, 'wb') as file:
            file.write(binary_data.to_bytes((binary_data.bit_length() + 7) // 8, byteorder='big'))

        print(f"Файл стиснуто і збережено в {output_file}. Розмір стиснутого файлу: {os.path.getsize(output_file)} байт.")

    def save_decompressed_file(self, compressed_file: str, output_file: str):
        with open(compressed_file, 'rb') as file:
            binary_data = int.from_bytes(file.read(), byteorder='big')

        compressed_text = bin(binary_data)[2:]

        decompressed_text = self.decompress(compressed_text)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(decompressed_text)

        print(f"Файл розпаковано і збережено в {output_file}. Розмір розпакованого файлу: {os.path.getsize(output_file)} байт.")


if __name__ == "__main__":
    compressor = HuffmanCompressor()

    input_file = '123.txt'
    compressed_file = 'compressed.bin'
    decompressed_file = 'decompressed.txt'

    compressor.save_compressed_file(input_file, compressed_file)
    compressor.save_decompressed_file(compressed_file, decompressed_file)
