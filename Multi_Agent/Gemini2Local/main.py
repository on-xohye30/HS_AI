# main.py
import sys
import os
import agents
import tasks
from crewai import Crew

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def get_attr(module, name):
    return getattr(module, name, None)


researcher = get_attr(agents, "researcher")
writer = get_attr(agents, "writer")
research_task = get_attr(tasks, "research_task")
write_task = get_attr(tasks, "write_task")

active_agents = [agent for agent in [researcher, writer] if agent is not None]
active_tasks = [task for task in [research_task, write_task] if task is not None]

if not active_agents or not active_tasks:
    raise RuntimeError(
        "유효한 agents/tasks 구성이 없습니다. agents.py와 tasks.py 정의를 확인하세요."
    )

# 1. 팀(Crew) 설정      
my_crew = Crew(
    agents=active_agents,
    tasks=active_tasks,
    verbose=True,
)

# 2. 실행 시작
print("### 에이전트 협업 시작 ###")
demo_query = (
    sys.argv[1]
    if len(sys.argv) > 1
    else os.getenv("DEMO_QUERY", "2024 생성형 AI 트렌드 핵심 변화")
)
print(f"[DEMO QUERY] {demo_query}")
result = my_crew.kickoff(inputs={"demo_query": demo_query})

# 3. 결과 출력
if research_task is not None and getattr(research_task, "output", None) is not None:
    print("--- 연구원의 조사 결과 ---")
    print(research_task.output.raw)

if write_task is not None and getattr(write_task, "output", None) is not None:
    print("--- 작가의 최종 글 ---")
    print(write_task.output.raw)

print("\n########## 최종 결과 ##########")
print(result)
