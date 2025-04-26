# Research-Assistant

An AI-powered research assistant that performs multi-step, deep research on any topic by combining web search (via Tavily) and large language model-based agents.

The goal of this repository is to provide a clean and understandable implementation of a deep research agent system using LangChain and LangGraph. It showcases how multiple specialized agents can collaborate to perform credible research, draft structured answers, refine them, and fact-check information.

## How It Works

The system is based on a **multi-agent pipeline**, where each agent specializes in a part of the research and answer development process:

- A **Research Agent** fetches data from the web using Tavily.
- A **Drafting Agent** organizes research into a structured response.
- Depending on the content, either a **Refinement Agent** improves unclear drafts, or a **Fact-Checking Agent** verifies controversial claims.
- Finally, a **Polishing Agent** performs a last refinement pass before delivering the final answer.

The entire agent workflow is orchestrated dynamically using LangGraph.

## Features

- **Online Research**: Gathers fresh web data using Tavily search API.
- **Answer Drafting**: Summarizes and organizes research into clear, professional responses.
- **Refinement and Fact-Checking**: Automatically routes drafts for improvement or fact-checking based on detected needs.
- **Final Polishing**: Every answer is finalized through an editing agent for clarity and professionalism.
- **Dynamic Routing**: Uses LangGraph conditional routing to adapt the workflow based on research content.
- **Streamlit Frontend**: Clean web app interface with chat history and a minimalistic user experience.

## Requirements

- Python 3.10+
- API keys for:
  - Tavily Search API
  - Groq LLM API (or another supported LLM)

## Setup

### Python Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/deep-research-assistant.git
   cd deep-research-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and set your API keys:
   ```
   TAVILY_API_KEY="your_tavily_key"
   GROQ_API_KEY="your_groq_key"
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Docker (Optional)

1. Clone the repository.

2. Create and configure `.env` with your keys.

3. Build and run the Docker container:
   ```bash
   docker build -t deep-research-assistant .
   docker run -p 8501:8501 deep-research-assistant
   ```

## Usage

Once running, the app will:

- Let you enter a research query.
- Automatically:
  - Search for information.
  - Draft an answer.
  - Refine or fact-check the answer as needed.
  - Finalize the output.
- Display the final answer on the main page.
- Store previous queries and answers in the sidebar under "Chat History."

## Agent Architecture

- **ResearchAgent**: Uses Tavily search to gather information.
- **AnswerDrafter**: Converts research into an initial draft.
- **RefinerAgent**: Enhances unclear or incomplete drafts.
- **FactCheckerAgent**: Verifies controversial information based on research.
- **FinalPolishAgent**: Improves overall clarity, structure, and professionalism.
- **Controller (LangGraph)**: Decides whether to refine, fact-check, or finalize the draft based on heuristics.

## System Workflow

1. Research agent fetches online information.
2. Drafting agent organizes findings into a structured answer.
3. Routing logic checks the content:
   - If unclear → Send to RefinerAgent.
   - If controversial → Send to FactCheckerAgent.
   - Otherwise → Proceed.
4. All paths finish with a final polishing step.
5. The final answer is shown in the UI and stored in chat history.

   <img width="549" alt="image" src="https://github.com/user-attachments/assets/e640aafe-a778-4161-9498-85a99d060500" />

   ## Output with Streamlit
   <img width="938" alt="image" src="https://github.com/user-attachments/assets/3cd4ab32-ab42-4db9-8288-7046522a0cb7" />
   

   <img width="920" alt="image" src="https://github.com/user-attachments/assets/b6c4466c-0892-4a5a-b8db-5140b65d822d" />





## To-Do and Improvements

- Add multi-turn conversation or follow-up question capability.
- Support additional LLM backends beyond Groq.
- Implement more fine-grained control over research depth and breadth.

