"""
referensi:
- https://piazza.com/class_profile/get_resource/ixlc30gojpe5fs/iyv0273azwtz4
- https://sandilands.info/sgordon/teaching/reports/simplified-aes-example-v2.pdf
"""

class MiniAes:
    __ROUND__ = 3
    __SBOX__ = [
        0xE, 0x4, 0xD, 0x1,
        0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC,
        0x5, 0x9, 0x0, 0x7
    ]

    __INV_SBOX__ = [
        0xE, 0x3, 0x4, 0x8,
        0x1, 0xC, 0xA, 0xF,
        0x7, 0xD, 0x9, 0x6,
        0xB, 0x2, 0x0, 0x5
    ]

    def __init__(self):
        self.__plaintext = ""
        self.__keys = ""
        self.__round_keys = []

    def set_plaintext(self, plaintext: str) -> None:
        self.__plaintext = plaintext

    def get_plaintext(self) -> str:
        return self.__plaintext

    def set_keys(self, keys: str) -> None:
        while len(keys) < 4:
            keys = "0" + keys
        self.__keys = keys[:4]

    def get_keys(self) -> str:
        return self.__keys

    def round_key_generator(self) -> None:
        key = int(self.__keys, 16)
        self.__round_keys = [key]
        for i in range(1, 4):
            next_key = ((self.__round_keys[i-1] << 1) & 0xFFFF) ^ (0b10011 << (i-1))
            self.__round_keys.append(next_key)

    def sub_nibbles(self, state: list[int]) -> list[int]:
        return [self.__SBOX__[nibble] for nibble in state]

    def inv_sub_nibbles(self, state: list[int]) -> list[int]:
        return [self.__INV_SBOX__[nibble] for nibble in state]

    def shift_rows(self, state: list[int]) -> list[int]:
        return [state[0], state[3], state[2], state[1]]

    def inv_shift_rows(self, state: list[int]) -> list[int]:
        return [state[0], state[3], state[2], state[1]]

    def gf_mult(self, a: int, b: int) -> int:
        p = 0
        for _ in range(4):
            if b & 1:
                p ^= a
            high_bit_set = a & 0x8
            a <<= 1
            if high_bit_set:
                a ^= 0x13
            a &= 0xF
            b >>= 1
        return p

    def mix_columns(self, state: list[int]) -> list[int]:
        new_state = [0] * 4
        new_state[0] = self.gf_mult(1, state[0]) ^ self.gf_mult(4, state[1])
        new_state[1] = self.gf_mult(4, state[0]) ^ self.gf_mult(1, state[1])
        new_state[2] = self.gf_mult(1, state[2]) ^ self.gf_mult(4, state[3])
        new_state[3] = self.gf_mult(4, state[2]) ^ self.gf_mult(1, state[3])
        return new_state

    def inv_mix_columns(self, state: list[int]) -> list[int]:
        new_state = [0] * 4
        new_state[0] = self.gf_mult(9, state[0]) ^ self.gf_mult(2, state[1])
        new_state[1] = self.gf_mult(2, state[0]) ^ self.gf_mult(9, state[1])
        new_state[2] = self.gf_mult(9, state[2]) ^ self.gf_mult(2, state[3])
        new_state[3] = self.gf_mult(2, state[2]) ^ self.gf_mult(9, state[3])
        return new_state

    def add_round_keys(self, state: list[int], round_key: int) -> list[int]:
        rk = [(round_key >> 12) & 0xF, (round_key >> 8) & 0xF, (round_key >> 4) & 0xF, round_key & 0xF]
        return [s ^ k for s, k in zip(state, rk)]

    def encrypt(self) -> str:
        print("Encrypt :\n")
        state = [(int(self.__plaintext, 16) >> 12) & 0xF, (int(self.__plaintext, 16) >> 8) & 0xF,
                 (int(self.__plaintext, 16) >> 4) & 0xF, int(self.__plaintext, 16) & 0xF]

<<<<<<< HEAD
    def sub_nibbles(self, state: list[list[int]]):
        subs_list: list[list[int]] = []

        for matrix in state:
            nibble_subs: list[int] = []

            for nibble in matrix:
                nibble_subs.append(self.__SBOX__[nibble])

            subs_list.append(nibble_subs)

        return subs_list

    def shift_rows(self, state: list[list[int]]):
        for matrix in state:
            matrix[1] ^= matrix[3]
            matrix[3] ^= matrix[1]
            matrix[1] ^= matrix[3]

        return state

    def mix_columns(self, state: list[list[int]]) -> list[list[int]]:
        __CONSTANT_MATRIX = [
            0x3, 0x4, 0x4, 0x3,
        ]

        result_list: list[list[int]] = []

        for matrix in state:
            this_matrix_result = []

            # index 0
            index_zero = (
                self.__MULTIPLICATION_TABLE__[matrix[0]][__CONSTANT_MATRIX[0]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[1]][__CONSTANT_MATRIX[2]]
            )

            this_matrix_result.append(index_zero)

            # index 1
            index_one = (
                self.__MULTIPLICATION_TABLE__[matrix[0]][__CONSTANT_MATRIX[1]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[1]][__CONSTANT_MATRIX[3]]
            )
            this_matrix_result.append(index_one)

            # index 2
            index_two = (
                self.__MULTIPLICATION_TABLE__[matrix[2]][__CONSTANT_MATRIX[0]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[3]][__CONSTANT_MATRIX[2]]
            )
            this_matrix_result.append(index_two)

            # index 3
            index_three = (
                self.__MULTIPLICATION_TABLE__[matrix[2]][__CONSTANT_MATRIX[1]]) ^ (
                self.__MULTIPLICATION_TABLE__[matrix[3]][__CONSTANT_MATRIX[3]]
            )
            this_matrix_result.append(index_three)

            result_list.append(this_matrix_result)

        return result_list

    def add_round_keys(
        self, state: list[list[int]], round: int
    ) -> list[list[int]]:
        result: list[list[int]] = []

        round_keys = self.get_round_keys()

        for matrix in state:
            this_matrix_result: list[int] = []

            for s, k in zip(matrix, round_keys[round]):
                this_matrix_result.append(s ^ k)

            result.append(this_matrix_result)

        return result

    def state_to_hex(self, state: list[list[int]]) -> str:
        # Converts the first block of encryption state into a hex string (for output)
        result = ""
        matrix = state[0]  # take ONLY the first matrix, hapus jika ingin outputnya lebih dari 4 digit
        for i in range(0, len(matrix), 2):
            combined = (matrix[i] << 4) | matrix[i + 1]
            result += format(combined, "02X")
        return result

    def encrypt(self) -> list[list[int]]:
=======
>>>>>>> 83b4839 (Update Mini AES: perbaikan main.py dan mini_aes.py)
        self.round_key_generator()

        print(f"Round 0 - Input State: {self.format_state(state)}")
        state = self.add_round_keys(state, self.__round_keys[0])
        print(f"Round 0 - After AddRoundKey: {self.format_state(state)}\n")

<<<<<<< HEAD
        for current_round in range(1, self.__ROUND__ + 1):
            print(f"ROUND {current_round}")

            state = self.sub_nibbles(state)
            print(f"After SubNibbles: {self.state_to_hex(state)}")

            state = self.shift_rows(state)
            print(f"After ShiftRows : {self.state_to_hex(state)}")

            state = self.mix_columns(state)
            print(f"After MixColumns: {self.state_to_hex(state)}")

            state = self.add_round_keys(state, current_round)
            print(f"After AddRoundKey: {self.state_to_hex(state)}")

        print("FINAL ROUND")
        state = self.sub_nibbles(state)
        print(f"After SubNibbles: {self.state_to_hex(state)}")

        state = self.shift_rows(state)
        print(f"After ShiftRows : {self.state_to_hex(state)}")

        state = self.add_round_keys(state, 4)
        print(f"After AddRoundKey: {self.state_to_hex(state)}")

        print("Encrypt COMPLETE")
        print(f"Ciphertext: {self.state_to_hex(state)}")

        return state
=======
        for r in range(1, 4):
            print(f"ROUND {r}")
            state = self.sub_nibbles(state)
            print(f"After SubNibbles: {self.format_state(state)}")

            state = self.shift_rows(state)
            print(f"After ShiftRows: {self.format_state(state)}")

            if r != 3:
                state = self.mix_columns(state)
                print(f"After MixColumns: {self.format_state(state)}")
>>>>>>> 83b4839 (Update Mini AES: perbaikan main.py dan mini_aes.py)

            state = self.add_round_keys(state, self.__round_keys[r])
            print(f"After AddRoundKey: {self.format_state(state)}\n")

        ciphertext = (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]
        print("Enrypt COMPLETE\n")
        return f"{ciphertext:04X}"

    def decrypt(self, ciphertext: str) -> str:
        print("\nDecryption :\n")
        state = [(int(ciphertext, 16) >> 12) & 0xF, (int(ciphertext, 16) >> 8) & 0xF,
                 (int(ciphertext, 16) >> 4) & 0xF, int(ciphertext, 16) & 0xF]

        self.round_key_generator()

        print(f"Round 3 - Input State: {self.format_state(state)}")
        state = self.add_round_keys(state, self.__round_keys[3])
        print(f"Round 3 - After AddRoundKey: {self.format_state(state)}\n")

        for r in range(2, -1, -1):
            print(f"=== ROUND {r} ===")
            state = self.inv_shift_rows(state)
            print(f"After InvShiftRows: {self.format_state(state)}")

            state = self.inv_sub_nibbles(state)
            print(f"After InvSubNibbles: {self.format_state(state)}")

            state = self.add_round_keys(state, self.__round_keys[r])
            print(f"After AddRoundKey: {self.format_state(state)}")

            if r != 0:
                state = self.inv_mix_columns(state)
                print(f"After InvMixColumns: {self.format_state(state)}\n")

        plaintext = (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]
        print("Decryption COMPLETE\n")
        return f"{plaintext:04X}"

    def format_state(self, state: list[int]) -> str:
        return ''.join(f"{x:X}" for x in state)

if __name__ == "__main__":
    plaintext = input("Masukkan plaintext (hex 4 digit, contoh 1234): ")
    key = input("Masukkan key (hex 4 digit, contoh 5678): ")

    aes = MiniAes()
    aes.set_plaintext(plaintext)
    aes.set_keys(key)

    ciphertext = aes.encrypt()
    print(f"Ciphertext: {ciphertext}")

<<<<<<< HEAD
            # index 3
            index_three = (__CONSTANT_MATRIX[1] * matrix[2]) ^ (
                __CONSTANT_MATRIX[3] * matrix[3]
            )
            this_matrix_result.append(index_three)

            result_list.append(this_matrix_result)

        return result_list

    def decrypt(self) -> list[list[int]]:
        return [[]]

aes = MiniAes()
aes.set_plaintext("C3C3")
aes.set_keys("A1A1")
state_result = aes.encrypt()
cipher_hex = aes.state_to_hex(state_result)
print("Ciphertext:", cipher_hex)
=======
    decrypted = aes.decrypt(ciphertext)
    print(f"Decrypted : {decrypted}")
>>>>>>> 83b4839 (Update Mini AES: perbaikan main.py dan mini_aes.py)
