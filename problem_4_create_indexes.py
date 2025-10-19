#!/usr/bin/env python3
"""
Problem 4: 인덱스 없이 대용량 데이터 조회

문제점:
- 인덱스가 없어 테이블 전체 스캔 (Full Table Scan) 발생
- JOIN, WHERE, ORDER BY 성능 저하

개선 방안:
- 자주 사용되는 컬럼에 인덱스 생성
- JOIN 키, WHERE 조건, ORDER BY 컬럼에 인덱스
"""

from sql_utils import get_connection, timer, print_header


def create_indexes(conn):
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

    cursor = conn.cursor()
    for idx_name, idx_query in indexes:
        with timer(f"Creating {idx_name}"):
            cursor.execute(idx_query)

    conn.commit()
    print("\n✅ 모든 인덱스 생성 완료!")


def show_indexes(conn):
    """생성된 인덱스 목록 조회"""
    print(f"\n{'='*80}")
    print("📋 생성된 인덱스 목록")
    print(f"{'='*80}\n")

    query = """
    SELECT name, tbl_name, sql
    FROM sqlite_master
    WHERE type = 'index'
    AND name LIKE 'idx_%'
    ORDER BY tbl_name, name
    """

    cursor = conn.cursor()
    results = cursor.execute(query).fetchall()

    if results:
        for row in results:
            print(f"📌 {row['name']}")
            print(f"   테이블: {row['tbl_name']}")
            print(f"   SQL: {row['sql']}")
            print()
    else:
        print("생성된 인덱스가 없습니다.")


def main():
    print_header("Problem 4: 인덱스 생성으로 성능 최적화")

    conn = get_connection()

    try:
        # 인덱스 생성 전 상태 확인
        print("\n현재 데이터베이스에 생성된 인덱스를 확인합니다...")
        show_indexes(conn)

        # 인덱스 생성
        input("\n⏸️  Press Enter to create indexes...")
        create_indexes(conn)

        # 인덱스 생성 후 상태 확인
        show_indexes(conn)

        print("\n" + "="*80)
        print("📚 학습 포인트:")
        print("="*80)
        print("""
1. 인덱스 생성 대상
   - JOIN 조건에 사용되는 컬럼 (FK)
   - WHERE 조건에 자주 사용되는 컬럼
   - ORDER BY, GROUP BY에 사용되는 컬럼

2. 인덱스 생성 시 주의사항
   - 너무 많은 인덱스는 INSERT/UPDATE/DELETE 성능 저하
   - 컬럼 선택도(Selectivity)가 높은 컬럼에 생성
   - 복합 인덱스(Composite Index) 고려

3. SQLite 인덱스 확인
   - sqlite_master 테이블에서 인덱스 정보 조회
   - EXPLAIN QUERY PLAN으로 인덱스 사용 여부 확인

4. 인덱스 효과
   - 테이블 전체 스캔 → 인덱스 스캔으로 변경
   - 대용량 데이터에서 큰 성능 향상
        """)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
