# Data Directory

이 디렉토리는 SQL 쿼리 최적화 실습을 위한 샘플 데이터베이스를 포함합니다.

## 파일 목록

- `setup_database.py`: 샘플 데이터베이스 생성 스크립트
- `ecommerce.db`: 생성된 SQLite 데이터베이스 파일

## 데이터베이스 생성

```bash
# 프로젝트 루트에서 실행
uv run python data/setup_database.py

# 또는 data 디렉토리에서 실행
cd data
uv run python setup_database.py
```

## 데이터베이스 스키마

### 테이블 구조

#### 1. regions (지역)
- `region_id` (PK): 지역 ID
- `region_name`: 지역명 (Seoul, Busan, Tokyo, Osaka, Beijing, Shanghai)
- `country`: 국가 (South Korea, Japan, China)

**데이터:** 6개 지역

#### 2. customers (고객)
- `customer_id` (PK): 고객 ID
- `customer_name`: 고객명
- `email`: 이메일
- `region_id` (FK): 지역 ID
- `join_date`: 가입일
- `customer_tier`: 등급 (Bronze, Silver, Gold, Platinum)

**데이터:** 1,000명

#### 3. categories (카테고리)
- `category_id` (PK): 카테고리 ID
- `category_name`: 카테고리명 (Electronics, Books, Clothing, Food, Sports)
- `description`: 설명

**데이터:** 5개 카테고리

#### 4. products (제품)
- `product_id` (PK): 제품 ID
- `product_name`: 제품명
- `category_id` (FK): 카테고리 ID
- `price`: 가격
- `stock_quantity`: 재고 수량

**데이터:** 500개 제품

#### 5. orders (주문)
- `order_id` (PK): 주문 ID
- `customer_id` (FK): 고객 ID
- `order_date`: 주문일
- `order_status`: 주문 상태 (Pending, Processing, Shipped, Delivered, Cancelled)
- `total_amount`: 총 금액

**데이터:** 5,000건

#### 6. order_items (주문 상세)
- `order_item_id` (PK): 주문 상세 ID
- `order_id` (FK): 주문 ID
- `product_id` (FK): 제품 ID
- `quantity`: 수량
- `unit_price`: 단가
- `discount_rate`: 할인율

**데이터:** 약 15,000건 (주문당 평균 3개 상품)

## 데이터 통계

- **총 고객**: 1,000명
- **총 제품**: 500개
- **총 주문**: 5,000건
- **총 주문 상세**: ~15,000건
- **데이터베이스 크기**: 약 1.3MB

## 인덱스

데이터베이스 생성 시 기본적으로 Primary Key에만 인덱스가 생성됩니다.
성능 최적화를 위한 추가 인덱스는 `problems/problem_4_create_indexes.py`를 참고하세요.

## 주의사항

- `ecommerce.db` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다
- 데이터베이스를 재생성하려면 기존 `ecommerce.db` 파일을 삭제하고 `setup_database.py`를 다시 실행하세요
- 샘플 데이터는 무작위로 생성되므로 실행할 때마다 다른 데이터가 생성됩니다

## 사용 예시

### Python에서 데이터베이스 연결

```python
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

# 쿼리 실행
cursor.execute("SELECT COUNT(*) FROM customers")
print(f"총 고객 수: {cursor.fetchone()[0]}")

conn.close()
```

### SQLite CLI로 탐색

```bash
# SQLite CLI 실행
sqlite3 data/ecommerce.db

# 테이블 목록 확인
.tables

# 스키마 확인
.schema customers

# 쿼리 실행
SELECT * FROM customers LIMIT 5;

# 종료
.quit
```
