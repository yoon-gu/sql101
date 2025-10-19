"""
SQL Query Optimization Hands-on Tutorial
복잡하고 비효율적인 SQL 쿼리 분석 및 최적화 실습

이 튜토리얼에서 다루는 주요 문제점:
1. 불필요한 JOIN 연산
2. 중복 서브쿼리
3. SELECT * 사용
4. 인덱스 미사용
5. GROUP BY와 JOIN의 비효율적 조합
6. OUTER JOIN의 잘못된 사용
"""

import sqlite3
import time
from contextlib import contextmanager

class SQLOptimizationTutorial:
    def __init__(self, db_name='ecommerce.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    @contextmanager
    def timer(self, description):
        """쿼리 실행 시간 측정"""
        start = time.time()
        yield
        end = time.time()
        print(f"\n⏱️  {description}: {(end - start)*1000:.2f}ms")

    def execute_and_analyze(self, query, description, show_plan=True, show_results=True, limit=10):
        """쿼리 실행 및 분석"""
        print(f"\n{'='*80}")
        print(f"🔍 {description}")
        print(f"{'='*80}")
        print(f"\n📝 SQL Query:")
        print(query)

        if show_plan:
            print(f"\n📊 Query Plan:")
            explain_query = f"EXPLAIN QUERY PLAN {query}"
            cursor = self.conn.cursor()
            for row in cursor.execute(explain_query):
                print(f"  {row}")

        if show_results:
            with self.timer(f"실행 시간"):
                cursor = self.conn.cursor()
                results = cursor.execute(query).fetchall()

            print(f"\n✅ 결과: {len(results)}개 행")
            if results and limit > 0:
                print(f"\n처음 {min(limit, len(results))}개 행:")
                for i, row in enumerate(results[:limit], 1):
                    print(f"  {i}. {dict(row)}")

        return results


# ============================================================================
# 문제 1: 불필요한 JOIN과 중복 서브쿼리
# ============================================================================

def problem_1_inefficient(tutorial):
    """
    문제점:
    - 같은 테이블을 여러 번 JOIN
    - 중복된 서브쿼리 사용
    - SELECT *로 불필요한 컬럼까지 조회
    """

    query = """
    SELECT
        *
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
    """

    return tutorial.execute_and_analyze(
        query,
        "❌ 비효율적 쿼리 - 중복 JOIN & 중복 서브쿼리"
    )


def problem_1_optimized(tutorial):
    """
    개선 방안:
    - 중복 JOIN 제거
    - 서브쿼리를 WITH 절로 변경
    - 필요한 컬럼만 SELECT
    """

    query = """
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
    """

    return tutorial.execute_and_analyze(
        query,
        "✅ 최적화된 쿼리 - 중복 제거 & CTE 사용"
    )


# ============================================================================
# 문제 2: 비효율적인 GROUP BY와 다중 LEFT JOIN
# ============================================================================

def problem_2_inefficient(tutorial):
    """
    문제점:
    - 불필요한 LEFT JOIN (실제로는 INNER JOIN이 적합)
    - GROUP BY 전에 너무 많은 데이터 JOIN
    - 서브쿼리에서 중복 계산
    """

    query = """
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
    """

    return tutorial.execute_and_analyze(
        query,
        "❌ 비효율적 쿼리 - 과도한 LEFT JOIN & 중복 서브쿼리"
    )


def problem_2_optimized(tutorial):
    """
    개선 방안:
    - LEFT JOIN을 INNER JOIN으로 변경 (실제 필요한 경우만)
    - 불필요한 JOIN 제거
    - 서브쿼리 대신 GROUP BY 활용
    """

    query = """
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
    """

    return tutorial.execute_and_analyze(
        query,
        "✅ 최적화된 쿼리 - INNER JOIN & 단일 GROUP BY"
    )


# ============================================================================
# 문제 3: 복잡한 중첩 서브쿼리와 잘못된 JOIN 순서
# ============================================================================

def problem_3_inefficient(tutorial):
    """
    문제점:
    - 깊이 중첩된 서브쿼리
    - 카테시안 곱(Cartesian Product) 발생 가능
    - 같은 집계를 여러 번 계산
    """

    query = """
    SELECT
        p.product_name,
        c.category_name,
        (
            SELECT COUNT(*)
            FROM order_items oi2
            WHERE oi2.product_id = p.product_id
        ) as times_ordered,
        (
            SELECT SUM(oi3.quantity * oi3.unit_price * (1 - oi3.discount_rate))
            FROM order_items oi3
            INNER JOIN orders o3 ON oi3.order_id = o3.order_id
            WHERE oi3.product_id = p.product_id
            AND o3.order_status = 'Delivered'
        ) as total_revenue,
        (
            SELECT AVG(oi4.unit_price)
            FROM order_items oi4
            WHERE oi4.product_id = p.product_id
        ) as avg_price
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.category_id
    WHERE p.product_id IN (
        SELECT DISTINCT oi.product_id
        FROM order_items oi
        INNER JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_date >= '2024-01-01'
        AND o.order_status IN (
            SELECT DISTINCT order_status
            FROM orders
            WHERE order_status IN ('Delivered', 'Shipped')
        )
    )
    ORDER BY total_revenue DESC
    """

    return tutorial.execute_and_analyze(
        query,
        "❌ 비효율적 쿼리 - 중첩 서브쿼리 & 중복 계산",
        limit=5
    )


def problem_3_optimized(tutorial):
    """
    개선 방안:
    - 서브쿼리를 JOIN으로 변경
    - 한 번의 집계로 모든 값 계산
    - 불필요한 DISTINCT 제거
    """

    query = """
    WITH product_stats AS (
        SELECT
            oi.product_id,
            COUNT(*) as times_ordered,
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_rate)) as total_revenue,
            AVG(oi.unit_price) as avg_price
        FROM order_items oi
        INNER JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_date >= '2024-01-01'
        AND o.order_status IN ('Delivered', 'Shipped')
        GROUP BY oi.product_id
    )
    SELECT
        p.product_name,
        c.category_name,
        ps.times_ordered,
        ps.total_revenue,
        ps.avg_price
    FROM product_stats ps
    INNER JOIN products p ON ps.product_id = p.product_id
    LEFT JOIN categories c ON p.category_id = c.category_id
    ORDER BY ps.total_revenue DESC
    """

    return tutorial.execute_and_analyze(
        query,
        "✅ 최적화된 쿼리 - CTE & 단일 집계",
        limit=5
    )


# ============================================================================
# 문제 4: 인덱스 없이 대용량 데이터 조회
# ============================================================================

def problem_4_create_indexes(tutorial):
    """필요한 인덱스 생성"""

    print(f"\n{'='*80}")
    print("📌 성능 최적화를 위한 인덱스 생성")
    print(f"{'='*80}\n")

    indexes = [
        ("idx_orders_customer_id", "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id)"),
        ("idx_orders_status", "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status)"),
        ("idx_orders_date", "CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)"),
        ("idx_order_items_order_id", "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)"),
        ("idx_order_items_product_id", "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)"),
        ("idx_customers_region_id", "CREATE INDEX IF NOT EXISTS idx_customers_region_id ON customers(region_id)"),
        ("idx_products_category_id", "CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id)"),
        ("idx_customers_tier", "CREATE INDEX IF NOT EXISTS idx_customers_tier ON customers(customer_tier)"),
    ]

    cursor = tutorial.conn.cursor()
    for idx_name, idx_query in indexes:
        with tutorial.timer(f"Creating {idx_name}"):
            cursor.execute(idx_query)

    tutorial.conn.commit()
    print("\n✅ 모든 인덱스 생성 완료!")


# ============================================================================
# 문제 5: 잘못된 OUTER JOIN 사용
# ============================================================================

def problem_5_inefficient(tutorial):
    """
    문제점:
    - 필요 없는 곳에 LEFT OUTER JOIN 사용
    - WHERE 절이 OUTER JOIN을 무효화
    """

    query = """
    SELECT
        o.order_id,
        c.customer_name,
        p.product_name,
        cat.category_name
    FROM orders o
    LEFT OUTER JOIN customers c ON o.customer_id = c.customer_id
    LEFT OUTER JOIN order_items oi ON o.order_id = oi.order_id
    LEFT OUTER JOIN products p ON oi.product_id = p.product_id
    LEFT OUTER JOIN categories cat ON p.category_id = cat.category_id
    WHERE c.customer_tier = 'Gold'
    AND p.price > 100
    AND cat.category_name = 'Electronics'
    """

    return tutorial.execute_and_analyze(
        query,
        "❌ 비효율적 쿼리 - 불필요한 LEFT JOIN",
        limit=10
    )


def problem_5_optimized(tutorial):
    """
    개선 방안:
    - WHERE 절 조건이 있는 테이블은 INNER JOIN 사용
    """

    query = """
    SELECT
        o.order_id,
        c.customer_name,
        p.product_name,
        cat.category_name
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
    INNER JOIN categories cat ON p.category_id = cat.category_id
    WHERE c.customer_tier = 'Gold'
    AND p.price > 100
    AND cat.category_name = 'Electronics'
    """

    return tutorial.execute_and_analyze(
        query,
        "✅ 최적화된 쿼리 - INNER JOIN 사용",
        limit=10
    )


# ============================================================================
# 실습 메인 함수
# ============================================================================

def run_tutorial():
    """전체 튜토리얼 실행"""

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          SQL Query Optimization Hands-on Tutorial                         ║
║          복잡하고 비효율적인 SQL 쿼리 최적화 실습                                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)

    tutorial = SQLOptimizationTutorial()

    try:
        # 문제 1: 중복 JOIN & 서브쿼리
        print("\n" + "🔴 " * 40)
        print("Problem 1: 불필요한 JOIN과 중복 서브쿼리")
        print("🔴 " * 40)

        problem_1_inefficient(tutorial)
        input("\n⏸️  Press Enter to see optimized version...")
        problem_1_optimized(tutorial)

        # 문제 2: 비효율적 GROUP BY
        input("\n\n⏸️  Press Enter to continue to Problem 2...")
        print("\n" + "🔴 " * 40)
        print("Problem 2: 비효율적인 GROUP BY와 다중 LEFT JOIN")
        print("🔴 " * 40)

        problem_2_inefficient(tutorial)
        input("\n⏸️  Press Enter to see optimized version...")
        problem_2_optimized(tutorial)

        # 문제 3: 중첩 서브쿼리
        input("\n\n⏸️  Press Enter to continue to Problem 3...")
        print("\n" + "🔴 " * 40)
        print("Problem 3: 복잡한 중첩 서브쿼리와 잘못된 JOIN 순서")
        print("🔴 " * 40)

        problem_3_inefficient(tutorial)
        input("\n⏸️  Press Enter to see optimized version...")
        problem_3_optimized(tutorial)

        # 인덱스 생성
        input("\n\n⏸️  Press Enter to create indexes...")
        problem_4_create_indexes(tutorial)

        # 문제 5: 잘못된 OUTER JOIN
        input("\n\n⏸️  Press Enter to continue to Problem 5...")
        print("\n" + "🔴 " * 40)
        print("Problem 5: 잘못된 OUTER JOIN 사용")
        print("🔴 " * 40)

        problem_5_inefficient(tutorial)
        input("\n⏸️  Press Enter to see optimized version...")
        problem_5_optimized(tutorial)

        print(f"\n{'='*80}")
        print("🎉 튜토리얼 완료!")
        print(f"{'='*80}")
        print("""
주요 학습 내용:
1. ✅ 중복 JOIN 제거 및 CTE(Common Table Expression) 활용
2. ✅ LEFT JOIN vs INNER JOIN 올바른 사용
3. ✅ 서브쿼리를 JOIN으로 변환하여 성능 개선
4. ✅ GROUP BY와 집계 함수의 효율적 사용
5. ✅ 인덱스를 통한 성능 최적화
6. ✅ SELECT * 대신 필요한 컬럼만 조회
7. ✅ EXPLAIN QUERY PLAN을 통한 실행 계획 분석
        """)

    finally:
        tutorial.close()


if __name__ == "__main__":
    run_tutorial()
