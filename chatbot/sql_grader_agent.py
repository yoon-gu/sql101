"""
SQL Query Optimization Grader Agent
LangGraph를 사용한 SQL 쿼리 최적화 문제 출제 및 채점 시스템
"""

import sqlite3
import time
import sys
from pathlib import Path
from typing import TypedDict, Annotated, Literal
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.sql_utils import get_connection, timer


@dataclass
class SQLProblem:
    """SQL 최적화 문제"""
    problem_id: int
    title: str
    description: str
    inefficient_query: str
    optimal_query: str
    expected_rows: int
    hints: list[str]


class GraderState(TypedDict):
    """채점 시스템 상태"""
    problem: SQLProblem | None
    user_query: str
    execution_time: float
    result_count: int
    is_correct: bool
    score: int
    feedback: str
    messages: list[dict]


class SQLGraderAgent:
    """SQL 쿼리 채점 에이전트"""

    def __init__(self, db_name='data/ecommerce.db'):
        self.db_name = db_name
        self.problems = self._load_problems()

    def _load_problems(self) -> list[SQLProblem]:
        """문제 목록 로드"""
        return [
            SQLProblem(
                problem_id=1,
                title="불필요한 JOIN과 중복 서브쿼리 제거",
                description="""
다음 쿼리는 같은 테이블을 여러 번 JOIN하고 중복된 서브쿼리를 사용합니다.
이를 최적화하여 같은 결과를 더 빠르게 조회하세요.

**조건:**
- order_status가 'Delivered'인 주문
- total_amount가 평균 이상
- 한국(South Korea) 지역의 고객

**반환 컬럼:** order_id, order_date, total_amount, customer_name, customer_tier, region_name
""",
                inefficient_query="""
SELECT *
FROM orders o
LEFT JOIN customers c1 ON o.customer_id = c1.customer_id
LEFT JOIN customers c2 ON o.customer_id = c2.customer_id
LEFT JOIN regions r1 ON c1.region_id = r1.region_id
LEFT JOIN regions r2 ON c2.region_id = r2.region_id
WHERE o.order_status = 'Delivered'
AND o.total_amount > (
    SELECT AVG(total_amount) FROM orders WHERE order_status = 'Delivered'
)
AND c1.customer_tier IN (
    SELECT customer_tier FROM customers
    WHERE region_id IN (
        SELECT region_id FROM regions WHERE country = 'South Korea'
    )
)
""",
                optimal_query="""
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
""",
                expected_rows=150,
                hints=[
                    "CTE(WITH 절)를 사용하여 서브쿼리 결과를 재사용하세요",
                    "중복된 JOIN을 제거하세요",
                    "필요한 컬럼만 SELECT하세요",
                    "LEFT JOIN 대신 INNER JOIN을 사용하세요"
                ]
            ),
            SQLProblem(
                problem_id=2,
                title="비효율적인 GROUP BY 최적화",
                description="""
다음 쿼리는 불필요한 LEFT JOIN과 중복 서브쿼리를 사용합니다.
2024년 이후 주문한 고객별 통계를 효율적으로 조회하세요.

**조건:**
- 2024-01-01 이후 주문
- 주문 건수가 5건 초과인 고객
- 총 주문금액 내림차순 정렬

**반환 컬럼:** customer_name, region_name, order_count, total_spent, avg_order, max_order, min_order
""",
                inefficient_query="""
SELECT
    c.customer_name,
    r.region_name,
    COUNT(*) as order_count,
    SUM(o.total_amount) as total_spent,
    (SELECT AVG(total_amount) FROM orders WHERE customer_id = c.customer_id) as avg_order,
    (SELECT MAX(total_amount) FROM orders WHERE customer_id = c.customer_id) as max_order,
    (SELECT MIN(total_amount) FROM orders WHERE customer_id = c.customer_id) as min_order
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN regions r ON c.region_id = r.region_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_id, c.customer_name, r.region_name
HAVING COUNT(*) > 5
ORDER BY total_spent DESC
""",
                optimal_query="""
SELECT
    c.customer_name,
    r.region_name,
    COUNT(DISTINCT o.order_id) as order_count,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order,
    MAX(o.total_amount) as max_order,
    MIN(o.total_amount) as min_order
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN regions r ON c.region_id = r.region_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_id, c.customer_name, r.region_name
HAVING COUNT(DISTINCT o.order_id) > 5
ORDER BY total_spent DESC
""",
                expected_rows=545,
                hints=[
                    "불필요한 테이블 JOIN을 제거하세요 (order_items, products는 결과에 사용되지 않음)",
                    "서브쿼리 대신 GROUP BY의 집계 함수를 사용하세요",
                    "LEFT JOIN 대신 INNER JOIN을 사용하세요",
                    "COUNT DISTINCT를 사용하여 중복을 제거하세요"
                ]
            ),
        ]

    def get_problem(self, problem_id: int) -> SQLProblem | None:
        """문제 ID로 문제 가져오기"""
        for problem in self.problems:
            if problem.problem_id == problem_id:
                return problem
        return None

    def execute_query(self, query: str) -> tuple[list, float]:
        """쿼리 실행 및 시간 측정"""
        conn = get_connection(self.db_name)
        cursor = conn.cursor()

        start = time.time()
        try:
            results = cursor.execute(query).fetchall()
            execution_time = (time.time() - start) * 1000  # ms
            return results, execution_time
        except Exception as e:
            raise Exception(f"쿼리 실행 오류: {str(e)}")
        finally:
            conn.close()

    def verify_results(self, user_results: list, optimal_results: list) -> bool:
        """결과 검증 - 순서 무관하게 같은 데이터인지 확인"""
        if len(user_results) != len(optimal_results):
            return False

        # 결과를 정렬 가능한 형태로 변환
        user_set = {tuple(dict(row).values()) for row in user_results}
        optimal_set = {tuple(dict(row).values()) for row in optimal_results}

        return user_set == optimal_set

    def grade_query(self, problem: SQLProblem, user_query: str) -> dict:
        """쿼리 채점"""
        try:
            # 사용자 쿼리 실행
            user_results, user_time = self.execute_query(user_query)

            # 최적 쿼리 실행
            optimal_results, optimal_time = self.execute_query(problem.optimal_query)

            # 비효율적 쿼리 실행 (비교용)
            inefficient_results, inefficient_time = self.execute_query(problem.inefficient_query)

            # 결과 검증
            is_correct = self.verify_results(user_results, optimal_results)

            if not is_correct:
                return {
                    "is_correct": False,
                    "score": 0,
                    "execution_time": user_time,
                    "result_count": len(user_results),
                    "feedback": f"""
❌ **오답입니다.**

**문제점:**
- 예상 결과: {len(optimal_results)}개 행
- 실제 결과: {len(user_results)}개 행
- 쿼리 결과가 올바르지 않습니다.

**힌트:**
{chr(10).join(f"- {hint}" for hint in problem.hints)}
"""
                }

            # 성능 점수 계산
            speedup = inefficient_time / user_time if user_time > 0 else 1

            if speedup >= 1.5:
                performance_score = 100
                performance_msg = "🌟 **매우 우수함** - 비효율적 쿼리보다 훨씬 빠릅니다!"
            elif speedup >= 1.2:
                performance_score = 90
                performance_msg = "✅ **우수함** - 성능이 크게 개선되었습니다."
            elif speedup >= 1.0:
                performance_score = 80
                performance_msg = "👍 **양호함** - 성능이 개선되었습니다."
            else:
                performance_score = 70
                performance_msg = "⚠️ **주의** - 성능이 기대보다 낮습니다."

            # 최적 쿼리와 비교
            optimal_ratio = user_time / optimal_time if optimal_time > 0 else 1

            feedback = f"""
✅ **정답입니다!**

**성능 분석:**
- 비효율적 쿼리: {inefficient_time:.2f}ms
- 사용자 쿼리: {user_time:.2f}ms
- 최적 쿼리: {optimal_time:.2f}ms

**개선도:**
- 비효율적 대비: {speedup:.2f}배 빠름
- 최적 대비: {optimal_ratio:.2f}배 {'느림' if optimal_ratio > 1 else '빠름'}

**점수:** {performance_score}/100

{performance_msg}

**결과:** {len(user_results)}개 행 반환 ✅

**추가 최적화 팁:**
{chr(10).join(f"- {hint}" for hint in problem.hints[:2])}
"""

            return {
                "is_correct": True,
                "score": performance_score,
                "execution_time": user_time,
                "result_count": len(user_results),
                "feedback": feedback
            }

        except Exception as e:
            return {
                "is_correct": False,
                "score": 0,
                "execution_time": 0,
                "result_count": 0,
                "feedback": f"""
❌ **쿼리 실행 오류**

**에러 메시지:**
{str(e)}

**힌트:**
- SQL 문법을 확인하세요
- 테이블명과 컬럼명을 확인하세요
- JOIN 조건을 확인하세요
"""
            }


def create_grader() -> SQLGraderAgent:
    """채점 에이전트 생성"""
    return SQLGraderAgent()


if __name__ == "__main__":
    # 테스트
    grader = create_grader()
    problem = grader.get_problem(1)

    if problem:
        print(f"문제: {problem.title}")
        print(f"설명: {problem.description}")

        # 최적 쿼리로 테스트
        result = grader.grade_query(problem, problem.optimal_query)
        print(f"\n채점 결과:")
        print(result["feedback"])
