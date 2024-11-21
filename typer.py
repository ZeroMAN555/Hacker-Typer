import curses
import time
import os
import pyfiglet

# Fungsi untuk menampilkan judul besar
def display_title():
    title = pyfiglet.figlet_format("HACKER TYPER")
    subtitle = "By ZeroMAN555"
    print(title)
    print(subtitle)
    print("=" * 30)  # Garis pemisah

# Fungsi utama untuk menampilkan simulasi editor nano dengan efek ketikan otomatis
def nano_editor_simulation(stdscr, text, file_name="untitled.txt"):
    curses.curs_set(0)  # Menyembunyikan kursor asli untuk efek sinematik
    stdscr.clear()

    # Mendapatkan ukuran layar terminal
    height, width = stdscr.getmaxyx()
    view_height = height - 3  # Area yang terlihat untuk kode (mengurangi header dan footer)
    lines = text.splitlines()  # Memisahkan teks menjadi baris-baris

    # Header dan footer nano-style
    header = f" GNU nano 5.8: {file_name} "
    status_bar = f" File: {file_name}                          Modified    "
    footer_bar = "^G Get Help  ^O Write Out  ^R Read File  ^Y Prev Page  ^K Cut Text  ^C Cur Pos"

    # Pengaturan offset awal untuk scrolling dan efek ketikan
    offset = 0
    max_offset = max(0, len(lines) - view_height)
    typed_lines = [""] * len(lines)  # Menyimpan baris "diketik" secara bertahap

    # Menampilkan header dan footer satu kali
    stdscr.addstr(0, 0, header + " " * (width - len(header)), curses.A_REVERSE)
    stdscr.addstr(height - 2, 0, status_bar + " " * (width - len(status_bar)), curses.A_REVERSE)
    stdscr.addstr(height - 1, 0, footer_bar)
    stdscr.refresh()

    # Mengetik otomatis seluruh teks
    line_idx, char_idx = 0, 0

    while line_idx < len(lines):
        # Menangani input pengguna
        key = stdscr.getch()

        if key == curses.KEY_BACKSPACE or key == 127:  # Backspace untuk menghapus karakter
            if char_idx > 0:
                char_idx -= 1
                typed_lines[line_idx] = typed_lines[line_idx][:-1]
            elif line_idx > 0:  # Pindah ke baris sebelumnya jika di awal baris
                line_idx -= 1
                char_idx = len(typed_lines[line_idx])
        elif key == curses.KEY_UP and offset > 0:  # Scroll ke atas
            offset -= 1
        elif key == curses.KEY_DOWN and offset < max_offset:  # Scroll ke bawah
            offset += 1
        elif key == ord('q'):  # Tekan 'q' untuk keluar
            break
        else:
            # Menambahkan karakter secara normal
            if char_idx < len(lines[line_idx]):
                typed_lines[line_idx] += lines[line_idx][char_idx]
                char_idx += 1
            else:
                char_idx = 0
                line_idx += 1
                if line_idx >= len(lines):
                    break

        # Menampilkan teks berdasarkan posisi offset
        for i in range(view_height):
            line_to_display = offset + i
            if line_to_display < len(typed_lines):
                stdscr.addstr(i + 1, 0, typed_lines[line_to_display][:width].ljust(width))
            else:
                stdscr.addstr(i + 1, 0, " " * width)

        # Menampilkan kotak (kursor) di akhir teks yang sedang diketik
        if line_idx < len(lines):
            cursor_row = line_idx - offset + 1
            cursor_col = len(typed_lines[line_idx]) % width
            if 0 <= cursor_row < view_height:
                stdscr.addstr(cursor_row, cursor_col, "█", curses.A_REVERSE)  # Kursor tetap di ujung teks

        stdscr.refresh()
        time.sleep(0.02)  # Jeda ketikan otomatis untuk efek yang lebih cepat dan responsif

# Fungsi untuk menampilkan editor nano dengan kode yang dimuat
def display_code(code_text, file_name="untitled.txt"):
    curses.wrapper(nano_editor_simulation, code_text, file_name)

# Fungsi utama untuk menjalankan program
def main():
    display_title()
    print("Pilih metode input kode:")
    print("1. Masukkan kode secara manual")
    print("2. Muat kode dari file")
    choice = input("Masukkan pilihan (1 atau 2): ")

    if choice == "1":
        print("\nMasukkan kode di bawah ini. Ketik 'END' pada baris baru untuk selesai:\n")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        code_text = "\n".join(lines)
        file_name = "untitled.txt"

    elif choice == "2":
        file_path = input("\nMasukkan path file: ")
        try:
            with open(file_path, "r") as file:
                code_text = file.read()
            # Mengambil nama file dan ekstensi untuk tampilan nano
            file_name = os.path.basename(file_path)
        except FileNotFoundError:
            print("File tidak ditemukan.")
            return
    else:
        print("Pilihan tidak valid.")
        return

    # Menampilkan kode dengan simulasi editor nano
    display_code(code_text, file_name)

# Memulai program utama
if __name__ == "__main__":
    main()
