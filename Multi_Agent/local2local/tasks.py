from crewai import Task
from agents import researcher, writer

# 조사 작업
research_task = Task(
    description=(
        "2024년 AI 기술 트렌드를 조사하고 요약해줘. "
        "모든 답변은 반드시 자연스러운 한국어로만 작성하고, 꼭 필요할 때만 영어 문장을 사용 해."
    ),
    expected_output=(
        "최소 5가지 핵심 트렌드와 각 트렌드의 간단한 설명이 포함된 한국어 요약 보고서"
    ),
    agent=researcher
)

# 글쓰기 작업
write_task = Task(
    description=(
        "조사된 내용을 바탕으로 일반인도 이해하기 쉬운 블로그 포스팅을 작성해줘. "
        "모든 문장은 한국어로 작성하고, 제목도 한국어로 작성해줘."
    ),
    expected_output=(
        "제목, 본문, 마무리로 구성된 1000자 내외의 쉬운 한국어 블로그 글"
    ),
    agent=writer,
    output_file="ai_trend_blog_post.md"
)
