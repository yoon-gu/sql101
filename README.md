# SQL Query Optimization Hands-on Tutorial

복잡하고 비효율적인 SQL 쿼리를 분석하고 최적화하는 실습 프로젝트입니다.

## 프로젝트 개요

실무에서 자주 발생하는 비효율적인 SQL 쿼리 패턴들을 직접 실행해보고, 단계별로 최적화하는 과정을 학습합니다.

### 다루는 주요 문제점

1. **불필요한 JOIN 연산**: 같은 테이블을 여러 번 조인하는 문제
2. **중복 서브쿼리**: 동일한 계산을 반복 수행
3. **SELECT * 남용**: 필요 없는 컬럼까지 조회
4. **인덱스 미사용**: 대용량 데이터에서 성능 저하
5. **GROUP BY와 JOIN의 비효율적 조합**: 데이터 중복 집계
6. **OUTER JOIN의 잘못된 사용**: LEFT JOIN이 필요 없는 상황에서 사용

## 🆕 대화형 학습 챗봇

Gradio 기반 대화형 SQL 쿼리 최적화 챗봇을 사용하여 실시간 피드백을 받으며 학습할 수 있습니다!

```bash
# Gradio 챗봇 실행
uv run python chatbot/app.py

# 브라우저에서 http://localhost:7860 접속
```

**챗봇 기능:**
- 📝 문제 출제 및 과제 제공
- ✅ 제출한 쿼리 자동 채점
- 📊 성능 분석 및 비교
- 💡 실시간 피드백 및 개선 팁
- 🎯 정답 및 해설 제공

👉 자세한 사용법은 [chatbot/README.md](chatbot/README.md)를 참고하세요!

---

## 설치 및 실행

### 0. 사전 준비

[uv](https://docs.astral.sh/uv/)가 설치되어 있어야 합니다:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 또는 pip로 설치
pip install uv
```

### 1. 프로젝트 설정

```bash
# 프로젝트 디렉토리로 이동
cd sql101

# uv로 Python 환경 자동 설정 및 동기화
uv sync
```

`uv sync` 명령은:
- `.python-version` 파일에 지정된 Python 3.11을 자동으로 다운로드/설치
- 가상환경 자동 생성 (`.venv`)
- 의존성 설치 (Gradio)

### 2. 샘플 데이터베이스 생성

먼저 실습용 전자상거래 데이터베이스를 생성합니다:

```bash
uv run python data/setup_database.py
```

생성되는 데이터:
- 지역: 6개 (한국, 일본, 중국)
- 고객: 1,000명
- 제품: 500개
- 주문: 5,000건
- 주문 상세: 약 15,000건

👉 데이터베이스 스키마 상세 정보는 [data/README.md](data/README.md)를 참고하세요!

### 3. 학습 방법 선택

#### 방법 1: 대화형 챗봇 (권장) 🤖

```bash
uv run python chatbot/app.py
# http://localhost:7860 접속
```

- 실시간 채점 및 피드백
- 성능 점수 (100점 만점)
- 단계별 힌트 제공

#### 방법 2: 독립 스크립트 실행 📝

```bash
# Problem 1: 불필요한 JOIN과 중복 서브쿼리
uv run python problems/problem_1_duplicate_joins.py

# Problem 2: 비효율적인 GROUP BY
uv run python problems/problem_2_inefficient_groupby.py

# Problem 3: 중첩 서브쿼리
uv run python problems/problem_3_nested_subqueries.py

# Problem 4: 인덱스 생성
uv run python problems/problem_4_create_indexes.py

# Problem 5: 잘못된 OUTER JOIN
uv run python problems/problem_5_outer_join.py
```

👉 Problem 스크립트 상세 정보는 [problems/README.md](problems/README.md)를 참고하세요!

## 📁 프로젝트 구조

```
sql101/
├── README.md                          # 이 파일
├── pyproject.toml                     # uv 프로젝트 설정
├── .python-version                    # Python 버전 (3.11)
│
├── data/                              # 📁 데이터베이스
│   ├── README.md                      # DB 스키마 및 생성 가이드
│   ├── setup_database.py              # DB 생성 스크립트
│   └── ecommerce.db                   # SQLite 데이터베이스
│
├── problems/                          # 📁 독립 실행 가능한 Problem 스크립트
│   ├── README.md                      # Problem 사용 가이드
│   ├── problem_1_duplicate_joins.py   # Problem 1
│   ├── problem_2_inefficient_groupby.py
│   ├── problem_3_nested_subqueries.py
│   ├── problem_4_create_indexes.py
│   └── problem_5_outer_join.py
│
├── chatbot/                           # 📁 Gradio 챗봇
│   ├── README.md                      # 챗봇 상세 가이드
│   ├── DEMO.md                        # 사용 예시
│   ├── app.py                         # Gradio UI
│   └── sql_grader_agent.py            # 채점 엔진
│
└── utils/                             # 📁 공통 유틸리티
    ├── README.md                      # 유틸리티 함수 문서
    └── sql_utils.py                   # 공통 함수
```

### 디렉토리별 설명

각 디렉토리는 독립적인 README.md를 포함하고 있습니다:

- **[data/](data/)**: 데이터베이스 생성 및 스키마 정보
- **[problems/](problems/)**: 개별 실행 가능한 최적화 문제
- **[chatbot/](chatbot/)**: 대화형 학습 챗봇 애플리케이션
- **[utils/](utils/)**: 공통 유틸리티 함수 모음

## 실습 구성

### Problem 1: 불필요한 JOIN과 중복 서브쿼리
**학습 목표:**
- CTE(WITH 절) 활용
- 중복 JOIN 제거
- 필요한 컬럼만 SELECT

**난이도:** ⭐⭐⭐

### Problem 2: 비효율적인 GROUP BY
**학습 목표:**
- 불필요한 테이블 JOIN 제거
- 서브쿼리 대신 집계 함수 활용
- COUNT DISTINCT 사용

**난이도:** ⭐⭐⭐⭐

### Problem 3: 복잡한 중첩 서브쿼리
**학습 목표:**
- 중첩 서브쿼리를 CTE로 변환
- 서브쿼리를 JOIN으로 변환
- 한 번의 집계로 모든 통계 계산

**난이도:** ⭐⭐⭐⭐⭐

### Problem 4: 인덱스 최적화
**학습 목표:**
- 적절한 인덱스 설계
- 인덱스 생성 및 확인
- 성능 개선 효과 측정

**난이도:** ⭐⭐

### Problem 5: 잘못된 OUTER JOIN
**학습 목표:**
- LEFT JOIN vs INNER JOIN 차이
- WHERE 절이 OUTER JOIN을 무효화하는 경우
- 적절한 JOIN 타입 선택

**난이도:** ⭐⭐⭐

## 학습 목표

이 튜토리얼을 완료하면 다음을 할 수 있습니다:

1. ✅ **쿼리 실행 계획 분석**: `EXPLAIN QUERY PLAN` 해석
2. ✅ **JOIN 최적화**: INNER/LEFT/RIGHT JOIN의 올바른 선택
3. ✅ **서브쿼리 최적화**: CTE와 JOIN을 활용한 리팩토링
4. ✅ **인덱스 전략**: 적절한 인덱스 설계 및 적용
5. ✅ **집계 최적화**: GROUP BY와 윈도우 함수의 효율적 사용
6. ✅ **성능 측정**: 쿼리 실행 시간 비교 및 분석

## 권장 학습 순서

1. 먼저 비효율적인 쿼리를 실행하고 실행 시간 확인
2. `EXPLAIN QUERY PLAN` 결과 분석
3. 챗봇 또는 스크립트로 최적화 학습
4. 인덱스 생성 전후 성능 차이 확인

## 기술 스택

- **Python**: 3.8+ (권장: 3.11)
- **SQLite3**: Python 내장
- **Gradio**: 5.x (챗봇 UI)
- **uv**: 의존성 관리 및 Python 버전 관리

## 참고 사항

- 실습용으로 SQLite를 사용하지만, 개념은 MySQL, PostgreSQL 등에도 동일하게 적용됩니다
- 실제 프로덕션 환경에서는 데이터베이스 종류에 따라 최적화 방법이 다를 수 있습니다
- 쿼리 최적화는 데이터 규모와 분포에 따라 결과가 달라질 수 있습니다

## 문제 해결

### 데이터베이스 파일이 없는 경우

```bash
uv run python data/setup_database.py
```

### Import 오류

```bash
# 프로젝트 루트에서 실행해야 합니다
cd /path/to/sql101
uv run python problems/problem_1_duplicate_joins.py
```

### 포트 충돌 (챗봇)

`chatbot/app.py` 파일 수정:
```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7861,  # 다른 포트로 변경
    share=False
)
```

## 라이선스

이 프로젝트는 학습 목적으로 자유롭게 사용할 수 있습니다.
