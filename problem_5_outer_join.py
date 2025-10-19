#!/usr/bin/env python3
"""
Problem 5: 잘못된 OUTER JOIN 사용

문제점:
- 필요 없는 곳에 LEFT OUTER JOIN 사용
- WHERE 절이 OUTER JOIN을 무효화
- OUTER JOIN은 INNER JOIN보다 비용이 더 큼

개선 방안:
- WHERE 절 조건이 있는 테이블은 INNER JOIN 사용
- NULL 값이 필요한 경우만 LEFT/RIGHT JOIN 사용
"""

from sql_utils import get_connection, execute_and_analyze, print_header, wait_for_input


def inefficient_query(conn):
    """비효율적인 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "❌ 비효율적 쿼리 - 불필요한 LEFT JOIN",
        limit=10
    )


def optimized_query(conn):
    """최적화된 쿼리"""
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

    return execute_and_analyze(
        conn,
        query,
        "✅ 최적화된 쿼리 - INNER JOIN 사용",
        limit=10
    )


def main():
    print_header("Problem 5: 잘못된 OUTER JOIN 사용")

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
1. LEFT JOIN vs INNER JOIN
   - LEFT JOIN: 왼쪽 테이블의 모든 행 + 오른쪽 테이블의 매칭되는 행
   - INNER JOIN: 양쪽 테이블에서 매칭되는 행만
   - WHERE 절에서 오른쪽 테이블의 컬럼을 사용하면 LEFT JOIN이 무의미

2. WHERE 절이 OUTER JOIN을 무효화하는 경우
   - LEFT JOIN한 테이블의 컬럼을 WHERE 절에서 사용
   - NULL이 아닌 값을 요구하면 INNER JOIN과 동일한 결과
   - 예: WHERE c.customer_tier = 'Gold' → NULL 제외

3. 성능 차이
   - INNER JOIN이 OUTER JOIN보다 일반적으로 빠름
   - 옵티마이저가 더 효율적인 실행 계획 수립 가능

4. OUTER JOIN을 사용해야 하는 경우
   - 한쪽 테이블의 모든 데이터가 필요한 경우
   - NULL 값도 결과에 포함해야 하는 경우
   - 예: 주문이 없는 고객도 조회하고 싶을 때
        """)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
