from crewai import Task
import agents

researcher = getattr(agents, "researcher", None)
writer = getattr(agents, "writer", None)

# 조사 작업
if researcher is None:
    raise RuntimeError("agents.py에 researcher 에이전트가 정의되어 있어야 합니다.")

research_task = Task(
    description=(
        "주제: {demo_query}\n"
        "데모 목적의 최소 호출로 진행해.\n"
        "반드시 web_search를 정확히 1회만 호출해서 외부 정보를 찾고,\n"
        "필요하면 fetch_page를 최대 1회만 호출해.\n"
        "출력은 다음 3줄로만 작성해:\n"
        "1) 핵심 포인트 2개 요약\n"
        "2) 신뢰 가능한 출처 URL 1개\n"
        "3) 1문장 결론"
    ),
    expected_output=(
        "짧은 조사 메모(최대 6문장, URL 1개 포함)"
    ),
    agent=researcher,
)

# 글쓰기 작업
write_task = None
if writer is not None:
    write_task = Task(
        description=(
            "research_task 결과만 사용해서 짧은 데모 문서를 작성해줘. "
            "새로운 외부 검색/사실 추가 금지. "
            "형식: 제목 1줄 + 본문 4~6문장 + 마무리 1문장."
        ),
        expected_output=(
            "간결한 한국어 데모 문서(최대 10문장)"
        ),
        agent=writer,
        context=[research_task],
        output_file="ai_trend_blog_post.md",
    )
