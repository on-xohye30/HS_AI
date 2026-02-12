import os
from crewai import Agent, LLM
from external_tools import fetch_page, web_search

# 역할 분담:
# - researcher: Gemini + 외부 검색/데이터 수집 전담
# - writer: Ollama + 데이터 정리/글쓰기 전담
google_api_key = os.getenv("GOOGLE_API_KEY", "Gemini_API_KEY")
raw_gemini_model = os.getenv("GEMINI_MODEL", "models/gemini-3-flash-preview")
local_model_name = os.getenv("LOCAL_LLM_MODEL", "mistral:latest")


def _normalize_gemini_model(model_name: str) -> str:
    if model_name.startswith("gemini/"):
        return model_name
    if model_name.startswith("models/"):
        return f"gemini/{model_name.split('/', 1)[1]}"
    return f"gemini/{model_name}"


gemini_model = _normalize_gemini_model(raw_gemini_model)

gemini_llm = LLM(
    model=gemini_model,
    api_key=google_api_key,
    temperature=0.2,
)

local_llm = LLM(
    model=f"ollama/{local_model_name}",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.3,
)

researcher = Agent(
    role="외부 정보 리서처",
    goal="웹에서 신뢰 가능한 최신 정보를 수집하고 근거를 정리한다.",
    backstory="당신은 검색과 원문 검증에 특화된 리서치 에이전트입니다.",
    llm=gemini_llm,
    tools=[web_search, fetch_page],
    allow_delegation=False,
    max_iter=3,
    verbose=True,
)

writer = Agent(
    role="콘텐츠 정리/작성 에디터",
    goal="수집된 자료를 구조화하고 읽기 쉬운 문서로 작성한다.",
    backstory="당신은 주어진 데이터만 바탕으로 명확한 글을 작성하는 편집 전문가입니다.",
    llm=local_llm,
    allow_delegation=False,
    max_iter=2,
    verbose=True,
)
