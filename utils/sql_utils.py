"""
SQL Query Optimization Tutorial - Common Utilities
각 Problem 스크립트에서 공통으로 사용하는 유틸리티 함수
"""

import sqlite3
import time
from contextlib import contextmanager


def get_connection(db_name='ecommerce.db'):
    """데이터베이스 연결 생성"""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def timer(description):
    """쿼리 실행 시간 측정"""
    start = time.time()
    yield
    end = time.time()
    print(f"\n⏱️  {description}: {(end - start)*1000:.2f}ms")


def execute_and_analyze(conn, query, description, show_plan=True, show_results=True, limit=10):
    """쿼리 실행 및 분석"""
    print(f"\n{'='*80}")
    print(f"🔍 {description}")
    print(f"{'='*80}")
    print(f"\n📝 SQL Query:")
    print(query)

    if show_plan:
        print(f"\n📊 Query Plan:")
        explain_query = f"EXPLAIN QUERY PLAN {query}"
        cursor = conn.cursor()
        for row in cursor.execute(explain_query):
            print(f"  {row}")

    if show_results:
        with timer(f"실행 시간"):
            cursor = conn.cursor()
            results = cursor.execute(query).fetchall()

        print(f"\n✅ 결과: {len(results)}개 행")
        if results and limit > 0:
            print(f"\n처음 {min(limit, len(results))}개 행:")
            for i, row in enumerate(results[:limit], 1):
                print(f"  {i}. {dict(row)}")

        return results

    return None


def print_header(title):
    """문제 헤더 출력"""
    print("\n" + "🔴 " * 40)
    print(title)
    print("🔴 " * 40)


def wait_for_input(message="\n⏸️  Press Enter to continue..."):
    """사용자 입력 대기"""
    input(message)
