# ArchImedes : 자유전공학부 AI 도우미 by Team CollabAI

2025년 자유전공학부가 신설되면서 학사제도, 교육과정, 전공 선택 등에 대한 궁금증이 많아졌습니다. 초창기에는 자유전공학부 학부장님(별명: Archimedes)께서 직접 Q&A를 통해 답변을 주셨고, 그 내용은 카톡 게시판에 계속 남아 있습니다. 하지만 필요한 정보를 찾으려면 매번 게시글을 일일이 뒤져야 하는 불편함이 있습니다.

저희는 “이 과정을 조금 더 편리하게 만들 수 없을까?”라는 생각에서 자유전공학부 AI 도우미 프로젝트를 시작했습니다. 학부에서 공유된 자료와 Q&A를 기반으로, 학생들이 AI를 통해 보다 쉽게 검색하고 대화 형식으로 활용할 수 있도록 구현했습니다.

OpenAI API + RAG 기법을 활용하여 「2025 학사제도 안내」, 학부 FAQ 자료를 기반으로 답변할 수 있는 챗봇을 PYTHON 기반으로 개발했습니다. LangChain, FAISS를 이용해 문서를 분할·임베딩하고 검색 인덱스를 구축했으며, Tkinter / CustomTkinter로 GUI를 구현해 직관적이고 친숙한 인터페이스를 만들었습니다.

해당 프로젝트는 다음과 같이 확장 & 활용 가능합니다.
1. 접근성 확장 : 학교 공식 홈페이지, 카카오톡 채널 또는 모바일 앱 버전 제작 -> 보편화 O
2. 데이터 확장 : 자유전공학부 뿐만 아니라 타 학과/학부의 데이터를 추가 -> 전공별 학사 도우미로 확장 O
3. 기능 확장 : 다국어 지원 가능 -> 유학생 활용 O
   
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

# 파일 체계(필수)

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
# 환경변수 설정(필수)
.env.example 참고
