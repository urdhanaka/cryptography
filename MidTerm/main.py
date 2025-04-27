import flet as ft
from mini_aes import MiniAes

def main(page: ft.Page):
    page.title = "Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 700
    page.padding = 20

    status_text = ft.Text(value="", color=ft.colors.RED)

    # Input fields
    key_field = ft.TextField(
<<<<<<< HEAD
        label="Kunci (4 Hex Digit)",  # updated label
        hint_text="Masukkan kunci 4 karakter hex",  # updated hint
=======
        label="Kunci (4 Hex Digit)",
        hint_text="Masukkan kunci 4 karakter hex",
>>>>>>> 83b4839 (Update Mini AES: perbaikan main.py dan mini_aes.py)
        width=400,
        text_align=ft.TextAlign.CENTER
    )

    plain_text_field = ft.TextField(
<<<<<<< HEAD
        label="Plaintext (4 Hex Digit)",  # updated label
        hint_text="Masukkan plaintext 4 karakter hex",  # updated hint
=======
        label="Plaintext (4 Hex Digit)",
        hint_text="Masukkan plaintext 4 karakter hex",
>>>>>>> 83b4839 (Update Mini AES: perbaikan main.py dan mini_aes.py)
        width=400,
        text_align=ft.TextAlign.CENTER
    )

    cipher_text_field = ft.TextField(
<<<<<<< HEAD
        label="Ciphertext (4 Hex Digit)",  # updated label
        hint_text="Masukkan ciphertext 4 karakter hex",  # updated hint
=======
        label="Ciphertext (4 Hex Digit)",
        hint_text="Masukkan ciphertext 4 karakter hex",
>>>>>>> 83b4839 (Update Mini AES: perbaikan main.py dan mini_aes.py)
        width=400,
        text_align=ft.TextAlign.CENTER
    )

    progress = ft.ProgressRing(width=16, height=16, visible=False)

    aes = MiniAes()

    # Clear all fields
    def clear_fields():
        plain_text_field.value = ""
        cipher_text_field.value = ""
        status_text.value = ""
        page.update()

    def encrypt(e):
        progress.visible = True
        status_text.value = ""
        page.update()

        try:
            if not key_field.value or not plain_text_field.value:
                status_text.value = "Kunci dan Plaintext harus diisi!"
                progress.visible = False
                page.update()
                return
            aes.set_plaintext(plain_text_field.value.upper())
            aes.set_keys(key_field.value.upper())
            encrypted_state = aes.encrypt()
            cipher_text_field.value = aes.state_to_hex(encrypted_state)  #using `state_to_hex`
            status_text.value = "Enkripsi berhasil"

        except Exception as err:
            status_text.value = f"Error: {str(err)}"

        progress.visible = False
        page.update()

    # On progress
    def decrypt(e):
        progress.visible = True
        status_text.value = ""
        page.update()

        try:
            status_text.value = "Fitur dekripsi belum tersedia"
        except Exception as err:
            status_text.value = f"Error: {str(err)}"

        progress.visible = False
        page.update()

    def save_to_file(e):
        try:
            content = f"Key: {key_field.value}\nPlaintext: {plain_text_field.value}\nCiphertext: {cipher_text_field.value}"
            with open("output.txt", "w") as f:
                f.write(content)
            status_text.value = "Output disimpan ke output.txt"
        except Exception as err:
            status_text.value = f"Gagal menyimpan file: {str(err)}"
        page.update()

    def load_from_file(e):
        try:
            with open("output.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("Key: "):
                        key_field.value = line.strip().split("Key: ")[-1]
                    if line.startswith("Plaintext: "):
                        plain_text_field.value = line.strip().split("Plaintext: ")[-1]
                    if line.startswith("Ciphertext: "):
                        cipher_text_field.value = line.strip().split("Ciphertext: ")[-1]
            status_text.value = "Data diambil dari output.txt"
        except Exception as err:
            status_text.value = f"Gagal memuat file: {str(err)}"
        page.update()

    # Buttons
    encrypt_btn = ft.ElevatedButton("Enkripsi", on_click=encrypt, width=130)
    decrypt_btn = ft.ElevatedButton("Dekripsi", on_click=decrypt, width=130)
    clear_btn = ft.OutlinedButton("Bersihkan", on_click=lambda _: clear_fields(), width=130)
    save_btn = ft.OutlinedButton("Simpan ke File", on_click=save_to_file, width=150)
    load_btn = ft.OutlinedButton("Muat dari File", on_click=load_from_file, width=150)

    # Title
    title = ft.Text("MiniAES Encryption/Decryption", size=20, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Implementasi Mini-AES 16-bit", size=14, italic=True)

    page.add(
        ft.Column([
            title,
            subtitle,
            ft.Divider(),
            key_field,
            plain_text_field,
            cipher_text_field,
            ft.Container(height=20),
            ft.Row([encrypt_btn, decrypt_btn, clear_btn, progress], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Row([save_btn, load_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            status_text
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)