# ArichImedes by Team_CollabAI

경희대학교 자유전공학부 전용 AI 학사 도우미 🎓. OpenAI API와 RAG(LangChain+FAISS)를 활용해 학사제도·교육과정 QnA를 빠르게 제공합니다. GUI 기반으로 질문·답변, 이메일 전송, 실시간 달력 기능까지 지원하는 학생 맞춤형 도우미 프로젝트.

# 파이선 패키지 설치(필수)
pip install --upgrade openai numpy faiss-cpu pymupdf beautifulsoup4 pillow customtkinter python-docx requests

#파일 위치(필수)
```
project_root/
├── CollabAI_finally.py      # 메인 실행 파일
├── sidebar_calendar.py      # (필수) 캘린더 모듈
├── khulogo1.png             # (옵션) 로고 이미지
├── 2025 학사제도 안내-1.pdf   # (옵션) 샘플 PDF
├── QnA.txt                  # (옵션) 텍스트 데이터
├── .env                     # (필수) 환경변수 파일 (GitHub에는 업로드 X)
└── assets/                  # (옵션) 사이드바 아이콘 모음
    ├── send.png
    ├── settings.png
    ├── new_chat.png
    ├── refresh.png
    ├── clear.png
    ├── attach.png
    └── history.png
```
# 환경변수 설정
.env.example 참고
