from __future__ import annotations
import os
# === 이메일 전송 설정 ===
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
# === 사이드 바 캘린더 ===
from sidebar_calendar import add_calendar_section
# ====================
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# ====================
api_key =os.getenv("OPENAI_API_KEY")
if not api_key :
    raise ValueError("환경변수 OPENAI_API_KEY가 로드되지 않았습니다!")
client = OpenAI(api_key=api_key)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")         # 발신 Gmail 주소 (앱 비밀번호 사용)
SMTP_PASS = os.getenv("SMTP_PASS")       # Gmail 앱 비밀번호
SENDER_NAME = "𝓐𝓻𝓬𝓱𝓲𝓶𝓮𝓭𝓮𝓼(경희대학교 자유전공학부 AI 도우미)"
SENDER_MAIL = SMTP_USER
# =======================

import sys
import math
import time
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
import re

# ---------------- 설치 ----------------
try:
    import customtkinter as ctk
except Exception as e:
    raise SystemExit("'customtkinter' (pip install customtkinter) 가 필요합니다.") from e

try:
    from PIL import Image
except Exception:
    Image = None  # icon images optional

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, messagebox

import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import faiss
import numpy as np
from email.header import decode_header
import imaplib
import email
import traceback

# === Email helpers (moved safely) ===

def is_valid_email(addr: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", addr.strip()))

def send_email(to_addr: str, subject: str, body: str) -> None:
    """Robust SMTP sender with TLS and basic validation + file logging."""
    import smtplib, ssl, os, datetime, traceback
    from email.mime.text import MIMEText
    from email.utils import formataddr

    if not (SMTP_USER and SMTP_PASS):
        raise RuntimeError("SMTP_USER/SMTP_PASS 미설정(앱 비밀번호 필요).")

    addr = to_addr.strip()
    if not is_valid_email(addr):
        raise ValueError(f"수신 이메일 형식 오류: {addr}")

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"]    = formataddr((SENDER_NAME, SENDER_MAIL))
    msg["To"]      = addr
    if "REPLY_TO" in globals() and REPLY_TO:
        msg["Reply-To"] = REPLY_TO

    log_path = os.path.join(os.path.dirname(__file__), "smtp_debug.log")
    def _log(line):
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {line}\n")
        except Exception:
            pass

    _log(f"=== SEND START to={addr} host={SMTP_HOST}:{SMTP_PORT} as={SMTP_USER}")
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=25) as server:
            server.set_debuglevel(1)  # 콘솔 디버그
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        _log("=== SEND OK")
    except Exception as e:
        tb = traceback.format_exc()
        _log(f"=== SEND FAIL: {e}\n{tb}")
        raise

try:
    import docx
except Exception:
    docx = None

try:
    from openai import OpenAI
except Exception as e:
    raise SystemExit("pip install openai 가 필요합니다.") from e

# ---------------- 모양 설정 ----------------
APP_TITLE = "𝓐𝓻𝓬𝓱𝓲𝓶𝓮𝓭𝓮𝓼"
WINDOW_MIN = (1100, 700)
SIDEBAR_WIDTH = 160
CONTENT_PAD = 16

# Optional PNG
ICON_PATHS = {
    "new": None,       # "assets/new_chat.png"
    "history": None,   # "assets/history.png"
    "refresh": None,   # "assets/refresh.png"
    "settings": None,  # "assets/settings.png"
    "send": None,      # "assets/send.png"
    "attach": None,    # "assets/attach.png"
    "clear": None,     # "assets/clear.png"
}

# 테마 설정
DEFAULT_APPEARANCE = "System"  
ctk.set_appearance_mode(DEFAULT_APPEARANCE)
ctk.set_default_color_theme("dark-blue")

# 전역 폰트
DEFAULT_FONT_SIZE = 13
DEFAULT_HEADER_SIZE = 14
MIN_FONT_SIZE = 10
MAX_FONT_SIZE = 22

# 폰트
FONT_SANS = None  

# Input expand 
INPUT_MIN_LINES = 1
INPUT_MAX_LINES = 10

# -------------- 중요 내용 및 개인정보 --------------


#client = OpenAI(api_key="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")

IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not EMAIL_USER or not EMAIL_PASS:
    raise ValueError("환경변수 EMAIL_USER/EMAIL_PASS가 설정되지 않았습니다!")
EMAIL_SENDER_FILTER = "hsk@khu.ac.kr"

WEBSITE_URL = "https://sls.khu.ac.kr"

# -------------- 파일 경로 --------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTACHMENTS_DIR = os.path.join(BASE_DIR, "attachments")
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

PDF_PATHS = [
    os.path.join(BASE_DIR, "2025 학사제도 안내-1.pdf"),
]

TEXT_PATHS = [
    os.path.join(BASE_DIR, "QnA.txt"),
]
LOGO_PATH = os.path.join(BASE_DIR, "assets", "khulogo1.png")  
LOGO_SIZE = (170, 100)  

# ---------------- 데이터 소스 도우미 ----------------
def get_website_text(url: str) -> str:
    if not url:
        return ""
    try:
        html = requests.get(url, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.extract()
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return f"[web fetch error] {e}"


def get_pdf_text(path: str) -> str:
    try:
        doc = fitz.open(path)
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"[pdf error] {os.path.basename(path)}: {e}"


def get_text_file_content(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"[txt read error] {os.path.basename(path)}: {e}"


def get_docx_text(path: str) -> str:
    if not docx:
        return ""
    try:
        d = docx.Document(path)
        return "\n".join(p.text for p in d.paragraphs)
    except Exception as e:
        return f"[docx error] {os.path.basename(path)}: {e}"


# ---------------- 이메일 ----------------
def get_emails_and_attachments(server, user, password, sender_filter):
    """Fetch plain-text bodies from a sender and save attachments safely."""
    if not (server and user and password):
        return "", []
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, password)
        mail.select("inbox")
        result, data = mail.search(None, f'(FROM "{sender_filter}")')
        email_texts, attachment_files = [], []
        for num in data[0].split():
            result, msg_data = mail.fetch(num, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    dispo = part.get("Content-Disposition")
                    if ctype == "text/plain" and not dispo:
                        email_texts.append(part.get_payload(decode=True).decode("utf-8", errors="ignore"))
                    if dispo and "attachment" in dispo:
                        fname = part.get_filename()
                        if fname:
                            decoded = decode_header(fname)
                            fname = ''.join([str(t[0], t[1] or 'utf-8') if isinstance(t[0], bytes) else str(t[0]) for t in decoded])
                            fname = re.sub(r'[<>:"/\|?*]', '_', fname)
                            path = os.path.join(ATTACHMENTS_DIR, fname)
                            with open(path, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            attachment_files.append(path)
            else:
                email_texts.append(msg.get_payload(decode=True).decode("utf-8", errors="ignore"))
        mail.logout()
        return " ".join(email_texts), attachment_files
    except Exception as e:
        return f"[email error] {e}", []


# ---------------- Embeddings / FAISS ----------------
def embed_texts(texts: List[str]) -> np.ndarray:
    if not texts:
        return np.array([])
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return np.array([it.embedding for it in resp.data])


def build_faiss_index(text_chunks: List[str]):
    if not text_chunks:
        return None
    vecs = embed_texts(text_chunks)
    dim = vecs.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vecs)
    return index


def search_context(query: str, text_chunks: List[str], index) -> str:
    if not (index and text_chunks):
        return ""
    q = embed_texts([query])
    D, I = index.search(q, k=5)
    return "\n".join(text_chunks[i] for i in I[0])


def ask_question(query: str, context: str, history: List[tuple]) -> str:
    system_prompt = (
        "You are a helpful multilingual assistant. Always prioritize the provided context when answering. "
        "Answer directly if the context supports it. If context is insufficient, explain what is missing "
        "but avoid fabricating facts. Use cautious reasoning only when context allows it. "
        "Stay professional, clear, and neutral."
    )
    messages = [{"role": "system", "content": system_prompt}]
    for user_msg, bot_msg, _ts in history[-8:]:  # keep last few turns
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": f"Context:{context}Question:{query}"})
    resp = client.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return resp.choices[0].message.content


# ---------------- 소스 로드 ----------------
def load_all_sources() -> List[str]:
    chunks: List[str] = []
    # Website
    site_text = get_website_text(WEBSITE_URL)
    if site_text:
        chunks.extend([site_text[i:i+800] for i in range(0, len(site_text), 800)])
    # Email + attachments
    email_text, attachments = get_emails_and_attachments(IMAP_SERVER, EMAIL_USER, EMAIL_PASS, EMAIL_SENDER_FILTER)
    if email_text:
        chunks.extend([email_text[i:i+800] for i in range(0, len(email_text), 800)])
    # Attachment contents
    for file_path in attachments:
        text = ""
        if file_path.lower().endswith(".pdf"):
            text = get_pdf_text(file_path)
        elif file_path.lower().endswith(".txt"):
            text = get_text_file_content(file_path)
        elif file_path.lower().endswith(".docx"):
            text = get_docx_text(file_path)
        if text:
            chunks.extend([text[i:i+800] for i in range(0, len(text), 800)])
    # Local PDFs
    for p in PDF_PATHS:
        if os.path.exists(p):
            t = get_pdf_text(p)
            chunks.extend([t[i:i+800] for i in range(0, len(t), 800)])
    # Local TXTs
    for p in TEXT_PATHS:
        if os.path.exists(p):
            t = get_text_file_content(p)
            chunks.extend([t[i:i+800] for i in range(0, len(t), 800)])
    return chunks


@dataclass
class ChatTurn:
    role: str  # user|assistant|system
    text: str
    ts: float


class ModernChatGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.history = []
        self.send_buffer = []
        self._last_question = ''
        self._last_answer = ''  # 대화 로그
        self.title(APP_TITLE)
        self.minsize(*WINDOW_MIN)
        self.geometry("1000x720")

        # fonts
        self.font_size = DEFAULT_FONT_SIZE
        self.font_header_size = DEFAULT_HEADER_SIZE
        self.font_base = ctk.CTkFont(size=self.font_size)
        self.font_small = ctk.CTkFont(size=max(MIN_FONT_SIZE, self.font_size-2))
        self.font_large = ctk.CTkFont(size=max(MIN_FONT_SIZE, self.font_size+2), weight="bold")
        self.font_header = ctk.CTkFont(size=self.font_header_size, weight="bold")

        self.history: List[tuple] = []  # (user, bot, ts)
        self._busy = False  

        # layout grid: sidebar | main
        self.grid_columnconfigure(0, weight=0, minsize=SIDEBAR_WIDTH)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self._build_sidebar()

        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=0)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=0)
        self.main.grid_columnconfigure(0, weight=1)

        self._build_topbar()
        self._build_chat_area()
        self._build_input_bar()

        # Busy during startup load
        self._set_busy(True, reason="데이터 불러오는 중… 잠시만 기다려주세요 ! (최대 1분...🥺)")
        threading.Thread(target=self._startup_load, daemon=True).start()

        # shortcuts: send & font control
        self.bind("<Control-Return>", lambda e: self._send_from_input())
        self.bind("<Control-equal>", lambda e: self._adjust_global_font(+1))  # Ctrl+=
        self.bind("<Control-plus>", lambda e: self._adjust_global_font(+1))
        self.bind("<Control-KP_Add>", lambda e: self._adjust_global_font(+1))
        self.bind("<Control-minus>", lambda e: self._adjust_global_font(-1))
        self.bind("<Control-KP_Subtract>", lambda e: self._adjust_global_font(-1))
        self.bind("<Control-0>", lambda e: self._reset_global_font())

    # ---------- 사이드바 ---------
    
    # === UI Color helpers ===
    def _text_color(self):
        try:
            import customtkinter as ctk
            return "#111111" if ctk.get_appearance_mode() == "Light" else "#EEEEEE"
        except Exception:
            return "#111111"

    def _muted_text_color(self):
        try:
            import customtkinter as ctk
            return "#6B7280" if ctk.get_appearance_mode() == "Light" else "#9CA3AF"
        except Exception:
            return "#6B7280"

    def _bg_color(self):
        try:
            import customtkinter as ctk
            return "#FFFFFF" if ctk.get_appearance_mode() == "Light" else "#111827"
        except Exception:
            return "#FFFFFF"

    def _accent_color(self):
        return "#3B82F6"
    # =========================
    def _build_sidebar(self):
            
            for i in range(6):
                self.sidebar.grid_rowconfigure(i, weight=0)
            self.sidebar.grid_rowconfigure(4, weight=1)  
    
            logo_container = ctk.CTkFrame(self.sidebar, corner_radius=0, fg_color="transparent", height=78)
            logo_container.grid(row=0, column=0, sticky="new", padx=6, pady=(8, 2))
            try:
                if Image and LOGO_PATH and os.path.exists(LOGO_PATH):
                    _img = Image.open(LOGO_PATH)
                    _img = _img.convert("RGBA")
                    ctk_img = ctk.CTkImage(light_image=_img, dark_image=_img, size=LOGO_SIZE)
                    self.logo_label = ctk.CTkLabel(logo_container, image=ctk_img, text="")
                    self.logo_label.image = ctk_img  # prevent GC
                    self.logo_label.pack(expand=True)
                else:
                    
                    self.logo_label = ctk.CTkLabel(logo_container, text="")
                    self.logo_label.pack(expand=True)
            except Exception:
                
                self.logo_label = ctk.CTkLabel(logo_container, text="")
                self.logo_label.pack(expand=True)
    
            self.btn_new = ctk.CTkButton(
                self.sidebar, text="＋새 채팅", width=SIDEBAR_WIDTH-12, height=54,
                text_color=self._text_color(),
                command=self.new_chat, font=self.font_large
            )
            self.btn_new.grid(row=1, column=0, padx=6, pady=6, sticky="new")
    
            self.btn_refresh = ctk.CTkButton(
                self.sidebar, text="🔁데이터 다시 불러오기", width=SIDEBAR_WIDTH-12, height=54,
                text_color=self._text_color(),
                command=self.refresh_sources, font=self.font_large
            )
            self.btn_refresh.grid(row=2, column=0, padx=6, pady=6, sticky="new")
    
            self.btn_clear = ctk.CTkButton(
                self.sidebar, text="🧹채팅 지우기", width=SIDEBAR_WIDTH-12, height=54,
                text_color=self._text_color(),
                command=self.clear_chat, font=self.font_large
            )
            self.btn_clear.grid(row=3, column=0, padx=6, pady=6, sticky="new")
            # ===== 이메일 전송 섹션 =====
            email_frame = ctk.CTkFrame(self.sidebar, corner_radius=6)
            email_frame.grid(row=4, column=0, padx=6, pady=(6, 6), sticky="new")
    
            ctk.CTkLabel(email_frame, text="이메일 전송", anchor="w",
                         font=self.font_small).pack(fill="x", padx=8, pady=(4,2))
    
            self.email_entry = ctk.CTkEntry(email_frame, placeholder_text="받는 이메일 주소", height=28)
            self.email_entry.pack(fill="x", padx=8, pady=(0,4))
    
            
            def _on_send_email_click():
                to_addr = self.email_entry.get().strip()
                if not to_addr:
                    messagebox.showwarning("알림", "수신 이메일을 입력하세요.")
                    return
                if not is_valid_email(to_addr):
                    messagebox.showwarning("알림", "올바른 수신 이메일을 입력하세요.")
                    return
    
                # 우선순위: send_buffer > 최근 문답
                if hasattr(self, "send_buffer") and self.send_buffer:
                    parts = []
                    for i, (q, a) in enumerate(self.send_buffer, 1):
                        parts.append(f"[Q{i}]\n{q}\n[A{i}]\n{a}")
                    body = "\n" + ("-"*40 + "\n").join(parts)
                else:
                    q = getattr(self, "_last_question", "").strip()
                    a = getattr(self, "_last_answer", "").strip()
                    if not (q and a):
                        messagebox.showwarning("알림", "보낼 ‘최근 문답’이 없습니다.")
                        return
                    body = f"[Q]\n{q}\n\n[A]\n{a}"
    
                try:
                    send_email(to_addr, "[𝓐𝓻𝓬𝓱𝓲𝓶𝓮𝓭𝓮𝓼] 질문 답변 전송", body)
                    messagebox.showinfo("성공", f"{to_addr}로 전송했습니다. (smtp_debug.log 확인 가능)")
                    if hasattr(self, "send_buffer"):
                        self.send_buffer.clear()
                except Exception as e:
                    messagebox.showerror("오류", f"이메일 전송 실패: {e}")
    
            ctk.CTkButton(
                email_frame, text="최근 답변 이메일로 보내기",
                command=_on_send_email_click
            ).pack(fill="x", padx=8, pady=(0,10))
    # ==========================

    # ==========================

            self._cal_section = add_calendar_section(self.sidebar)
     # --- 크레딧(하단) ---
            self.credit_label = ctk.CTkLabel(
            self.sidebar,
            text="© 2025 Team CollabAI \n - 경희대학교 자유전공학부 -",
            justify="center",
            anchor="center",
            font=self.font_small,
            )
            self.credit_label.grid(row=99, column=0, padx=6, pady=(12, 10), sticky="snew")

    
            #
            self.appearance_option = ctk.CTkOptionMenu(
                self.sidebar, values=["System","Light","Dark"],
                command=ctk.set_appearance_mode,
                width=SIDEBAR_WIDTH-12, height=34, anchor="center"
            )
            def _on_appearance_change(self, mode):
                ctk.set_appearance_mode(mode)
                self._apply_text_colors()
    
            self.appearance_option.set(DEFAULT_APPEARANCE)
            self.appearance_option.grid(row=16, column=0, padx=6, pady=8, sticky="sew")
    # ---------- 색상 ---------
    def _text_color(self):
        mode = ctk.get_appearance_mode().lower()
        return "white" if mode == "dark" else "black"
    def _apply_text_colors(self):
        try: self.title_label.configure(text_color=self._text_color())
        except: pass
        try: self.btn_new.configure(text_color=self._text_color())
        except: pass
        try: self.btn_refresh.configure(text_color=self._text_color())
        except: pass
        try: self.btn_clear.configure(text_color=self._text_color())
        except: pass
        try: self.btn_send.configure(text_color=self._text_color())
        except: pass

    # ---------- 상단 ---------
    # ---------- 상단 ----------
    def _build_topbar(self):
        import tkinter as tk

        # 상단 프레임 (둥근 모서리)
        self.topbar = ctk.CTkFrame(self.main, corner_radius=16, fg_color="#2b2b2b", height=48)
        self.title_label = ctk.CTkLabel(self.topbar, text=APP_TITLE, font=self.font_header)
        self.title_label.pack(side="left", padx=12, pady=8)

        # 채팅창 크기에 맞춰 상단바 동기화
        def sync_topbar(event=None):
            try:
                chat = self.chat_area   # 채팅창 Frame
                x = chat.winfo_x()
                w = chat.winfo_width()
                self.topbar.place(x=x, y=0, width=w, height=48)
            except Exception:
                pass

        self.main.bind("<Configure>", sync_topbar)
        self.after(100, sync_topbar)  # 초기 실행
    def _build_chat_area(self):
        self.chat_scroll = ctk.CTkScrollableFrame(self.main, corner_radius=12)
        self.chat_scroll.grid(row=1, column=0, sticky="nsew", padx=CONTENT_PAD, pady=(0, CONTENT_PAD))
        self.chat_scroll.grid_columnconfigure(0, weight=1)

    def _bubble_color(self, role: str):
        mode = ctk.get_appearance_mode().lower()
        if role == "user":
            return ("#e8f2ff", "#1e2633") if mode=="dark" else ("#e8f2ff", "#1e2633")
        if role == "assistant":
            return ("#f3f3f3", "#1f1f1f") if mode=="dark" else ("#f3f3f3", "#1f1f1f")
        return ("#fffbe6", "#2a2615")

    def _add_message(self, role: str, text: str):
        wrap_px = int(self.winfo_width() * 0.6)
        bubble = ctk.CTkFrame(self.chat_scroll, corner_radius=16, fg_color=self._bubble_color(role))
        anchor = "e" if role=="user" else "w"
        bubble.grid(sticky=anchor, padx=8, pady=6)
        lbl = ctk.CTkLabel(bubble, text=text, wraplength=wrap_px, justify="left", font=self.font_base)
        lbl.pack(padx=12, pady=10)
        self.after(30, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))
    def _add_user(self, text: str):
        # 최근 질문 추적 + 히스토리 기록
        self._last_question = text
        try:
            self.history.append((text, "", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except Exception:
            pass
        self._add_message("user", text)

    def _add_assistant(self, text: str):
        # 최근 답변 추적 + 히스토리 업데이트
        self._last_answer = text
        try:
            if self.history:
                q, _, t = self.history[-1]
                self.history[-1] = (q, text, t)
        except Exception:
            pass
        self._add_message("assistant", text)

    # ---------- 입력 칸 ---------
    def _build_input_bar(self):
        self.input_bar = ctk.CTkFrame(self.main, corner_radius=16)
        self.input_bar.grid(row=2, column=0, sticky="ew", padx=CONTENT_PAD, pady=(0, CONTENT_PAD))
        self.input_bar.grid_columnconfigure(0, weight=1)
        self.input_bar.grid_columnconfigure(1, weight=0)

        self.entry = ctk.CTkTextbox(self.input_bar, height=36, corner_radius=12)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(10,6), pady=10)
        self.entry.bind("<KeyRelease-Return>", self._auto_expand)
        self.entry.bind("<KeyRelease-BackSpace>", self._auto_expand)
        self.entry.bind("<KeyRelease-Delete>", self._auto_expand)
        self.entry.bind("<<Paste>>", self._auto_expand)
        self.entry.bind("<<Cut>>", self._auto_expand)
        self.entry.bind("<Return>", self._on_return)
        self.entry.bind("<Shift-Return>", lambda e: None)
        self._placeholder_text = "메시지를 입력하세요..."  
        self._placeholder = False
        self._apply_placeholder()

        self.entry.bind("<FocusIn>", self._placeholder_focus_in)
        self.entry.bind("<Button-1>", self._placeholder_click)   
        self.entry.bind("<Key>", self._placeholder_on_key)       
        self.entry.bind("<FocusOut>", self._restore_placeholder)

        
        self.btn_send = ctk.CTkButton(self.input_bar, text="⬆️", width=52, height=40,
                                      text_color=self._text_color(),
                                      command=self._send_from_input, font=self.font_small)
        self.btn_send.grid(row=0, column=1, padx=(6,10), pady=10)

    def _apply_placeholder(self):
        if self.entry.get("1.0", "end-1c").strip():
            return
        self.entry.delete("1.0", "end")
        self.entry.insert("1.0", self._placeholder_text)
        try:
            self.entry.tag_configure("_ph", foreground="#888888")
            self.entry.tag_add("_ph", "1.0", "end-1c")
        except Exception:
            pass
        self._placeholder = True

    def _clear_placeholder_now(self):
        if self._placeholder:
            self.entry.delete("1.0", "end")
            try:
                self.entry.tag_remove("_ph", "1.0", "end")
            except Exception:
                pass
            self._placeholder = False
    
    def _placeholder_focus_in(self, _evt=None):
        # remove immediately on focus
        self._clear_placeholder_now()

    def _placeholder_click(self, _evt=None):
        self._clear_placeholder_now()

    def _placeholder_on_key(self, _evt=None):
        self._clear_placeholder_now()

    def _restore_placeholder(self, _evt=None):
        # if user left it empty, restore watermark
        if not self.entry.get("1.0", "end-1c").strip():
            self._apply_placeholder()
            self._auto_expand()

    def _auto_expand(self, _=None):
        line_count = int(self.entry.index("end-1c").split(".")[0])  # 1-based
        line_count = max(1, min(10, line_count))
        self.entry.configure(height=18 * line_count + 12)

    def _on_return(self, event):
        if event.state & 0x0001:  # Shift
            return
        self._send_from_input()
        return "break"

    def _clear_placeholder(self, _):
        if self._placeholder:
            self.entry.delete("1.0", "end")
            self._placeholder = False


    # ---------- busy state & gating ---------
    def _set_busy(self, busy: bool, reason: Optional[str]=None):
        self._busy = busy
        state = "disabled" if busy else "normal"
        try:
            self.entry.configure(state=state)
            self.btn_send.configure(state=state)
            self.btn_new.configure(state=state)
            self.btn_refresh.configure(state=state)
            self.btn_clear.configure(state=state)
        except Exception:
            pass
        if reason:
            self._add_message("assistant", reason)

    # ---------- 기타 기능 ---------
    def new_chat(self):
        if self._busy:
            return
        self.clear_chat()
        self._add_assistant('''새 대화를 시작했습니다. 
        안녕하세요! 경희대학교 자유전공학부 AI 도우미 𝓐𝓻𝓬𝓱𝓲𝓶𝓮𝓭𝓮𝓼입니다. 🎓

이 챗봇은 「2025 학사제도 안내」와 학부 「FAQ」를 기반으로 답변합니다.  
더 정확한 답변을 받으시려면 아래와 같이 질문해 보세요:

- “자유전공학부 분반은 몇 개 있나요?”  
- “소속 변경은 언제 적용되나요?”  
- “희망 전공 기초 과목은 1학년 때 들을 수 있나요?”  
- “전공탐색2와 미래교육2의 차이는 무엇인가요?”  

⚠️ 주의:  
- 수강신청, 전공 선택, 교과과정 관련 답변은 **2025년도 기준**입니다.  
- 𝓐𝓻𝓬𝓱𝓲𝓶𝓮𝓭𝓮𝓼가 최대한 정확히 답하려고 노력하지만, 가끔 틀릴 수도 있어요. 
- 중요한 내용은 반드시 학부/학과 공지를 기준으로 해주세요.

궁금한 내용을 자유롭게 입력해 주세요!

* 개발/문의 :Team CollabAI *''')

    def clear_chat(self):
        for ch in list(self.chat_scroll.children.values()):
            ch.destroy()
        self.history.clear()

    # 새로고침 및 로드
    def _startup_load(self):
        try:
            self.text_chunks = load_all_sources()
            self.faiss_index = build_faiss_index(self.text_chunks)
            self.after(0, self._add_assistant, '''안녕하세요! 경희대학교 자유전공학부 AI  도우미 𝓐𝓻𝓬𝓱𝓲𝓶𝓮𝓭𝓮𝓼입니다. 🎓

이 챗봇은 「2025 학사제도 안내」와 「학부 FAQ」를 기반으로 답변합니다.  
더 정확한 답변을 받으시려면 아래와 같이 질문해 보세요:

- “자유전공학부 분반은 몇 개 있나요?”  
- “소속 변경은 언제 적용되나요?”  
- “희망 전공 기초 과목은 1학년 때 들을 수 있나요?”  
- “전공탐색2와 미래교육2의 차이는 무엇인가요?”  
- "자유전공학부 학생은 전공기초 과목을 언제 신청하나요?"

⚠️ 주의:  
- 수강신청, 전공 선택, 교과과정 관련 답변은 2025년도 기준입니다.  
- 𝓐𝓻𝓬𝓱𝓲𝓶𝓮𝓭𝓮𝓼가 최대한 정확히 답하려고 노력하지만, 가끔 틀릴 수도 있어요. 
- 중요한 내용은 반드시 학부/학과 공지를 기준으로 해주세요.


궁금한 내용을 자유롭게 입력해 주세요!

* 개발/문의 : Team CollabAI *''')
        except Exception as e:
            tb = traceback.format_exc()
            msg = f"[startup error] {e}\n{tb}"
            self.after(0, self._add_assistant, msg)
        finally:
            self.after(0, self._set_busy, False)

    def refresh_sources(self):
        if self._busy:
            return
        self._set_busy(True, reason="데이터 새로고침 중...")
        threading.Thread(target=self._do_refresh, daemon=True).start()

    def _do_refresh(self):
        try:
            self.text_chunks = load_all_sources()
            self.faiss_index = build_faiss_index(self.text_chunks)
            self.after(0, self._add_assistant, "데이터 새로고침 완료")
        except Exception as e:
            tb = traceback.format_exc()
            msg = f"새로고침 실패: {e}\n{tb}"
            self.after(0, self._add_assistant, msg)
        finally:
            self.after(0, self._set_busy, False)

    # 전송
    def _send_from_input(self):
        if self._busy:
            return
        text = self.entry.get("1.0", "end-1c").strip()
        if not text or self._placeholder:
            return
        self.entry.delete("1.0", "end"); self._auto_expand()
        self._add_user(text)
        self._set_busy(True, reason=None)
        threading.Thread(target=self._process_user_message, args=(text,), daemon=True).start()

    def _process_user_message(self, text: str):
        try:
            try:
                ctx = search_context(text, getattr(self, 'text_chunks', []), getattr(self, 'faiss_index', None))
            except Exception:
                ctx = ""
            try:
                ans = ask_question(text, ctx, self.history)
            except Exception as e:
                ans = f"(Error fetching answer: {e})"
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.history:
                last_u, _b, _ts = self.history[-1]
                if last_u == text:
                    self.history[-1] = (text, ans, ts)
                else:
                    self.history.append((text, ans, ts))
            else:
                self.history.append((text, ans, ts))
            self.after(0, lambda: self._add_assistant(ans))
        finally:
            self.after(0, self._set_busy, False)

    # ---------- 폰트 크기 조정 ---------
    def _apply_fonts_to_widgets(self):
        # Title
        try:
            self.title_label.configure(font=self.font_header)
        except Exception:
            pass
        
        for child in self.chat_scroll.winfo_children():
            for sub in child.winfo_children():
                if isinstance(sub, ctk.CTkLabel):
                    try:
                        sub.configure(font=self.font_base)
                    except Exception:
                        pass
        
        try:
            self.entry.configure(font=self.font_base)
            self.btn_send.configure(font=self.font_small)
            self.btn_new.configure(font=self.font_small)
            self.btn_refresh.configure(font=self.font_small)
            self.btn_clear.configure(font=self.font_small)
        except Exception:
            pass

    def _adjust_global_font(self, delta: int):
        new_base = max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, self.font_size + delta))
        if new_base == self.font_size:
            return
        self.font_size = new_base
        self.font_header_size = max(MIN_FONT_SIZE+1, min(MAX_FONT_SIZE+2, new_base+1))
        self.font_base = ctk.CTkFont(size=self.font_size)
        self.font_small = ctk.CTkFont(size=max(MIN_FONT_SIZE, self.font_size-2))
        self.font_header = ctk.CTkFont(size=self.font_header_size, weight="bold")
        self._apply_fonts_to_widgets()

    def _reset_global_font(self):
        self.font_size = DEFAULT_FONT_SIZE
        self.font_header_size = DEFAULT_HEADER_SIZE
        self.font_base = ctk.CTkFont(size=self.font_size)
        self.font_small = ctk.CTkFont(size=max(MIN_FONT_SIZE, self.font_size-2))
        self.font_header = ctk.CTkFont(size=self.font_header_size, weight="bold")
        self._apply_fonts_to_widgets()



        try:
            self.history.append(("user", text))
        except Exception:
            pass

        try:
            self.history.append(("assistant", text))
        except Exception:
            pass
def main():
    app = ModernChatGUI()
    app.mainloop()


if __name__ == "__main__":
    main()