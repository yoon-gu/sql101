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
- 의존성 설치 (이 프로젝트는 Python 내장 라이브러리만 사용)

### 2. 샘플 데이터베이스 생성

먼저 실습용 전자상거래 데이터베이스를 생성합니다:

```bash
# 방법 1: uv run 사용 (권장)
uv run python setup_database.py

# 방법 2: 가상환경 활성화 후 실행
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python setup_database.py
```

생성되는 데이터:
- 지역: 6개 (한국, 일본, 중국)
- 고객: 1,000명
- 제품: 500개
- 주문: 5,000건
- 주문 상세: 약 15,000건

### 3. 최적화 튜토리얼 실행

```bash
# 방법 1: uv run 사용 (권장)
uv run python sql_optimization_tutorial.py

# 방법 2: 가상환경 활성화 후 실행
python sql_optimization_tutorial.py
```

## 실습 구성

### Problem 1: 불필요한 JOIN과 중복 서브쿼리

**비효율적인 쿼리 예시:**
- 같은 테이블(`customers`, `regions`)을 두 번씩 JOIN
- 동일한 서브쿼리를 여러 번 실행
- `SELECT *`로 모든 컬럼 조회

**최적화 방법:**
- 중복 JOIN 제거
- CTE(Common Table Expression)로 서브쿼리 재사용
- 필요한 컬럼만 명시적으로 SELECT

### Problem 2: 비효율적인 GROUP BY와 다중 LEFT JOIN

**비효율적인 쿼리 예시:**
- 불필요한 LEFT JOIN 사용 (실제로는 INNER JOIN이 적합)
- 각 고객별로 서브쿼리를 반복 실행하여 통계 계산
- 필요 없는 테이블까지 JOIN

**최적화 방법:**
- LEFT JOIN을 INNER JOIN으로 변경
- 서브쿼리 대신 GROUP BY의 집계 함수 활용
- 불필요한 JOIN 제거

### Problem 3: 복잡한 중첩 서브쿼리

**비효율적인 쿼리 예시:**
- 깊이 중첩된 서브쿼리
- 각 제품마다 여러 번 서브쿼리 실행
- 불필요한 DISTINCT 연산

**최적화 방법:**
- CTE로 서브쿼리를 하나의 집계로 통합
- 서브쿼리를 JOIN으로 변환
- 한 번의 GROUP BY로 모든 통계 계산

### Problem 4: 인덱스 최적화

**생성할 인덱스:**
- `orders(customer_id)`: 고객별 주문 조회
- `orders(order_status)`: 주문 상태별 필터링
- `orders(order_date)`: 날짜 범위 검색
- `order_items(order_id)`: 주문 상세 조인
- `order_items(product_id)`: 제품별 판매 분석
- `customers(region_id)`: 지역별 고객 조회
- `products(category_id)`: 카테고리별 제품 조회

### Problem 5: 잘못된 OUTER JOIN 사용

**비효율적인 쿼리 예시:**
- WHERE 절에서 필터링하는 테이블에 LEFT JOIN 사용
- OUTER JOIN의 의미가 WHERE 절에 의해 무효화됨

**최적화 방법:**
- WHERE 절 조건이 있는 테이블은 INNER JOIN 사용
- NULL 허용이 필요한 경우만 LEFT JOIN 사용

## 학습 목표

이 튜토리얼을 완료하면 다음을 할 수 있습니다:

1. ✅ **쿼리 실행 계획 분석**: `EXPLAIN QUERY PLAN` 해석
2. ✅ **JOIN 최적화**: INNER/LEFT/RIGHT JOIN의 올바른 선택
3. ✅ **서브쿼리 최적화**: CTE와 JOIN을 활용한 리팩토링
4. ✅ **인덱스 전략**: 적절한 인덱스 설계 및 적용
5. ✅ **집계 최적화**: GROUP BY와 윈도우 함수의 효율적 사용
6. ✅ **성능 측정**: 쿼리 실행 시간 비교 및 분석

## 파일 구조

```
sql101/
├── README.md                      # 이 파일
├── pyproject.toml                 # uv 프로젝트 설정
├── .python-version                # Python 버전 (3.11)
├── requirements.txt               # 의존성 목록 (레거시)
├── setup_database.py              # 샘플 DB 생성 스크립트
├── sql_optimization_tutorial.py   # 메인 튜토리얼
├── .venv/                         # 가상환경 (uv sync 후 생성)
└── ecommerce.db                   # 생성된 SQLite 데이터베이스
```

## 추가 학습 자료

### 권장 실습 순서

1. 먼저 비효율적인 쿼리를 실행하고 실행 시간 확인
2. `EXPLAIN QUERY PLAN` 결과 분석
3. 최적화된 쿼리와 비교
4. 인덱스 생성 전후 성능 차이 확인

### 직접 해보기

튜토리얼의 각 문제를 보고 최적화 방법을 스스로 생각해본 후, 제공된 해답과 비교해보세요.

## 실행 결과 예시

```
🔍 ❌ 비효율적 쿼리 - 중복 JOIN & 중복 서브쿼리
================================================================================

📝 SQL Query:
SELECT * FROM orders o
LEFT JOIN customers c1 ON o.customer_id = c1.customer_id
LEFT JOIN customers c2 ON o.customer_id = c2.customer_id
...

📊 Query Plan:
  SCAN o
  SEARCH c1 USING INDEX ...
  SEARCH c2 USING INDEX ...

⏱️  실행 시간: 245.32ms
✅ 결과: 150개 행

---

🔍 ✅ 최적화된 쿼리 - 중복 제거 & CTE 사용
================================================================================

⏱️  실행 시간: 12.45ms  👈 20배 빠름!
✅ 결과: 150개 행
```

## 기술 스택

- Python 3.8+ (권장: 3.11)
- SQLite3 (Python 내장)
- uv (의존성 관리 및 Python 버전 관리)

## 참고 사항

- 실습용으로 SQLite를 사용하지만, 개념은 MySQL, PostgreSQL 등에도 동일하게 적용됩니다
- 실제 프로덕션 환경에서는 데이터베이스 종류에 따라 최적화 방법이 다를 수 있습니다
- 쿼리 최적화는 데이터 규모와 분포에 따라 결과가 달라질 수 있습니다

## 라이선스

이 프로젝트는 학습 목적으로 자유롭게 사용할 수 있습니다.
