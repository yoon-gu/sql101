# SQL Query Optimization Chatbot - 사용 예시

## 1. 챗봇 시작하기

```bash
# 챗봇 실행
uv run python app.py

# 출력:
# Running on local URL:  http://127.0.0.1:7860
# To create a public link, set `share=True` in `launch()`.
```

브라우저에서 http://localhost:7860 접속

## 2. 문제 선택

**Problem 1: 불필요한 JOIN과 중복 서브쿼리 제거** 선택

챗봇이 다음과 같이 문제를 출제:

```
📝 불필요한 JOIN과 중복 서브쿼리 제거

다음 쿼리는 같은 테이블을 여러 번 JOIN하고 중복된 서브쿼리를 사용합니다.
이를 최적화하여 같은 결과를 더 빠르게 조회하세요.

조건:
- order_status가 'Delivered'인 주문
- total_amount가 평균 이상
- 한국(South Korea) 지역의 고객

반환 컬럼: order_id, order_date, total_amount, customer_name, customer_tier, region_name

[비효율적인 쿼리 표시]

힌트:
1. CTE(WITH 절)를 사용하여 서브쿼리 결과를 재사용하세요
2. 중복된 JOIN을 제거하세요
3. 필요한 컬럼만 SELECT하세요
4. LEFT JOIN 대신 INNER JOIN을 사용하세요
```

## 3. 쿼리 작성 및 제출

### 예시 1: 잘못된 쿼리 제출

**제출한 쿼리:**
```sql
SELECT * FROM orders
WHERE order_status = 'Delivered'
```

**채점 결과:**
```
❌ 오답입니다.

문제점:
- 예상 결과: 146개 행
- 실제 결과: 2534개 행
- 쿼리 결과가 올바르지 않습니다.

힌트:
- CTE(WITH 절)를 사용하여 서브쿼리 결과를 재사용하세요
- 중복된 JOIN을 제거하세요
- 필요한 컬럼만 SELECT하세요
- LEFT JOIN 대신 INNER JOIN을 사용하세요
```

### 예시 2: 정답 쿼리 제출

**제출한 쿼리:**
```sql
WITH avg_amount AS (
    SELECT AVG(total_amount) as avg_total
    FROM orders
    WHERE order_status = 'Delivered'
)
SELECT
    o.order_id,
    o.order_date,
    o.total_amount,
    c.customer_name,
    c.customer_tier,
    r.region_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN regions r ON c.region_id = r.region_id
CROSS JOIN avg_amount
WHERE o.order_status = 'Delivered'
AND o.total_amount > avg_amount.avg_total
AND r.country = 'South Korea'
```

**채점 결과:**
```
✅ 정답입니다!

성능 분석:
- 비효율적 쿼리: 3.45ms
- 사용자 쿼리: 1.82ms
- 최적 쿼리: 1.75ms

개선도:
- 비효율적 대비: 1.89배 빠름
- 최적 대비: 1.04배 느림

점수: 100/100

🌟 매우 우수함 - 비효율적 쿼리보다 훨씬 빠릅니다!

결과: 146개 행 반환 ✅

추가 최적화 팁:
- CTE(WITH 절)를 사용하여 서브쿼리 결과를 재사용하세요
- 중복된 JOIN을 제거하세요
```

## 4. 정답 보기

"💡 정답 보기" 버튼 클릭 시:

```
💡 모범 답안

[최적화된 쿼리 표시]

🎯 최적화 포인트

✅ CTE(WITH 절)를 사용하여 서브쿼리 결과를 재사용하세요
✅ 중복된 JOIN을 제거하세요
✅ 필요한 컬럼만 SELECT하세요
✅ LEFT JOIN 대신 INNER JOIN을 사용하세요

이 쿼리를 복사하여 직접 실행해보고 성능을 비교해보세요!
```

## 5. 초기화

"🔄 초기화" 버튼 클릭 시 모든 대화 내역이 삭제되고 처음부터 다시 시작할 수 있습니다.

## 채점 기준

### 정확성
- ✅ 올바른 행 개수 반환
- ✅ 정확한 데이터 내용

### 성능 점수
| 점수 | 조건 | 평가 |
|------|------|------|
| 100점 | 비효율적 대비 1.5배 이상 빠름 | 🌟 매우 우수함 |
| 90점 | 비효율적 대비 1.2배 이상 빠름 | ✅ 우수함 |
| 80점 | 비효율적 대비 1.0배 이상 빠름 | 👍 양호함 |
| 70점 | 비효율적 대비 느림 | ⚠️ 주의 |

## 주요 학습 포인트

### Problem 1: 불필요한 JOIN과 중복 서브쿼리
- ✅ CTE(Common Table Expression) 활용
- ✅ 중복 JOIN 제거
- ✅ SELECT * 대신 필요한 컬럼만 선택
- ✅ LEFT JOIN vs INNER JOIN 적절한 사용

### Problem 2: 비효율적인 GROUP BY
- ✅ 불필요한 테이블 조인 제거
- ✅ 서브쿼리 대신 집계 함수 활용
- ✅ COUNT DISTINCT 사용
- ✅ GROUP BY 성능 최적화

## 실행 환경

- **Python**: 3.8+
- **Gradio**: 5.x
- **SQLite3**: 내장
- **데이터**: ecommerce.db (1.3MB, 약 15,000건)

## 문제 해결

### 오류: "ecommerce.db 파일이 없습니다"

```bash
# 데이터베이스 생성
uv run python setup_database.py
```

### 오류: "포트 7860이 이미 사용 중입니다"

app.py 파일 수정:
```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7861,  # 다른 포트 사용
    share=False
)
```

### Gradio가 설치되지 않음

```bash
# uv로 재설치
uv sync

# 또는 pip로 설치
pip install gradio
```
