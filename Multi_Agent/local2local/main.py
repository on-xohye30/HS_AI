# main.py
import sys
from crewai import Crew
from agents import researcher, writer  # agents.py에서 정의한 에이전트 불러오기
from tasks import research_task, write_task  # tasks.py에서 정의한 작업 불러오기

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# 1. 팀(Crew) 설정
my_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

# 2. 실행 시작
print("### 에이전트 협업 시작 ###")
result = my_crew.kickoff()

# 3. 결과 출력

print("--- 연구원의 조사 결과 ---")
print(research_task.output.raw)

# 2. 작가의 결과(최종본)만 보고 싶을 때
print("--- 작가의 최종 글 ---")
print(write_task.output.raw)

print("\n########## 최종 결과 ##########")
print(result)
