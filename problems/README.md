# Problems Directory

SQL 쿼리 최적화 문제를 개별적으로 실행할 수 있는 스크립트 모음입니다.

## 특징

- ✅ **독립 실행 가능**: 각 파일이 단독으로 실행됩니다
- ✅ **Portable**: 데이터베이스만 있으면 어디서든 실행 가능
- ✅ **비교 분석**: 비효율적 쿼리와 최적화 쿼리를 직접 비교
- ✅ **학습 포인트**: 각 문제별 상세한 설명과 힌트 포함
- ✅ **성능 측정**: 쿼리 실행 시간을 ms 단위로 측정

## 실행 방법

### 개별 실행

```bash
# 프로젝트 루트에서
uv run python problems/problem_1_duplicate_joins.py

# 또는 problems 디렉토리에서
cd problems
uv run python problem_1_duplicate_joins.py
```

### 모든 문제 순서대로 실행

```bash
cd problems
for f in problem_*.py; do
    echo "Running $f..."
    uv run python $f
    echo "Press Enter to continue..."
    read
done
```

## 문제 목록

### Problem 1: 불필요한 JOIN과 중복 서브쿼리 제거
**파일**: `problem_1_duplicate_joins.py`

**난이도**: ⭐⭐⭐

**학습 목표**:
- CTE(Common Table Expression) 활용
- 중복 JOIN 제거
- 필요한 컬럼만 SELECT
- LEFT JOIN vs INNER JOIN 올바른 선택

**주요 문제점**:
- 같은 테이블(customers, regions)을 여러 번 JOIN
- 중복된 서브쿼리 반복 실행
- SELECT *로 불필요한 컬럼 조회

### Problem 2: 비효율적인 GROUP BY 최적화
**파일**: `problem_2_inefficient_groupby.py`

**난이도**: ⭐⭐⭐⭐

**학습 목표**:
- 불필요한 테이블 JOIN 제거
- 서브쿼리 대신 집계 함수 활용
- COUNT DISTINCT 사용
- GROUP BY 성능 최적화

**주요 문제점**:
- 결과에 사용되지 않는 테이블까지 JOIN
- 각 행마다 서브쿼리 반복 실행
- LEFT JOIN의 잘못된 사용

### Problem 3: 복잡한 중첩 서브쿼리
**파일**: `problem_3_nested_subqueries.py`

**난이도**: ⭐⭐⭐⭐⭐

**학습 목표**:
- 중첩 서브쿼리를 CTE로 변환
- 서브쿼리를 JOIN으로 변환
- 한 번의 집계로 모든 통계 계산
- 불필요한 DISTINCT 제거

**주요 문제점**:
- 깊이 중첩된 서브쿼리
- 각 제품마다 여러 번 서브쿼리 실행
- SELECT 절에 스칼라 서브쿼리 과다 사용

### Problem 4: 인덱스 생성으로 성능 최적화
**파일**: `problem_4_create_indexes.py`

**난이도**: ⭐⭐

**학습 목표**:
- 적절한 인덱스 설계
- 인덱스 생성 및 확인
- EXPLAIN QUERY PLAN으로 인덱스 사용 확인
- 인덱스의 효과 측정

**생성 인덱스**:
- `orders(customer_id)`: 고객별 주문 조회
- `orders(order_status)`: 주문 상태별 필터링
- `orders(order_date)`: 날짜 범위 검색
- `order_items(order_id)`: 주문 상세 조인
- `order_items(product_id)`: 제품별 판매 분석
- `customers(region_id)`: 지역별 고객 조회
- `products(category_id)`: 카테고리별 제품 조회
- `customers(customer_tier)`: 등급별 고객 조회

### Problem 5: 잘못된 OUTER JOIN 사용
**파일**: `problem_5_outer_join.py`

**난이도**: ⭐⭐⭐

**학습 목표**:
- LEFT JOIN vs INNER JOIN 차이 이해
- WHERE 절이 OUTER JOIN을 무효화하는 경우
- 적절한 JOIN 타입 선택
- 성능 차이 분석

**주요 문제점**:
- WHERE 절에서 필터링하는 테이블에 LEFT JOIN 사용
- OUTER JOIN의 의미가 WHERE 절에 의해 무효화됨
- 불필요한 NULL 체크 오버헤드

## 공통 출력 형식

각 스크립트는 다음 정보를 출력합니다:

1. **문제 헤더**: 문제 제목과 설명
2. **비효율적 쿼리**:
   - SQL 쿼리
   - EXPLAIN QUERY PLAN
   - 실행 시간 (ms)
   - 결과 행 수
   - 샘플 데이터

3. **최적화된 쿼리**:
   - SQL 쿼리
   - EXPLAIN QUERY PLAN
   - 실행 시간 (ms)
   - 결과 행 수
   - 샘플 데이터

4. **학습 포인트**: 주요 최적화 기법 설명

## 권장 학습 순서

1. **먼저 비효율적 쿼리 분석**
   - 어떤 부분이 비효율적인지 파악
   - EXPLAIN QUERY PLAN 결과 해석

2. **스스로 최적화 시도**
   - 학습 포인트를 참고하여 직접 쿼리 작성
   - chatbot에서 채점 받기

3. **최적화된 쿼리 확인**
   - 제공된 최적화 쿼리와 비교
   - 성능 차이 분석

4. **실행 계획 비교**
   - EXPLAIN QUERY PLAN 결과 비교
   - 인덱스 사용 여부 확인

## 의존성

이 스크립트들은 `utils/sql_utils.py`에 의존합니다:

```python
from utils.sql_utils import (
    get_connection,
    execute_and_analyze,
    print_header,
    wait_for_input
)
```

## 문제 해결

### Import 오류

```bash
# 프로젝트 루트에서 실행해야 합니다
cd /path/to/sql101
uv run python problems/problem_1_duplicate_joins.py
```

### 데이터베이스 파일 없음

```bash
# 먼저 데이터베이스 생성
uv run python data/setup_database.py
```

## 추가 학습 자료

더 대화형 학습을 원한다면 **Gradio 챗봇**을 사용하세요:

```bash
uv run python chatbot/app.py
```

챗봇에서는:
- 실시간 채점 및 피드백
- 성능 점수 (100점 만점)
- 상세한 개선 팁
- 정답 및 해설 제공
