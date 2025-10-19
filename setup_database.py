"""
SQL Query Optimization Hands-on - Database Setup
복잡하고 비효율적인 SQL 쿼리 최적화 실습용 데이터베이스 생성
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_sample_database(db_name='ecommerce.db'):
    """전자상거래 샘플 데이터베이스 생성"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 기존 테이블 삭제
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS categories")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS regions")

    # 1. 지역 테이블
    cursor.execute("""
        CREATE TABLE regions (
            region_id INTEGER PRIMARY KEY,
            region_name TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)

    # 2. 고객 테이블
    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            region_id INTEGER,
            join_date DATE,
            customer_tier TEXT,
            FOREIGN KEY (region_id) REFERENCES regions(region_id)
        )
    """)

    # 3. 카테고리 테이블
    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL,
            parent_category_id INTEGER
        )
    """)

    # 4. 제품 테이블
    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category_id INTEGER,
            price REAL,
            stock_quantity INTEGER,
            supplier TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    # 5. 주문 테이블
    cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            order_status TEXT,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)

    # 6. 주문 상세 테이블
    cursor.execute("""
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            discount_rate REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    print("테이블 생성 완료!")

    # 샘플 데이터 삽입
    print("샘플 데이터 삽입 중...")

    # 지역 데이터
    regions = [
        (1, 'Seoul', 'South Korea'),
        (2, 'Busan', 'South Korea'),
        (3, 'Tokyo', 'Japan'),
        (4, 'Osaka', 'Japan'),
        (5, 'Beijing', 'China'),
        (6, 'Shanghai', 'China'),
    ]
    cursor.executemany("INSERT INTO regions VALUES (?, ?, ?)", regions)

    # 카테고리 데이터
    categories = [
        (1, 'Electronics', None),
        (2, 'Clothing', None),
        (3, 'Food', None),
        (4, 'Smartphones', 1),
        (5, 'Laptops', 1),
        (6, 'Men', 2),
        (7, 'Women', 2),
        (8, 'Snacks', 3),
        (9, 'Beverages', 3),
    ]
    cursor.executemany("INSERT INTO categories VALUES (?, ?, ?)", categories)

    # 고객 데이터 (1000명)
    customers = []
    tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    start_date = datetime(2020, 1, 1)

    for i in range(1, 1001):
        region_id = random.randint(1, 6)
        join_date = start_date + timedelta(days=random.randint(0, 1500))
        tier = random.choice(tiers)
        customers.append((
            i,
            f'Customer_{i}',
            f'customer{i}@email.com',
            region_id,
            join_date.strftime('%Y-%m-%d'),
            tier
        ))

    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
        customers
    )

    # 제품 데이터 (500개)
    products = []
    suppliers = ['Supplier_A', 'Supplier_B', 'Supplier_C', 'Supplier_D']

    for i in range(1, 501):
        category_id = random.randint(1, 9)
        price = round(random.uniform(10, 1000), 2)
        stock = random.randint(0, 500)
        supplier = random.choice(suppliers)
        products.append((
            i,
            f'Product_{i}',
            category_id,
            price,
            stock,
            supplier
        ))

    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)",
        products
    )

    # 주문 데이터 (5000개)
    orders = []
    statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    order_start_date = datetime(2023, 1, 1)

    for i in range(1, 5001):
        customer_id = random.randint(1, 1000)
        order_date = order_start_date + timedelta(days=random.randint(0, 700))
        status = random.choice(statuses)
        total_amount = round(random.uniform(50, 5000), 2)
        orders.append((
            i,
            customer_id,
            order_date.strftime('%Y-%m-%d'),
            status,
            total_amount
        ))

    cursor.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
        orders
    )

    # 주문 상세 데이터 (각 주문당 1-5개 항목)
    order_items = []
    order_item_id = 1

    for order_id in range(1, 5001):
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product_id = random.randint(1, 500)
            quantity = random.randint(1, 10)
            # 실제 제품 가격 가져오기
            cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
            unit_price = cursor.fetchone()[0]
            discount_rate = random.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2])

            order_items.append((
                order_item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                discount_rate
            ))
            order_item_id += 1

    cursor.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)",
        order_items
    )

    conn.commit()

    print(f"✅ 데이터베이스 생성 완료!")
    print(f"  - 지역: {len(regions)}개")
    print(f"  - 카테고리: {len(categories)}개")
    print(f"  - 고객: {len(customers)}명")
    print(f"  - 제품: {len(products)}개")
    print(f"  - 주문: {len(orders)}건")
    print(f"  - 주문 상세: {len(order_items)}건")

    # 인덱스 없는 상태로 시작 (최적화 실습용)
    print("\n⚠️  성능 최적화를 위한 인덱스는 아직 생성되지 않았습니다.")
    print("    실습 과정에서 필요한 인덱스를 직접 생성하게 됩니다.")

    conn.close()
    return db_name

if __name__ == "__main__":
    create_sample_database()
