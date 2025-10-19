"""
SQL Query Optimization Chatbot with Gradio
LangGraph 기반 SQL 쿼리 최적화 챗봇
"""

import gradio as gr
from sql_grader_agent import SQLGraderAgent, SQLProblem


class SQLChatbot:
    """SQL 최적화 챗봇"""

    def __init__(self):
        self.grader = SQLGraderAgent()
        self.current_problem: SQLProblem | None = None
        self.problem_shown = False

    def reset(self):
        """상태 초기화"""
        self.current_problem = None
        self.problem_shown = False
        return [], "문제를 선택하세요.", ""

    def select_problem(self, problem_id: int) -> tuple[list, str, str]:
        """문제 선택"""
        self.current_problem = self.grader.get_problem(problem_id)
        self.problem_shown = True

        if not self.current_problem:
            return [], "문제를 찾을 수 없습니다.", ""

        # 문제 설명 생성
        problem_text = f"""
# 📝 {self.current_problem.title}

{self.current_problem.description}

---

## 🔍 비효율적인 쿼리 (참고용)

```sql
{self.current_problem.inefficient_query.strip()}
```

---

## ✍️ 과제

위 쿼리를 최적화하여 **같은 결과**를 **더 빠르게** 조회하는 쿼리를 작성하세요!

**힌트:**
{chr(10).join(f"{i+1}. {hint}" for i, hint in enumerate(self.current_problem.hints))}

---

아래 SQL 입력창에 최적화된 쿼리를 작성하고 "제출 및 채점" 버튼을 클릭하세요.
"""

        chat_history = [
            {
                "role": "assistant",
                "content": problem_text
            }
        ]

        return chat_history, problem_text, ""

    def submit_query(self, query: str, chat_history: list) -> tuple[list, str]:
        """쿼리 제출 및 채점"""
        if not self.current_problem:
            error_msg = "먼저 문제를 선택해주세요."
            chat_history.append({
                "role": "user",
                "content": query
            })
            chat_history.append({
                "role": "assistant",
                "content": error_msg
            })
            return chat_history, ""

        if not query.strip():
            error_msg = "SQL 쿼리를 입력해주세요."
            chat_history.append({
                "role": "assistant",
                "content": error_msg
            })
            return chat_history, ""

        # 사용자 쿼리 추가
        chat_history.append({
            "role": "user",
            "content": f"```sql\n{query.strip()}\n```"
        })

        # 채점
        result = self.grader.grade_query(self.current_problem, query)

        # 채점 결과 추가
        chat_history.append({
            "role": "assistant",
            "content": result["feedback"]
        })

        return chat_history, ""

    def show_solution(self, chat_history: list) -> list:
        """정답 보기"""
        if not self.current_problem:
            chat_history.append({
                "role": "assistant",
                "content": "먼저 문제를 선택해주세요."
            })
            return chat_history

        solution_text = f"""
# 💡 모범 답안

```sql
{self.current_problem.optimal_query.strip()}
```

## 🎯 최적화 포인트

{chr(10).join(f"✅ {hint}" for hint in self.current_problem.hints)}

---

이 쿼리를 복사하여 직접 실행해보고 성능을 비교해보세요!
"""

        chat_history.append({
            "role": "assistant",
            "content": solution_text
        })

        return chat_history


def create_ui():
    """Gradio UI 생성"""
    chatbot_instance = SQLChatbot()

    with gr.Blocks(
        title="SQL Query Optimization Chatbot",
        theme=gr.themes.Soft(),
        css="""
        .problem-selector {
            margin-bottom: 20px;
        }
        .sql-input {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
        }
        """
    ) as demo:
        gr.Markdown("""
# 🎓 SQL Query Optimization Chatbot

SQL 쿼리 최적화 문제를 풀고 실시간 피드백을 받아보세요!

**사용 방법:**
1. 아래에서 문제를 선택하세요
2. 비효율적인 쿼리를 분석하고 최적화된 쿼리를 작성하세요
3. "제출 및 채점" 버튼을 클릭하여 채점 받으세요
4. 막히면 "정답 보기" 버튼을 눌러 해설을 확인하세요
        """)

        with gr.Row():
            with gr.Column(scale=2):
                # 문제 선택
                problem_selector = gr.Radio(
                    choices=[
                        ("Problem 1: 불필요한 JOIN과 중복 서브쿼리 제거", 1),
                        ("Problem 2: 비효율적인 GROUP BY 최적화", 2),
                    ],
                    label="📚 문제 선택",
                    value=None,
                    elem_classes=["problem-selector"]
                )

            with gr.Column(scale=1):
                with gr.Row():
                    reset_btn = gr.Button("🔄 초기화", variant="secondary", size="sm")
                    solution_btn = gr.Button("💡 정답 보기", variant="secondary", size="sm")

        # 채팅 인터페이스
        chatbot = gr.Chatbot(
            label="SQL Optimization Challenge",
            type="messages",
            height=500,
            show_copy_button=True
        )

        # 문제 설명 (숨김 상태)
        problem_display = gr.Markdown(visible=False)

        # SQL 입력
        with gr.Row():
            sql_input = gr.Code(
                label="✍️ 최적화된 SQL 쿼리를 입력하세요",
                language="sql",
                lines=10,
                elem_classes=["sql-input"]
            )

        # 제출 버튼
        submit_btn = gr.Button("🚀 제출 및 채점", variant="primary", size="lg")

        gr.Markdown("""
---
### 💡 팁
- **CTE(WITH 절)** 사용하여 서브쿼리 재사용
- **중복 JOIN** 제거
- **LEFT JOIN vs INNER JOIN** 올바르게 선택
- **필요한 컬럼만 SELECT**
- **집계 함수** 효율적으로 사용
        """)

        # 이벤트 핸들러
        def on_problem_select(problem_id):
            if problem_id is None:
                return [], gr.update(visible=False), ""
            chat_hist, prob_text, sql = chatbot_instance.select_problem(problem_id)
            return chat_hist, gr.update(value=prob_text, visible=True), sql

        def on_submit(query, chat_history):
            return chatbot_instance.submit_query(query, chat_history)

        def on_reset():
            chat_hist, prob_text, sql = chatbot_instance.reset()
            return chat_hist, gr.update(visible=False), sql, None

        def on_solution(chat_history):
            return chatbot_instance.show_solution(chat_history)

        # 이벤트 연결
        problem_selector.change(
            fn=on_problem_select,
            inputs=[problem_selector],
            outputs=[chatbot, problem_display, sql_input]
        )

        submit_btn.click(
            fn=on_submit,
            inputs=[sql_input, chatbot],
            outputs=[chatbot, sql_input]
        )

        reset_btn.click(
            fn=on_reset,
            outputs=[chatbot, problem_display, sql_input, problem_selector]
        )

        solution_btn.click(
            fn=on_solution,
            inputs=[chatbot],
            outputs=[chatbot]
        )

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
