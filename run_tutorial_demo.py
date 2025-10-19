"""
SQL Query Optimization Tutorial - Demo Runner
대화형 프롬프트 없이 자동으로 전체 튜토리얼 실행
"""

from sql_optimization_tutorial import *

def run_demo():
    """전체 튜토리얼 자동 실행"""

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
        print("\n" + "➡️  " * 40)
        problem_1_optimized(tutorial)

        # 문제 2: 비효율적 GROUP BY
        print("\n\n" + "🔴 " * 40)
        print("Problem 2: 비효율적인 GROUP BY와 다중 LEFT JOIN")
        print("🔴 " * 40)

        problem_2_inefficient(tutorial)
        print("\n" + "➡️  " * 40)
        problem_2_optimized(tutorial)

        # 문제 3: 중첩 서브쿼리
        print("\n\n" + "🔴 " * 40)
        print("Problem 3: 복잡한 중첩 서브쿼리와 잘못된 JOIN 순서")
        print("🔴 " * 40)

        problem_3_inefficient(tutorial)
        print("\n" + "➡️  " * 40)
        problem_3_optimized(tutorial)

        # 인덱스 생성
        print("\n\n" + "🔵 " * 40)
        print("Problem 4: 인덱스 생성으로 성능 최적화")
        print("🔵 " * 40)
        problem_4_create_indexes(tutorial)

        # 문제 5: 잘못된 OUTER JOIN
        print("\n\n" + "🔴 " * 40)
        print("Problem 5: 잘못된 OUTER JOIN 사용")
        print("🔴 " * 40)

        problem_5_inefficient(tutorial)
        print("\n" + "➡️  " * 40)
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

성능 개선 요약:
- 중복 제거와 CTE 사용으로 대폭적인 성능 향상
- 불필요한 JOIN 제거로 쿼리 단순화
- 인덱스 활용으로 검색 속도 향상
- 서브쿼리를 CTE/JOIN으로 변경하여 중복 계산 제거
        """)

    finally:
        tutorial.close()


if __name__ == "__main__":
    run_demo()
