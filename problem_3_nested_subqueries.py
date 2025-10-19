#!/usr/bin/env python3
"""
Problem 3: 복잡한 중첩 서브쿼리와 잘못된 JOIN 순서

문제점:
- 깊이 중첩된 서브쿼리
- 카테시안 곱(Cartesian Product) 발생 가능
- 같은 집계를 여러 번 계산

개선 방안:
- 서브쿼리를 JOIN으로 변경
- 한 번의 집계로 모든 값 계산
- 불필요한 DISTINCT 제거
"""

from sql_utils import get_connection, execute_and_analyze, print_header, wait_for_input


def inefficient_query(conn):
    """비효율적인 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "❌ 비효율적 쿼리 - 중첩 서브쿼리 & 중복 계산",
        limit=5
    )


def optimized_query(conn):
    """최적화된 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "✅ 최적화된 쿼리 - CTE & 단일 집계",
        limit=5
    )


def main():
    print_header("Problem 3: 복잡한 중첩 서브쿼리와 잘못된 JOIN 순서")

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
1. 중첩 서브쿼리를 CTE로 변경
   - 같은 데이터를 여러 번 조회하지 않고 한 번에 집계
   - 가독성과 유지보수성 향상

2. SELECT 절의 스칼라 서브쿼리 제거
   - 각 행마다 서브쿼리가 실행되어 매우 비효율적
   - CTE에서 미리 집계한 결과를 JOIN

3. 불필요한 DISTINCT 제거
   - IN ('Delivered', 'Shipped')처럼 명시적으로 값을 나열하면
   - DISTINCT가 불필요

4. JOIN 순서 최적화
   - 먼저 필터링하고 집계한 후 JOIN
   - 처리할 데이터 양을 줄여 성능 향상
        """)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
