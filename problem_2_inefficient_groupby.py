#!/usr/bin/env python3
"""
Problem 2: 비효율적인 GROUP BY와 다중 LEFT JOIN

문제점:
- 불필요한 LEFT JOIN (실제로는 INNER JOIN이 적합)
- GROUP BY 전에 너무 많은 데이터 JOIN
- 서브쿼리에서 중복 계산

개선 방안:
- LEFT JOIN을 INNER JOIN으로 변경 (실제 필요한 경우만)
- 불필요한 JOIN 제거
- 서브쿼리 대신 GROUP BY 활용
"""

from sql_utils import get_connection, execute_and_analyze, print_header, wait_for_input


def inefficient_query(conn):
    """비효율적인 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "❌ 비효율적 쿼리 - 과도한 LEFT JOIN & 중복 서브쿼리"
    )


def optimized_query(conn):
    """최적화된 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "✅ 최적화된 쿼리 - INNER JOIN & 단일 GROUP BY"
    )


def main():
    print_header("Problem 2: 비효율적인 GROUP BY와 다중 LEFT JOIN")

    conn = get_connection()

    try:
        # 비효율적인 쿼리 실행
        inefficient_query(conn)

        # 최적화된 쿼리 실행
        wait_for_input("\n⏸️  Press Enter to see optimized version...")
        optimized_query(conn)

        print("\n" + "="*80)
        print("📚 학습 포인트:")
        print("="*80)
        print("""
1. 불필요한 JOIN 제거
   - 실제로 사용하지 않는 테이블은 JOIN하지 않기
   - products 테이블과 order_items 테이블이 결과에 사용되지 않음

2. 서브쿼리 대신 집계 함수 사용
   - 같은 데이터를 여러 번 서브쿼리로 조회하지 않고
   - GROUP BY와 집계 함수를 한 번에 사용

3. LEFT JOIN vs INNER JOIN
   - WHERE 절에서 JOIN된 테이블의 컬럼을 사용하면 LEFT JOIN이 무의미
   - NULL 값이 필요 없다면 INNER JOIN 사용

4. COUNT DISTINCT 사용
   - JOIN으로 인한 중복 행을 고려하여 DISTINCT 사용
        """)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
