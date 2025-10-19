#!/usr/bin/env python3
"""
Problem 1: 불필요한 JOIN과 중복 서브쿼리

문제점:
- 같은 테이블을 여러 번 JOIN
- 중복된 서브쿼리 사용
- SELECT *로 불필요한 컬럼까지 조회

개선 방안:
- 중복 JOIN 제거
- 서브쿼리를 WITH 절로 변경
- 필요한 컬럼만 SELECT
"""

from sql_utils import get_connection, execute_and_analyze, print_header, wait_for_input


def inefficient_query(conn):
    """비효율적인 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "❌ 비효율적 쿼리 - 중복 JOIN & 중복 서브쿼리"
    )


def optimized_query(conn):
    """최적화된 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "✅ 최적화된 쿼리 - 중복 제거 & CTE 사용"
    )


def main():
    print_header("Problem 1: 불필요한 JOIN과 중복 서브쿼리")

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
1. 중복 JOIN 제거
   - 같은 테이블을 여러 번 JOIN하지 않기

2. CTE (Common Table Expression) 활용
   - 서브쿼리를 WITH 절로 변경하여 가독성과 성능 개선

3. 필요한 컬럼만 SELECT
   - SELECT * 대신 필요한 컬럼만 명시

4. INNER JOIN vs LEFT JOIN
   - WHERE 조건이 있는 경우 INNER JOIN이 더 효율적
        """)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
