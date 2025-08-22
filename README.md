# ArichImedes by Team CollabAI

경희대학교 자유전공학부 전용 AI 학사 도우미 🎓. OpenAI API와 RAG(LangChain+FAISS)를 활용해 학사제도·교육과정 QnA를 빠르게 제공합니다. GUI 기반으로 질문·답변, 이메일 전송, 실시간 달력 기능까지 지원하는 학생 맞춤형 도우미 프로젝트.
(2025 경희대학교 AI•SW 융합 프로젝트/페스티벌)
# 샘플 동영상(클릭!)
[![Watch the video](https://img.youtube.com/vi/PPrhjXUHsB0/0.jpg)](https://www.youtube.com/watch?v=PPrhjXUHsB0)

# 샘플 화면
![샘플 화면](https://github.com/robot7171-a11y/ArichImedes-by-Team_CollabAI/blob/main/sample.png?raw=true)

![샘플 화면](https://github.com/robot7171-a11y/ArichImedes-by-Team_CollabAI/blob/main/sample2.png?raw=true)

![샘플 화면](https://github.com/robot7171-a11y/ArichImedes-by-Team_CollabAI/blob/main/sample3.png?raw=true)

# 소개 PPT(클릭!)
[![프로젝트 소개 PPT](https://github.com/qpntux/ArchImedes/blob/main/intro.png)](https://www.miricanvas.com/v/14zxu3h)
# 파이선 패키지 설치(필수)
pip install --upgrade openai numpy faiss-cpu pymupdf beautifulsoup4 pillow customtkinter python-docx requests

# 파일 위치(필수)

```
project_root/
├── CollabAI_finally.py      # 메인 실행 파일
├── sidebar_calendar.py      # (필수) 캘린더 모듈
├── khulogo1.png             # (옵션) 로고 이미지
├── 2025 학사제도 안내-1.pdf   # (옵션) 샘플 PDF
├── QnA.txt                  # (옵션) 텍스트 데이터
├── .env                     # (필수) 환경변수 파일 (GitHub에는 업로드 X)
└── assets/                  # (옵션) 사이드바 아이콘 모음

```
# 환경변수 설정
.env.example 참고
