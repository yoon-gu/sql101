# Utils Directory

SQL 쿼리 최적화 프로젝트 전체에서 공통으로 사용되는 유틸리티 함수 모음입니다.

## 파일 목록

- `sql_utils.py`: SQL 쿼리 실행 및 분석을 위한 공통 함수

## sql_utils.py

### 주요 함수

#### `get_connection(db_name='ecommerce.db')`
데이터베이스 연결을 생성합니다.

**Parameters:**
- `db_name` (str): 데이터베이스 파일 경로. 기본값은 'ecommerce.db'

**Returns:**
- `sqlite3.Connection`: SQLite 연결 객체

**사용 예시:**
```python
from utils.sql_utils import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM customers LIMIT 5")
results = cursor.fetchall()
conn.close()
```

#### `timer(description)`
쿼리 실행 시간을 측정하는 컨텍스트 매니저입니다.

**Parameters:**
- `description` (str): 측정 작업 설명

**사용 예시:**
```python
from utils.sql_utils import timer, get_connection

conn = get_connection()
with timer("고객 조회"):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    results = cursor.fetchall()
conn.close()

# 출력: ⏱️  고객 조회: 12.34ms
```

#### `execute_and_analyze(conn, query, description, show_plan=True, show_results=True, limit=10)`
쿼리를 실행하고 상세한 분석 결과를 출력합니다.

**Parameters:**
- `conn` (sqlite3.Connection): 데이터베이스 연결
- `query` (str): 실행할 SQL 쿼리
- `description` (str): 쿼리 설명
- `show_plan` (bool): EXPLAIN QUERY PLAN 표시 여부. 기본값 True
- `show_results` (bool): 결과 표시 여부. 기본값 True
- `limit` (int): 표시할 결과 행 수. 기본값 10

**Returns:**
- `list`: 쿼리 실행 결과 (show_results=True인 경우)
- `None`: show_results=False인 경우

**사용 예시:**
```python
from utils.sql_utils import get_connection, execute_and_analyze

conn = get_connection()

query = """
SELECT c.customer_name, COUNT(*) as order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING COUNT(*) > 5
ORDER BY order_count DESC
"""

results = execute_and_analyze(
    conn,
    query,
    "주문 많은 고객 조회",
    show_plan=True,
    show_results=True,
    limit=5
)

conn.close()
```

**출력 형식:**
```
================================================================================
🔍 주문 많은 고객 조회
================================================================================

📝 SQL Query:
SELECT c.customer_name, COUNT(*) as order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING COUNT(*) > 5
ORDER BY order_count DESC

📊 Query Plan:
  SCAN o
  SEARCH c USING INTEGER PRIMARY KEY (rowid=?)

⏱️  실행 시간: 15.23ms

✅ 결과: 234개 행

처음 5개 행:
  1. {'customer_name': 'Customer_123', 'order_count': 15}
  2. {'customer_name': 'Customer_456', 'order_count': 14}
  ...
```

#### `print_header(title)`
문제 헤더를 출력합니다.

**Parameters:**
- `title` (str): 헤더 제목

**사용 예시:**
```python
from utils.sql_utils import print_header

print_header("Problem 1: 불필요한 JOIN 제거")

# 출력:
# 🔴 🔴 🔴 🔴 🔴 ...
# Problem 1: 불필요한 JOIN 제거
# 🔴 🔴 🔴 🔴 🔴 ...
```

#### `wait_for_input(message="\n⏸️  Press Enter to continue...")`
사용자 입력을 기다립니다.

**Parameters:**
- `message` (str): 표시할 메시지. 기본값은 "Press Enter to continue..."

**사용 예시:**
```python
from utils.sql_utils import wait_for_input

print("비효율적 쿼리 실행 완료")
wait_for_input("\n⏸️  Press Enter to see optimized version...")
print("최적화 쿼리 실행...")
```

## 사용 위치

이 유틸리티 함수들은 다음 모듈에서 사용됩니다:

### 1. Problems 스크립트
```python
# problems/problem_1_duplicate_joins.py
from utils.sql_utils import (
    get_connection,
    execute_and_analyze,
    print_header,
    wait_for_input
)
```

### 2. Chatbot 채점 엔진
```python
# chatbot/sql_grader_agent.py
from utils.sql_utils import get_connection, timer
```

### 3. 데이터베이스 설정
```python
# data/setup_database.py
# 직접 sqlite3 사용하지만 참고 가능
```

## 개발 가이드

### 새로운 유틸리티 함수 추가

1. `sql_utils.py`에 함수 작성
2. Docstring 작성 (Google Style 권장)
3. 이 README.md에 문서 추가
4. 사용 예시 포함

### 함수 작성 가이드라인

```python
def new_utility_function(param1, param2, optional_param=None):
    """
    함수의 간단한 설명

    Args:
        param1 (type): 파라미터 1 설명
        param2 (type): 파라미터 2 설명
        optional_param (type, optional): 선택적 파라미터. 기본값 None

    Returns:
        type: 반환값 설명

    Example:
        >>> result = new_utility_function("value1", "value2")
        >>> print(result)
    """
    # 구현
    pass
```

## 의존성

- Python 3.8+
- sqlite3 (Python 내장)

외부 라이브러리 의존성 없음 - 순수 Python 표준 라이브러리만 사용합니다.

## 테스트

```python
# utils/sql_utils.py의 기능 테스트
import sys
sys.path.insert(0, '..')

from utils.sql_utils import *

# 연결 테스트
conn = get_connection('data/ecommerce.db')
print("✅ 연결 성공")

# 쿼리 실행 테스트
execute_and_analyze(
    conn,
    "SELECT COUNT(*) as total FROM customers",
    "테스트 쿼리",
    show_plan=True,
    show_results=True,
    limit=1
)

conn.close()
print("✅ 모든 테스트 통과")
```

## 문제 해결

### ModuleNotFoundError: No module named 'utils'

```bash
# 프로젝트 루트에서 실행해야 합니다
cd /path/to/sql101
uv run python problems/problem_1_duplicate_joins.py
```

### 데이터베이스 경로 오류

`get_connection()`의 기본 경로는 현재 디렉토리 기준입니다.
다른 디렉토리에서 실행하는 경우 절대 경로 또는 상대 경로를 명시하세요:

```python
# 절대 경로
conn = get_connection('/absolute/path/to/data/ecommerce.db')

# 상대 경로
conn = get_connection('../data/ecommerce.db')
```
