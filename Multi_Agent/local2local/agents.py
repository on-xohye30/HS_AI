import os
from crewai import Agent, LLM

# provider selection:
# - RESEARCHER_PROVIDER=local (default) or gemini
# - LOCAL_LLM_MODEL default: mistral:latest
# - GEMINI_MODEL default: gemini/gemini-2.0-flash
google_api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyA2JfDBTpXP3aylhgU2kXjnZcDBJMHD2tk")
gemini_model = os.getenv("GEMINI_MODEL", "gemini/gemini-1.5-flash")
local_model_name = os.getenv("LOCAL_LLM_MODEL", "mistral:latest")
researcher_provider = os.getenv("RESEARCHER_PROVIDER", "local").lower()

gemini_llm = LLM(
    model=gemini_model,
    api_key=google_api_key,
    temperature=0.5,
)

local_llm = LLM(
    model=f"ollama/{local_model_name}",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.5,
)

researcher_llm = local_llm if researcher_provider == "local" else gemini_llm
writer_llm = gemini_llm if researcher_provider == "local" else local_llm

researcher = Agent(
    role="보안 분석 전문가",
    goal="최신 제로데이 취약점을 분석하라",
    backstory="당신은 복잡한 보안 위협을 분석하는 데 특화된 AI입니다.",
    llm=researcher_llm,
    verbose=True,
)

writer = Agent(
    role="기술 블로그 작가",
    goal="어려운 기술 내용을 일반인도 이해하기 쉽게 설명하라",
    backstory="복잡한 기술 정보를 친절하고 구조적으로 전달하는 글쓰기 전문가입니다.",
    llm=writer_llm,
    verbose=True,
)
