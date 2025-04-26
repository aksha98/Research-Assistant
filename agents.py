from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from groq_llm import GroqLLM
import traceback

def clean_text(text):
    drop_phrases = [
        "You must log in to", "Sign in to view", "Log in to reply",
        "Sign up", "Register", "Please login", "Join now", "Subscribe"
    ]
    return "\n".join(
        [line for line in text.splitlines() if not any(p.lower() in line.lower() for p in drop_phrases)]
    )

groq_llm = GroqLLM()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
search_tool = TavilySearchResults()

draft_prompt = PromptTemplate(
    input_variables=["research"],
    template="""
You are an expert research assistant.
Using the following research data, write a clear, comprehensive, and professional answer.
Do not explain your process, just provide the final structured answer.

Research:
{research}
"""
)

refiner_prompt = PromptTemplate(
    input_variables=["answer"],
    template="""
You are a professional editor.
Refine the following draft to improve clarity, conciseness, and professionalism.
Only output the final improved version without any extra notes or explanations.

Draft:
{answer}
"""
)

fact_checker_prompt = PromptTemplate(
    input_variables=["answer"],
    template="""
You are a fact-checking expert.
Carefully fact-check the following text. Correct any misinformation if necessary.
Only output the corrected, final version. Do not include commentary or explain changes.

Text:
{answer}
"""
)

drafting_chain = LLMChain(llm=groq_llm, prompt=draft_prompt, memory=memory, verbose=True)
refiner_chain = LLMChain(llm=groq_llm, prompt=refiner_prompt, verbose=True)
fact_checker_chain = LLMChain(llm=groq_llm, prompt=fact_checker_prompt, verbose=True)

def research_agent(query: str) -> str:
    print("Research phase started...")
    try:
        results = search_tool.invoke(query)
        if isinstance(results, list):
            cleaned_results = [
                clean_text(f"{item.get('title', '')}\n{item.get('content', '')}")
                for item in results
            ]
            return "\n\n".join(cleaned_results)
        return clean_text(str(results))
    except Exception as e:
        print(f"Error during research: {e}")
        traceback.print_exc()
        return "Error: Research failed"

def answer_drafting_agent(research: str) -> str:
    print("Drafting the answer...")
    try:
        result = drafting_chain.invoke({"research": research})
        return result["text"]
    except Exception as e:
        print(f"Error during drafting: {e}")
        traceback.print_exc()
        return "Error: Drafting failed"

def refine_agent(answer: str) -> str:
    print("Refining the draft...")
    try:
        result = refiner_chain.invoke({"answer": answer})
        return result["text"]
    except Exception as e:
        print(f"Error during refinement: {e}")
        traceback.print_exc()
        return "Error: Refining failed"

def fact_checker_agent(answer: str) -> str:
    print("Fact-checking the answer...")
    try:
        result = fact_checker_chain.invoke({"answer": answer})
        return result["text"]
    except Exception as e:
        print(f"Error during fact-checking: {e}")
        traceback.print_exc()
        return "Error: Fact-checking failed"
