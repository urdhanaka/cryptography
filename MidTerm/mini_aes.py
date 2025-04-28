"""
references:
- https://piazza.com/class_profile/get_resource/ixlc30gojpe5fs/iyv0273azwtz4
- https://sandilands.info/sgordon/teaching/reports/simplified-aes-example-v2.pdf
"""
class MiniAes:
    # constants
    __ROUND__ = 3
    __SBOX__ = [
        0xE, 0x4, 0xD, 0x1,  # 0x0  0x1  0x2  0x3
        0x2, 0xF, 0xB, 0x8,  # 0x4  0x5  0x6  0x7
        0x3, 0xA, 0x6, 0xC,  # 0x8  0x9  0xA  0xB
        0x5, 0x9, 0x0, 0x7,  # 0xC  0xD  0xE  0xF
    ]
    __INV_SBOX__ = [
        0xE, 0x3, 0x4, 0x8,  # 0x0  0x1  0x2  0x3
        0x1, 0xC, 0xA, 0xF,  # 0x4  0x5  0x6  0x7
        0x7, 0xD, 0x9, 0x6,  # 0x8  0x9  0xA  0xB
        0xB, 0x2, 0x0, 0x5,  # 0xC  0xD  0xE  0xF
    ]
    __MULTIPLICATION_TABLE__ = [
        # 0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0], # 0
        [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF], # 1
        [0x0, 0x2, 0x4, 0x6, 0x8, 0xA, 0xC, 0xE, 0x3, 0x1, 0x7, 0x5, 0xB, 0x9, 0xF, 0xD], # 2
        [0x0, 0x3, 0x6, 0x5, 0xC, 0xF, 0xA, 0x9, 0xB, 0x8, 0xD, 0xE, 0x7, 0x4, 0x1, 0x2], # 3
        [0x0, 0x4, 0x8, 0xC, 0x3, 0x7, 0xB, 0xF, 0x6, 0x2, 0xE, 0xA, 0x5, 0x1, 0xD, 0x9], # 4
        [0x0, 0x5, 0xA, 0xF, 0x7, 0x2, 0xD, 0x8, 0xE, 0xB, 0x4, 0x1, 0x9, 0xC, 0x3, 0x6], # 5
        [0x0, 0x6, 0xC, 0xA, 0xB, 0xD, 0x7, 0x1, 0x5, 0x3, 0x9, 0xF, 0xE, 0x8, 0x2, 0x4], # 6
        [0x0, 0x7, 0xE, 0x9, 0xF, 0x8, 0x1, 0x6, 0xD, 0xA, 0x3, 0x4, 0x2, 0x5, 0xC, 0xB], # 7
        [0x0, 0x8, 0x3, 0xB, 0x6, 0xE, 0x5, 0xD, 0xC, 0x4, 0xF, 0x7, 0xA, 0x2, 0x9, 0x1], # 8
        [0x0, 0x9, 0x1, 0x8, 0x2, 0xB, 0x3, 0xA, 0x4, 0xD, 0x5, 0xC, 0x6, 0xF, 0x7, 0xE], # 9
        [0x0, 0xA, 0x7, 0xD, 0xE, 0x4, 0x9, 0x3, 0xF, 0x5, 0x8, 0x2, 0x1, 0xB, 0x6, 0xC], # A
        [0x0, 0xB, 0x5, 0xE, 0xA, 0x1, 0xF, 0x4, 0x7, 0xC, 0x2, 0x9, 0xD, 0x6, 0x8, 0x3], # B
        [0x0, 0xC, 0xB, 0x7, 0x5, 0x9, 0xE, 0x2, 0xA, 0x6, 0x1, 0xD, 0xF, 0x3, 0x4, 0x8], # C
        [0x0, 0xD, 0x9, 0x4, 0x1, 0xC, 0x8, 0x5, 0x2, 0xF, 0xB, 0x6, 0x3, 0xE, 0xA, 0x7], # D
        [0x0, 0xE, 0xF, 0x1, 0xD, 0x3, 0x2, 0xC, 0x9, 0x7, 0x6, 0x8, 0x4, 0xA, 0xB, 0x5], # E
        [0x0, 0xF, 0xD, 0x2, 0x9, 0x6, 0x4, 0x8, 0x1, 0xE, 0xC, 0x3, 0x8, 0x7, 0x5, 0xA], # F
    ]

    def __init__(self, plaintext: str = "", keys: str = "", log_file: str = "mini_aes_log.txt"):
        self.__plaintext = plaintext
        self.__keys = keys
        self.__round_keys: list[list[int]] = []
        self.__ciphertext = ""
        self.log_file = log_file

        with open(self.log_file, "w") as f:
            f.write("Mini AES Encryption/Decryption Log\n\n")

    def log(self, message: str) -> None:
        with open(self.log_file, "a") as f:
            f.write(message + "\n")
        print(message)

    # Getter and Setter for __ciphertext
    def set_ciphertext(self, ciphertext: str) -> None:
        self.__ciphertext = ciphertext

    def get_ciphertext(self) -> str:
        return self.__ciphertext

    # Getter and Setter for __plaintext
    def set_plaintext(self, plaintext: str) -> None:
        self.__plaintext = plaintext

    def get_plaintext(self) -> str:
        return self.__plaintext

    # Getter and Setter for __keys
    def set_keys(self, keys: str) -> None:
        # make at least the length of the keys is 2
        while len(keys) < 2:
            # append with "0"
            keys += "0"

        self.__keys = keys

    def get_keys(self) -> str:
        return self.__keys

    # Getter and Setter for __round_keys
    def set_round_keys(self, keys: list[list[int]]) -> None:
        self.__round_keys = keys

    def get_round_keys(self) -> list[list[int]]:
        return self.__round_keys

    def convert_to_nibble(self, text: str) -> list[int]:
        res: list[int] = []
        copy_of_text = text

        # defensive measure
        if len(text) == 0:
            raise ValueError("plaintext must not be empty")

        # check if plaintext is divisible by 2
        # if not, pad the plaintext with a '0' character
        if len(text) & 1:
            copy_of_text += "0"

        for char in copy_of_text:
            res.append(int(char, 16))

        return res

    def round_key_generator(self) -> None:
        round_keys: list[list[int]] = []

        # keys
        if self.get_keys() == "":
            self.set_keys("0000")

        keys = self.get_keys()

        # round 0
        round_0_keys: list[int] = []
        round_0_keys.append(int(keys[0], 16))
        round_0_keys.append(int(keys[1], 16))
        round_0_keys.append(int(keys[2], 16))
        round_0_keys.append(int(keys[3], 16))

        round_keys.append(round_0_keys)

        # round = 3
        # but needed more for round 0 (plus 1) and the last one (plus 1)
        for i in range(self.__ROUND__):
            this_round_keys: list[int] = []

            this_round_keys.append(round_keys[i][0] ^ self.__SBOX__[round_keys[i][3]] ^ i)
            this_round_keys.append(round_keys[i][1] ^ this_round_keys[0])
            this_round_keys.append(round_keys[i][2] ^ this_round_keys[1])
            this_round_keys.append(round_keys[i][3] ^ this_round_keys[2])

            round_keys.append(this_round_keys)

        self.set_round_keys(round_keys)

        return

    def sub_nibbles(self, state: list[int]) -> list[int]:
        for i in range(0, len(state)):
            state[i] = self.__SBOX__[state[i]]

        return state

    def shift_rows(self, state: list[int]) -> list[int]:
        return [state[0], state[3], state[2], state[1]]

    def mix_columns(self, state: list[int]) -> list[int]:
        __CONSTANT_MATRIX = [
            0x1, 0x4, 0x4, 0x1,
        ]

        res: list[int] = []

        # index 0
        index_zero = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[0]][state[0]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[2]][state[1]]
            )
        res.append(index_zero)

        # index 1
        index_one = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[1]][state[0]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[3]][state[1]]
            )
        res.append(index_one)

        # index 2
        index_two = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[0]][state[2]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[2]][state[3]]
            )
        res.append(index_two)

        # index 3
        index_three = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[1]][state[2]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[3]][state[3]]
            )
        res.append(index_three)

        return res

    def add_round_keys(
        self, state: list[int], round: int
    ) -> list[int]:
        result: list[int] = []

        round_keys = self.get_round_keys()

        for s, k in zip(state, round_keys[round]):
            result.append(s ^ k)

        return result

    def state_to_hex(self, state: list[int]) -> str:
        # Converts the first block of encryption state into a hex string (for output)
        result = ""
        
        for num in state:
            result += format(num, "X")

        return result


    def encrypt(self) -> list[int]:
        self.round_key_generator()
        self.log(f"Using Keys: {self.get_round_keys()}")

        state = self.convert_to_nibble(self.get_plaintext())
        self.log(f"Encrypting {self.state_to_hex(state)}")

        state = self.add_round_keys(state, 0)
        self.log(f"After RoundKeys: {self.state_to_hex(state)}")

        for current_round in range(1, self.__ROUND__):
            self.log(f"ROUND {current_round}")

            state = self.sub_nibbles(state)
            self.log(f"After SubNibbles: {self.state_to_hex(state)}")

            state = self.shift_rows(state)
            self.log(f"After ShiftRows : {self.state_to_hex(state)}")

            state = self.mix_columns(state)
            self.log(f"After MixColumns: {self.state_to_hex(state)}")

            state = self.add_round_keys(state, current_round)
            self.log(f"After AddRoundKey: {self.state_to_hex(state)}")

        self.log("FINAL ROUND")
        state = self.sub_nibbles(state)
        self.log(f"After SubNibbles: {self.state_to_hex(state)}")

        state = self.shift_rows(state)
        self.log(f"After ShiftRows : {self.state_to_hex(state)}")

        state = self.add_round_keys(state, 3)
        self.log(f"After AddRoundKey: {self.state_to_hex(state)}")

        self.log("Encrypt COMPLETE")

        self.log(f"Ciphertext: {self.state_to_hex(state)}")

        self.set_ciphertext(self.state_to_hex(state))

        return state

    def inv_sub_nibbles(self, state: list[int]) -> list[int]:
        for i in range(0, len(state)):
            state[i] = self.__INV_SBOX__[state[i]]

        return state

    def inv_shift_rows(self, state: list[int]) -> list[int]:
        return [state[0], state[3], state[2], state[1]]

    def inv_mix_columns(self, state: list[int]) -> list[int]:
        __CONSTANT_MATRIX = [
            0x9, 0x2, 0x2, 0x9,
        ]

        res: list[int] = []

        # index 0
        index_zero = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[0]][state[0]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[2]][state[1]]
            )
        res.append(index_zero)

        # index 1
        index_one = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[1]][state[0]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[3]][state[1]]
            )
        res.append(index_one)

        # index 2
        index_two = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[0]][state[2]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[2]][state[3]]
            )
        res.append(index_two)

        # index 3
        index_three = (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[1]][state[2]]) ^ (
            self.__MULTIPLICATION_TABLE__[__CONSTANT_MATRIX[3]][state[3]]
            )
        res.append(index_three)

        return res

    def decrypt(self) -> list[int]:
        self.log(f"Using Keys: {self.get_round_keys()}")

        self.log("Decrypting from final round...")

        state = self.convert_to_nibble(self.get_ciphertext())
        self.log(f"Decrypting {self.state_to_hex(state)}")

        state = self.add_round_keys(state, 3)
        self.log(f"After InvRoundKeys {self.state_to_hex(state)}")

        state = self.inv_shift_rows(state)
        self.log(f"After InvShiftRows {self.state_to_hex(state)}")

        state = self.inv_sub_nibbles(state)
        self.log(f"After InvSubNibbles {self.state_to_hex(state)}")

        for current_round in range(2, 0, -1):
            self.log(f"ROUND {current_round}")

            state = self.add_round_keys(state, current_round)
            self.log(f"After InvRoundKeys: {self.state_to_hex(state)}")

            state = self.inv_mix_columns(state)
            self.log(f"After InvMixColumns: {self.state_to_hex(state)}")

            state = self.inv_shift_rows(state)
            self.log(f"After InvShiftRows : {self.state_to_hex(state)}")

            state = self.inv_sub_nibbles(state)
            self.log(f"After InvSubNibbles : {self.state_to_hex(state)}")

        self.log("FINAL INVERSE ROUND")

        state = self.add_round_keys(state, 0)
        self.log(f"After InvRoundKeys: {self.state_to_hex(state)}")

        self.log("Decrypt COMPLETE")
        self.log(f"Plaintext: {self.state_to_hex(state)}")

        return state

# main_class = MiniAes("AFFA", "FAFA")
# main_class.encrypt()
# main_class.decrypt()
