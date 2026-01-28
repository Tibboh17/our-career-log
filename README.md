# Our Career Log

팀의 프로젝트와 기술 블로그를 관리/공유하는 Django 웹앱입니다.

## 주요 기능
- 프로젝트 목록/상세/관리(작성·수정·삭제)
- 기술 블로그 목록/상세/관리(작성·수정·삭제)
- 마크다운 기반 글 작성 + 이미지 업로드(Toast UI Editor)
- 공개/비공개 설정
- 썸네일 업로드
- 슬러그(URL 커스텀) 지원

## 기술 스택
- Python 3.12
- Django 6.0.1
- SQLite(로컬 기본), 배포 시 외부 DB로 변경 가능
- Toast UI Editor (CDN)

## 설치된 패키지
`requirements.txt` 기준
- Django==6.0.1
- Markdown==3.10.1
- bleach==6.3.0
- pillow==12.1.0
- asgiref==3.11.0
- sqlparse==0.5.5
- tzdata==2025.3
- webencodings==0.5.1

## 폴더 구조 요약
```
config/           # 프로젝트 설정
portal/           # 메인 앱 (프로젝트/블로그)
  templates/
    portal/
      index.html
      project_list.html
      detail.html
      project_manage.html
      project_form.html
      project_delete.html
      blog_list.html
      blog_detail.html
      blog_manage.html
      blog_form.html
      blog_delete.html
db.sqlite3        # 로컬 DB (깃에 올리지 않음)
manage.py
requirements.txt
```

## 로컬 실행 방법 (Windows PowerShell 기준)
```powershell
# 1) 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2) 패키지 설치
pip install -r requirements.txt

# 3) 마이그레이션
python manage.py migrate

# 4) 관리자 계정 생성
python manage.py createsuperuser

# 5) 서버 실행
python manage.py runserver
```

접속:
- 메인: http://127.0.0.1:8000/
- 프로젝트 목록: http://127.0.0.1:8000/projects/
- 블로그 목록: http://127.0.0.1:8000/blog/
- 관리자: http://127.0.0.1:8000/admin/

## 글/프로젝트 작성 방법
- **관리 페이지**에서 작성/수정/삭제 가능
  - 프로젝트 관리: `/projects/manage/`
  - 블로그 관리: `/blog/manage/`
- 작성 폼에서:
  - 제목/요약/썸네일/공개 여부 입력
  - 본문은 **마크다운**으로 작성
  - 이미지 버튼으로 업로드하면 마크다운에 자동 삽입

## 슬러그(URL 커스텀)
- 프로젝트/블로그 모두 `slug`를 직접 입력 가능
- 입력하지 않으면 제목 기반으로 자동 생성
- URL 예시: `/projects/gofooda/`, `/blog/my-first-post/`

## 주의 사항
- `db.sqlite3`, `media/`는 깃에 올리지 않음
- 배포 시 외부 DB 연결 필요 (예: PostgreSQL)

## 환경 변수 (배포 시)
배포 시에는 다음 환경변수를 사용하는 구성이 일반적입니다.
- `SECRET_KEY`
- `DEBUG` (보통 False)
- `DATABASE_URL` (PostgreSQL 등)