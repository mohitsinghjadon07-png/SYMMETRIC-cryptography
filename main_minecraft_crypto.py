import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ============================================================
# PYCRYPTODOME
# ============================================================

try:
    from Crypto.Cipher import AES
except ImportError:
    AES = None


# ============================================================
# MINECRAFT THEME
# ============================================================

BG = "#10140f"
BLACK = "#080a07"
PANEL_BG = "#1b2118"
PANEL_ALT = "#242c20"

STONE_DARK = "#30382b"
STONE = "#4a5540"

GRASS_DARK = "#355c2a"
GRASS = "#4d7c32"
GRASS_LIGHT = "#7aa64b"

WHITE = "#f2f2e8"
TEXT = "#d9e3cf"
MUTED = "#9eaa94"

RED = "#a83b32"
GOLD = "#d3a23c"


# ============================================================
# AES SETTINGS
# ============================================================

BLOCK_SIZE = 16


def require_crypto():
    if AES is None:
        raise RuntimeError(
            "PyCryptodome is not installed.\n\n"
            "Run this command:\n"
            "python -m pip install pycryptodome"
        )


# ============================================================
# PKCS#7 PADDING
# ============================================================

def pkcs7_pad(data):
    padding = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([padding]) * padding


def pkcs7_unpad(data):

    if not data:
        raise ValueError("Empty decrypted data.")

    if len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid block size.")

    padding = data[-1]

    if padding < 1 or padding > BLOCK_SIZE:
        raise ValueError("Invalid PKCS#7 padding.")

    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid PKCS#7 padding.")

    return data[:-padding]


# ============================================================
# AES-256-ECB
# ============================================================

def generate_key():
    return os.urandom(32)


def key_to_text(key):
    return base64.urlsafe_b64encode(key).decode("ascii")


def text_to_key(text):

    try:
        key = base64.urlsafe_b64decode(text.strip())
    except Exception:
        raise ValueError("Invalid Base64 key.")

    if len(key) != 32:
        raise ValueError(
            "AES-256 requires a 32-byte key."
        )

    return key


def encrypt_bytes(data, key):

    require_crypto()

    cipher = AES.new(key, AES.MODE_ECB)

    padded = pkcs7_pad(data)

    return cipher.encrypt(padded)


def decrypt_bytes(data, key):

    require_crypto()

    if not data:
        raise ValueError("Ciphertext is empty.")

    if len(data) % BLOCK_SIZE != 0:
        raise ValueError(
            "Invalid ciphertext length."
        )

    cipher = AES.new(key, AES.MODE_ECB)

    decrypted = cipher.decrypt(data)

    return pkcs7_unpad(decrypted)


def encrypt_text(text, key):

    encrypted = encrypt_bytes(
        text.encode("utf-8"),
        key
    )

    return base64.b64encode(encrypted).decode("ascii")


def decrypt_text(ciphertext, key):

    try:
        encrypted = base64.b64decode(
            ciphertext.strip()
        )
    except Exception:
        raise ValueError(
            "Invalid Base64 ciphertext."
        )

    decrypted = decrypt_bytes(
        encrypted,
        key
    )

    return decrypted.decode("utf-8")


# ============================================================
# CLASSICAL CIPHERS
# ============================================================

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def caesar_transform(text, shift):

    result = ""

    for ch in text:

        if ch.isupper():

            result += chr(
                (ord(ch) - ord("A") + shift) % 26
                + ord("A")
            )

        elif ch.islower():

            result += chr(
                (ord(ch) - ord("a") + shift) % 26
                + ord("a")
            )

        else:

            result += ch

    return result


def rot13(text):

    return caesar_transform(text, 13)


def atbash_transform(text):

    result = ""

    for ch in text:

        if ch.isupper():

            result += chr(
                ord("Z") - (ord(ch) - ord("A"))
            )

        elif ch.islower():

            result += chr(
                ord("z") - (ord(ch) - ord("a"))
            )

        else:

            result += ch

    return result


def rail_fence_encode(text, rails):

    if rails <= 1 or len(text) <= 1:
        return text

    rows = [[] for _ in range(rails)]

    row = 0
    direction = 1

    for ch in text:

        rows[row].append(ch)

        if row == 0:
            direction = 1

        elif row == rails - 1:
            direction = -1

        row += direction

    return "".join(
        "".join(row_data)
        for row_data in rows
    )


# ============================================================
# PIXEL BUTTON
# ============================================================

class PixelButton(tk.Button):

    def __init__(
        self,
        master,
        text,
        command,
        width=20,
        **kwargs
    ):

        kwargs.setdefault(
            "bg",
            STONE_DARK
        )

        kwargs.setdefault(
            "fg",
            WHITE
        )

        kwargs.setdefault(
            "activebackground",
            GRASS_DARK
        )

        kwargs.setdefault(
            "activeforeground",
            WHITE
        )

        kwargs.setdefault(
            "relief",
            "raised"
        )

        kwargs.setdefault(
            "bd",
            3
        )

        kwargs.setdefault(
            "cursor",
            "hand2"
        )

        kwargs.setdefault(
            "padx",
            8
        )

        kwargs.setdefault(
            "pady",
            7
        )

        kwargs.setdefault(
            "font",
            ("Consolas", 10, "bold")
        )

        super().__init__(
            master,
            text=text,
            command=command,
            width=width,
            **kwargs
        )


# ============================================================
# PIXEL PANEL
# ============================================================

class PixelPanel(tk.Frame):

    def __init__(
        self,
        master,
        title="",
        **kwargs
    ):

        kwargs.setdefault(
            "bg",
            PANEL_BG
        )

        kwargs.setdefault(
            "bd",
            3
        )

        kwargs.setdefault(
            "relief",
            "raised"
        )

        super().__init__(
            master,
            **kwargs
        )

        if title:

            title_frame = tk.Frame(
                self,
                bg=STONE_DARK,
                height=36
            )

            title_frame.pack(
                fill="x"
            )

            title_frame.pack_propagate(
                False
            )

            tk.Label(
                title_frame,
                text=title,
                bg=STONE_DARK,
                fg=WHITE,
                font=(
                    "Consolas",
                    11,
                    "bold"
                ),
                anchor="w",
                padx=12
            ).pack(
                fill="both",
                expand=True
            )

        self.body = tk.Frame(
            self,
            bg=PANEL_BG
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )


# ============================================================
# SCROLLABLE FRAME
# ============================================================

class ScrollableFrame(tk.Frame):

    def __init__(self, master):

        super().__init__(
            master,
            bg=BG
        )

        self.canvas = tk.Canvas(
            self,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.content = tk.Frame(
            self.canvas,
            bg=BG
        )

        self.window_id = (
            self.canvas.create_window(
                (0, 0),
                window=self.content,
                anchor="nw"
            )
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.content.bind(
            "<Configure>",
            self._update_scroll
        )

        self.canvas.bind(
            "<Configure>",
            self._resize_content
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self._mousewheel
        )

    def _update_scroll(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _resize_content(self, event):

        self.canvas.itemconfigure(
            self.window_id,
            width=event.width
        )

    def _mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-event.delta / 120),
            "units"
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

class CryptoApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Minecraft Symmetric Cryptography Lab"
        )

        self.root.geometry(
            "1200x850"
        )

        self.root.minsize(
            900,
            650
        )

        self.root.configure(
            bg=BG
        )

        self.key = generate_key()

        self.algorithm_frames = {}

        self.algorithm_buttons = {}

        self.build_ui()

        self.show_algorithm(
            "caesar"
        )

    # ========================================================
    # COMMON LABEL
    # ========================================================

    def label(
        self,
        parent,
        text,
        size=10,
        bold=False,
        color=TEXT,
        **kwargs
    ):

        return tk.Label(
            parent,
            text=text,
            bg=kwargs.pop(
                "bg",
                parent.cget("bg")
            ),
            fg=color,
            font=(
                "Consolas",
                size,
                "bold" if bold else "normal"
            ),
            **kwargs
        )

    # ========================================================
    # TEXT BOX
    # ========================================================

    def text_box(
        self,
        parent,
        height=8
    ):

        return tk.Text(
            parent,
            height=height,
            bg=BLACK,
            fg=TEXT,
            insertbackground=WHITE,
            selectbackground=GRASS,
            selectforeground=WHITE,
            relief="sunken",
            bd=2,
            font=("Consolas", 10),
            wrap="word"
        )

    # ========================================================
    # BUILD UI
    # ========================================================

    def build_ui(self):

        # HEADER

        header = tk.Frame(
            self.root,
            bg=BLACK,
            height=85
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text="▣  SYMMETRIC CRYPTOGRAPHY LAB",
            bg=BLACK,
            fg=GRASS_LIGHT,
            font=(
                "Consolas",
                21,
                "bold"
            )
        ).pack(
            pady=(12, 0)
        )

        tk.Label(
            header,
            text="MINECRAFT EDITION  •  AES-256-ECB + CLASSICAL CIPHERS",
            bg=BLACK,
            fg=MUTED,
            font=(
                "Consolas",
                9,
                "bold"
            )
        ).pack(
            pady=(3, 0)
        )

        # SCROLL AREA

        self.scroller = ScrollableFrame(
            self.root
        )

        self.scroller.pack(
            fill="both",
            expand=True
        )

        content = self.scroller.content

        self.build_key_section(
            content
        )

        self.build_crypto_section(
            content
        )

        self.build_algorithm_section(
            content
        )

        self.build_info_section(
            content
        )

    # ========================================================
    # KEY SECTION
    # ========================================================

    def build_key_section(self, parent):

        panel = PixelPanel(
            parent,
            "1. § SECRET KEY  —  AES-256"
        )

        panel.pack(
            fill="x",
            padx=14,
            pady=(14, 8)
        )

        body = panel.body

        self.key_var = tk.StringVar(
            value=key_to_text(
                self.key
            )
        )

        self.label(
            body,
            "256-bit Secret Key (Base64)",
            bold=True
        ).pack(
            anchor="w"
        )

        row = tk.Frame(
            body,
            bg=PANEL_BG
        )

        row.pack(
            fill="x",
            pady=5
        )

        self.key_entry = tk.Entry(
            row,
            textvariable=self.key_var,
            bg=BLACK,
            fg=TEXT,
            insertbackground=WHITE,
            relief="sunken",
            bd=2,
            font=("Consolas", 10)
        )

        self.key_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )

        PixelButton(
            row,
            "GENERATE NEW KEY",
            self.generate_new_key,
            width=20,
            bg=GRASS_DARK
        ).pack(
            side="left",
            padx=6
        )

        PixelButton(
            row,
            "COPY KEY",
            self.copy_key,
            width=12
        ).pack(
            side="left"
        )

        self.label(
            body,
            "The same secret key is required to decrypt the data.",
            color=MUTED
        ).pack(
            anchor="w"
        )

    # ========================================================
    # CRYPTO SECTION
    # ========================================================

    def build_crypto_section(self, parent):

        panel = PixelPanel(
            parent,
            "2. § AES-256-ECB ENCRYPTION / DECRYPTION"
        )

        panel.pack(
            fill="x",
            padx=14,
            pady=8
        )

        body = panel.body

        self.label(
            body,
            "PLAINTEXT / CIPHERTEXT",
            bold=True,
            color=GOLD
        ).pack(
            anchor="w"
        )

        self.crypto_text = self.text_box(
            body,
            8
        )

        self.crypto_text.pack(
            fill="x",
            pady=5
        )

        row = tk.Frame(
            body,
            bg=PANEL_BG
        )

        row.pack(
            fill="x",
            pady=5
        )

        PixelButton(
            row,
            "ENCRYPT TEXT",
            self.encrypt_text,
            width=18,
            bg=GRASS_DARK
        ).pack(
            side="left",
            padx=4
        )

        PixelButton(
            row,
            "DECRYPT TEXT",
            self.decrypt_text,
            width=18
        ).pack(
            side="left",
            padx=4
        )

        PixelButton(
            row,
            "CLEAR",
            self.clear_text,
            width=10
        ).pack(
            side="left",
            padx=4
        )

        self.label(
            body,
            "FILE OPERATIONS",
            bold=True,
            color=GOLD
        ).pack(
            anchor="w",
            pady=(10, 3)
        )

        file_row = tk.Frame(
            body,
            bg=PANEL_BG
        )

        file_row.pack(
            fill="x"
        )

        PixelButton(
            file_row,
            "ENCRYPT FILE",
            self.encrypt_file,
            width=18,
            bg=GRASS_DARK
        ).pack(
            side="left",
            padx=4
        )

        PixelButton(
            file_row,
            "DECRYPT FILE",
            self.decrypt_file,
            width=18
        ).pack(
            side="left",
            padx=4
        )

        self.status_var = tk.StringVar(
            value="STATUS: READY"
        )

        self.status_label = tk.Label(
            body,
            textvariable=self.status_var,
            bg=BLACK,
            fg=GRASS_LIGHT,
            font=(
                "Consolas",
                10,
                "bold"
            ),
            anchor="w",
            padx=10,
            pady=8
        )

        self.status_label.pack(
            fill="x",
            pady=(12, 0)
        )

    # ========================================================
    # ALGORITHM SECTION
    # ========================================================

    def build_algorithm_section(
        self,
        parent
    ):

        panel = PixelPanel(
            parent,
            "3. § CLASSICAL CIPHER ALGORITHM LAB"
        )

        panel.pack(
            fill="x",
            padx=14,
            pady=8
        )

        body = panel.body

        self.label(
            body,
            "Select an algorithm to see its real transformation.",
            color=MUTED
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        selector = tk.Frame(
            body,
            bg=PANEL_BG
        )

        selector.pack(
            fill="x",
            pady=(0, 10)
        )

        algorithms = [
            (
                "caesar",
                "1. CAESAR CIPHER (SHIFT)"
            ),
            (
                "rot13",
                "2. ROT13"
            ),
            (
                "atbash",
                "3. ATBASH (REVERSE ALPHABET)"
            ),
            (
                "rail",
                "4. RAIL FENCE"
            )
        ]

        for key, title in algorithms:

            button = PixelButton(
                selector,
                title,
                lambda k=key:
                    self.show_algorithm(k),
                width=24
            )

            button.pack(
                side="left",
                padx=3,
                fill="x",
                expand=True
            )

            self.algorithm_buttons[
                key
            ] = button

        self.algorithm_container = tk.Frame(
            body,
            bg=PANEL_BG
        )

        self.algorithm_container.pack(
            fill="x"
        )

        self.create_caesar(
            self.algorithm_container
        )

        self.create_rot13(
            self.algorithm_container
        )

        self.create_atbash(
            self.algorithm_container
        )

        self.create_rail(
            self.algorithm_container
        )

    # ========================================================
    # CAESAR
    # ========================================================

    def create_caesar(self, parent):

        frame = tk.Frame(
            parent,
            bg=PANEL_ALT,
            bd=2,
            relief="sunken"
        )

        self.algorithm_frames[
            "caesar"
        ] = frame

        self.label(
            frame,
            "CAESAR CIPHER — SHIFT EACH LETTER",
            size=11,
            bold=True,
            color=GOLD
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 6)
        )

        row = tk.Frame(
            frame,
            bg=PANEL_ALT
        )

        row.pack(
            fill="x",
            padx=12
        )

        self.label(
            row,
            "Input:",
            bold=True
        ).pack(
            side="left"
        )

        self.caesar_input = tk.Entry(
            row,
            bg=BLACK,
            fg=TEXT,
            insertbackground=WHITE,
            font=("Consolas", 10)
        )

        self.caesar_input.insert(
            0,
            "HELLO WORLD"
        )

        self.caesar_input.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
            ipady=5
        )

        self.label(
            row,
            "Shift:",
            bold=True
        ).pack(
            side="left"
        )

        self.caesar_shift = tk.Spinbox(
            row,
            from_=0,
            to=25,
            width=5,
            bg=BLACK,
            fg=TEXT,
            buttonbackground=STONE,
            insertbackground=WHITE,
            font=("Consolas", 10)
        )

        self.caesar_shift.delete(
            0,
            "end"
        )

        self.caesar_shift.insert(
            0,
            "3"
        )

        self.caesar_shift.pack(
            side="left",
            padx=7
        )

        PixelButton(
            row,
            "TRANSFORM",
            self.update_caesar,
            width=13,
            bg=GRASS_DARK
        ).pack(
            side="left"
        )

        self.caesar_map = tk.Label(
            frame,
            bg=BLACK,
            fg=GRASS_LIGHT,
            font=(
                "Consolas",
                11,
                "bold"
            ),
            justify="left",
            anchor="w",
            padx=12,
            pady=10
        )

        self.caesar_map.pack(
            fill="x",
            padx=12,
            pady=10
        )

        self.caesar_output = tk.Label(
            frame,
            bg=BLACK,
            fg=WHITE,
            font=(
                "Consolas",
                12,
                "bold"
            ),
            justify="left",
            anchor="w",
            padx=12,
            pady=10
        )

        self.caesar_output.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        self.update_caesar()

    # ========================================================
    # ROT13
    # ========================================================

    def create_rot13(self, parent):

        frame = tk.Frame(
            parent,
            bg=PANEL_ALT,
            bd=2,
            relief="sunken"
        )

        self.algorithm_frames[
            "rot13"
        ] = frame

        self.label(
            frame,
            "ROT13 — CAESAR CIPHER WITH SHIFT 13",
            size=11,
            bold=True,
            color=GOLD
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 6)
        )

        row = tk.Frame(
            frame,
            bg=PANEL_ALT
        )

        row.pack(
            fill="x",
            padx=12
        )

        self.label(
            row,
            "Input:",
            bold=True
        ).pack(
            side="left"
        )

        self.rot13_input = tk.Entry(
            row,
            bg=BLACK,
            fg=TEXT,
            insertbackground=WHITE,
            font=("Consolas", 10)
        )

        self.rot13_input.insert(
            0,
            "HELLO WORLD"
        )

        self.rot13_input.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
            ipady=5
        )

        PixelButton(
            row,
            "ROTATE 13",
            self.update_rot13,
            width=14,
            bg=GRASS_DARK
        ).pack(
            side="left"
        )

        mapping = (
            "A B C D E F G H I J K L M\n"
            "↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓\n"
            "N O P Q R S T U V W X Y Z\n\n"
            "N O P Q R S T U V W X Y Z\n"
            "↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓\n"
            "A B C D E F G H I J K L M"
        )

        tk.Label(
            frame,
            text=mapping,
            bg=BLACK,
            fg=GRASS_LIGHT,
            font=(
                "Consolas",
                11,
                "bold"
            ),
            justify="center",
            pady=10
        ).pack(
            fill="x",
            padx=12,
            pady=10
        )

        self.rot13_output = tk.Label(
            frame,
            bg=BLACK,
            fg=WHITE,
            font=(
                "Consolas",
                12,
                "bold"
            ),
            anchor="w",
            padx=12,
            pady=10
        )

        self.rot13_output.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        self.update_rot13()

    # ========================================================
    # ATBASH
    # ========================================================

    def create_atbash(self, parent):

        frame = tk.Frame(
            parent,
            bg=PANEL_ALT,
            bd=2,
            relief="sunken"
        )

        self.algorithm_frames[
            "atbash"
        ] = frame

        self.label(
            frame,
            "ATBASH — REVERSE ALPHABET",
            size=11,
            bold=True,
            color=GOLD
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 6)
        )

        row = tk.Frame(
            frame,
            bg=PANEL_ALT
        )

        row.pack(
            fill="x",
            padx=12
        )

        self.label(
            row,
            "Input:",
            bold=True
        ).pack(
            side="left"
        )

        self.atbash_input = tk.Entry(
            row,
            bg=BLACK,
            fg=TEXT,
            insertbackground=WHITE,
            font=("Consolas", 10)
        )

        self.atbash_input.insert(
            0,
            "HELLO WORLD"
        )

        self.atbash_input.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
            ipady=5
        )

        PixelButton(
            row,
            "REVERSE ALPHABET",
            self.update_atbash,
            width=19,
            bg=GRASS_DARK
        ).pack(
            side="left"
        )

        mapping = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n"
            "↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓\n"
            "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        )

        tk.Label(
            frame,
            text=mapping,
            bg=BLACK,
            fg=GRASS_LIGHT,
            font=(
                "Consolas",
                10,
                "bold"
            ),
            justify="center",
            pady=10
        ).pack(
            fill="x",
            padx=12,
            pady=10
        )

        self.atbash_output = tk.Label(
            frame,
            bg=BLACK,
            fg=WHITE,
            font=(
                "Consolas",
                12,
                "bold"
            ),
            anchor="w",
            padx=12,
            pady=10
        )

        self.atbash_output.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        self.update_atbash()

    # ========================================================
    # RAIL FENCE
    # ========================================================

    def create_rail(self, parent):

        frame = tk.Frame(
            parent,
            bg=PANEL_ALT,
            bd=2,
            relief="sunken"
        )

        self.algorithm_frames[
            "rail"
        ] = frame

        self.label(
            frame,
            "RAIL FENCE — ZIG-ZAG TRANSPOSITION",
            size=11,
            bold=True,
            color=GOLD
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 6)
        )

        row = tk.Frame(
            frame,
            bg=PANEL_ALT
        )

        row.pack(
            fill="x",
            padx=12
        )

        self.label(
            row,
            "Input:",
            bold=True
        ).pack(
            side="left"
        )

        self.rail_input = tk.Entry(
            row,
            bg=BLACK,
            fg=TEXT,
            insertbackground=WHITE,
            font=("Consolas", 10)
        )

        self.rail_input.insert(
            0,
            "WEAREDISCOVEREDFLEEATONCE"
        )

        self.rail_input.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
            ipady=5
        )

        self.label(
            row,
            "Rails:",
            bold=True
        ).pack(
            side="left"
        )

        self.rail_count = tk.Spinbox(
            row,
            from_=2,
            to=6,
            width=5,
            bg=BLACK,
            fg=TEXT,
            buttonbackground=STONE,
            insertbackground=WHITE,
            font=("Consolas", 10)
        )

        self.rail_count.delete(
            0,
            "end"
        )

        self.rail_count.insert(
            0,
            "3"
        )

        self.rail_count.pack(
            side="left",
            padx=7
        )

        PixelButton(
            row,
            "DRAW ZIG-ZAG",
            self.update_rail,
            width=15,
            bg=GRASS_DARK
        ).pack(
            side="left"
        )

        self.rail_canvas = tk.Canvas(
            frame,
            height=200,
            bg=BLACK,
            highlightthickness=1,
            highlightbackground=STONE
        )

        self.rail_canvas.pack(
            fill="x",
            padx=12,
            pady=10
        )

        self.rail_output = tk.Label(
            frame,
            bg=BLACK,
            fg=WHITE,
            font=(
                "Consolas",
                12,
                "bold"
            ),
            anchor="w",
            padx=12,
            pady=10
        )

        self.rail_output.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        self.update_rail()

    # ========================================================
    # SHOW ALGORITHM
    # ========================================================

    def show_algorithm(self, key):

        for frame in self.algorithm_frames.values():

            frame.pack_forget()

        self.algorithm_frames[
            key
        ].pack(
            fill="x"
        )

        for name, button in self.algorithm_buttons.items():

            if name == key:

                button.configure(
                    bg=GRASS,
                    activebackground=GRASS_LIGHT
                )

            else:

                button.configure(
                    bg=STONE_DARK,
                    activebackground=GRASS_DARK
                )

    # ========================================================
    # CAESAR UPDATE
    # ========================================================

    def update_caesar(self):

        text = self.caesar_input.get()

        try:
            shift = int(
                self.caesar_shift.get()
            )
        except ValueError:
            shift = 3

        shift %= 26

        output = caesar_transform(
            text,
            shift
        )

        shifted = (
            ALPHABET[shift:]
            +
            ALPHABET[:shift]
        )

        self.caesar_map.configure(
            text=(
                "NORMAL : "
                + ALPHABET
                + "\n"
                "SHIFT  : "
                + shifted
                + "\n\n"
                f"A → {shifted[0]}    "
                f"B → {shifted[1]}    "
                f"C → {shifted[2]}"
            )
        )

        self.caesar_output.configure(
            text=(
                "OUTPUT: "
                + text
                + "  →  "
                + output
            )
        )

    # ========================================================
    # ROT13 UPDATE
    # ========================================================

    def update_rot13(self):

        text = self.rot13_input.get()

        output = rot13(
            text
        )

        self.rot13_output.configure(
            text=(
                "OUTPUT: "
                + text
                + "  →  "
                + output
            )
        )

    # ========================================================
    # ATBASH UPDATE
    # ========================================================

    def update_atbash(self):

        text = self.atbash_input.get()

        output = atbash_transform(
            text
        )

        self.atbash_output.configure(
            text=(
                "OUTPUT: "
                + text
                + "  →  "
                + output
            )
        )

    # ========================================================
    # RAIL FENCE UPDATE
    # ========================================================

    def update_rail(self):

        text = self.rail_input.get()

        clean_text = text.replace(
            " ",
            ""
        )

        try:
            rails = int(
                self.rail_count.get()
            )
        except ValueError:
            rails = 3

        rails = max(
            2,
            min(6, rails)
        )

        encoded = rail_fence_encode(
            clean_text,
            rails
        )

        self.rail_output.configure(
            text=(
                "ENCODED: "
                + encoded
            )
        )

        self.draw_rail(
            clean_text,
            rails
        )

    # ========================================================
    # DRAW RAIL FENCE
    # ========================================================

    def draw_rail(
        self,
        text,
        rails
    ):

        canvas = self.rail_canvas

        canvas.delete(
            "all"
        )

        if not text:
            return

        canvas.update_idletasks()

        width = max(
            canvas.winfo_width(),
            700
        )

        height = 200

        top = 30
        bottom = height - 30

        if rails == 1:

            gap_y = 0

        else:

            gap_y = (
                bottom - top
            ) / (
                rails - 1
            )

        step_x = min(
            35,
            max(
                18,
                (width - 40)
                /
                max(1, len(text))
            )
        )

        positions = []

        row = 0
        direction = 1

        for i, ch in enumerate(text):

            x = (
                25
                +
                i * step_x
            )

            y = (
                top
                +
                row * gap_y
            )

            positions.append(
                (
                    x,
                    y,
                    ch
                )
            )

            if row == 0:

                direction = 1

            elif row == rails - 1:

                direction = -1

            row += direction

        # Rail lines

        for r in range(rails):

            y = (
                top
                +
                r * gap_y
            )

            canvas.create_line(
                10,
                y,
                width - 10,
                y,
                fill=STONE,
                width=1
            )

        # Zig-zag lines

        for i in range(
            len(positions) - 1
        ):

            x1, y1, _ = positions[i]

            x2, y2, _ = positions[i + 1]

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=GRASS_DARK,
                width=2
            )

        # Character nodes

        for x, y, ch in positions:

            canvas.create_oval(
                x - 13,
                y - 13,
                x + 13,
                y + 13,
                fill=STONE_DARK,
                outline=GRASS,
                width=2
            )

            canvas.create_text(
                x,
                y,
                text=ch,
                fill=WHITE,
                font=(
                    "Consolas",
                    10,
                    "bold"
                )
            )

        canvas.create_text(
            12,
            10,
            anchor="w",
            text="ZIG-ZAG PATH",
            fill=MUTED,
            font=(
                "Consolas",
                8,
                "bold"
            )
        )

    # ========================================================
    # INFORMATION SECTION
    # ========================================================

    def build_info_section(
        self,
        parent
    ):

        panel = PixelPanel(
            parent,
            "4. § PROJECT INFORMATION"
        )

        panel.pack(
            fill="x",
            padx=14,
            pady=8
        )

        body = panel.body

        information = (
            "SYMMETRIC CRYPTOGRAPHY\n\n"

            "Symmetric encryption uses the same secret key "
            "for encryption and decryption.\n\n"

            "AES-256-ECB is used in this educational project "
            "to demonstrate block encryption.\n\n"

            "CLASSICAL CIPHERS INCLUDED\n"
            "• Caesar Cipher\n"
            "• ROT13\n"
            "• Atbash\n"
            "• Rail Fence\n\n"

            "SECURITY NOTE\n"
            "ECB is included for educational demonstration only. "
            "It is not recommended for real-world secure communication "
            "because ECB leaks patterns and does not provide "
            "authentication or integrity protection.\n\n"

            "For real applications, authenticated AES-GCM "
            "is generally preferred."
        )

        tk.Label(
            body,
            text=information,
            bg=BLACK,
            fg=TEXT,
            justify="left",
            anchor="w",
            padx=12,
            pady=12,
            font=(
                "Consolas",
                10
            )
        ).pack(
            fill="x"
        )

        self.label(
            body,
            "Python  •  Tkinter  •  PyCryptodome",
            bold=True,
            color=GRASS_LIGHT
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

    # ========================================================
    # KEY FUNCTIONS
    # ========================================================

    def get_key(self):

        return text_to_key(
            self.key_var.get()
        )

    def generate_new_key(self):

        self.key = generate_key()

        self.key_var.set(
            key_to_text(
                self.key
            )
        )

        self.set_status(
            "STATUS: NEW AES-256 KEY GENERATED",
            True
        )

    def copy_key(self):

        try:

            self.root.clipboard_clear()

            self.root.clipboard_append(
                self.key_var.get()
            )

            self.root.update()

            self.set_status(
                "STATUS: KEY COPIED",
                True
            )

        except Exception as e:

            messagebox.showerror(
                "Clipboard Error",
                str(e)
            )

    # ========================================================
    # TEXT ENCRYPTION
    # ========================================================

    def encrypt_text(self):

        try:

            key = self.get_key()

            text = self.crypto_text.get(
                "1.0",
                "end-1c"
            )

            if not text:

                messagebox.showwarning(
                    "No Input",
                    "Enter plaintext first."
                )

                return

            ciphertext = encrypt_text(
                text,
                key
            )

            self.crypto_text.delete(
                "1.0",
                "end"
            )

            self.crypto_text.insert(
                "1.0",
                ciphertext
            )

            self.set_status(
                "STATUS: TEXT ENCRYPTED SUCCESSFULLY",
                True
            )

        except Exception as e:

            messagebox.showerror(
                "Encryption Error",
                str(e)
            )

            self.set_status(
                "STATUS: ENCRYPTION FAILED",
                False
            )

    # ========================================================
    # TEXT DECRYPTION
    # ========================================================

    def decrypt_text(self):

        try:

            key = self.get_key()

            ciphertext = self.crypto_text.get(
                "1.0",
                "end-1c"
            ).strip()

            if not ciphertext:

                messagebox.showwarning(
                    "No Input",
                    "Enter Base64 ciphertext first."
                )

                return

            plaintext = decrypt_text(
                ciphertext,
                key
            )

            self.crypto_text.delete(
                "1.0",
                "end"
            )

            self.crypto_text.insert(
                "1.0",
                plaintext
            )

            self.set_status(
                "STATUS: TEXT DECRYPTED SUCCESSFULLY",
                True
            )

        except Exception as e:

            messagebox.showerror(
                "Decryption Error",
                str(e)
            )

            self.set_status(
                "STATUS: DECRYPTION FAILED",
                False
            )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_text(self):

        self.crypto_text.delete(
            "1.0",
            "end"
        )

        self.set_status(
            "STATUS: TEXT AREA CLEARED",
            True
        )

    # ========================================================
    # FILE ENCRYPTION
    # ========================================================

    def encrypt_file(self):

        try:

            key = self.get_key()

            source = filedialog.askopenfilename(
                title="Select file to encrypt"
            )

            if not source:
                return

            with open(
                source,
                "rb"
            ) as file:

                data = file.read()

            encrypted = encrypt_bytes(
                data,
                key
            )

            destination = filedialog.asksaveasfilename(
                title="Save encrypted file",
                initialfile=(
                    os.path.basename(source)
                    + ".enc"
                )
            )

            if not destination:
                return

            with open(
                destination,
                "wb"
            ) as file:

                file.write(
                    encrypted
                )

            self.set_status(
                "STATUS: FILE ENCRYPTED SUCCESSFULLY",
                True
            )

            messagebox.showinfo(
                "Success",
                "File encrypted successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "File Encryption Error",
                str(e)
            )

    # ========================================================
    # FILE DECRYPTION
    # ========================================================

    def decrypt_file(self):

        try:

            key = self.get_key()

            source = filedialog.askopenfilename(
                title="Select encrypted file"
            )

            if not source:
                return

            with open(
                source,
                "rb"
            ) as file:

                encrypted = file.read()

            decrypted = decrypt_bytes(
                encrypted,
                key
            )

            filename = os.path.basename(
                source
            )

            if filename.endswith(".enc"):

                filename = filename[:-4]

            destination = filedialog.asksaveasfilename(
                title="Save decrypted file",
                initialfile=filename
            )

            if not destination:
                return

            with open(
                destination,
                "wb"
            ) as file:

                file.write(
                    decrypted
                )

            self.set_status(
                "STATUS: FILE DECRYPTED SUCCESSFULLY",
                True
            )

            messagebox.showinfo(
                "Success",
                "File decrypted successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "File Decryption Error",
                str(e)
            )

    # ========================================================
    # STATUS
    # ========================================================

    def set_status(
        self,
        text,
        success=True
    ):

        self.status_var.set(
            text
        )

        self.status_label.configure(
            fg=(
                GRASS_LIGHT
                if success
                else "#ff776b"
            )
        )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    CryptoApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()