# AI Engineer Technical Assignment: Company Assistant Agent

**Goal:**  
Design and implement an *agentic AI system* that acts as a **company assistant**, capable of answering both internal (company-related) and general knowledge queries — a “Company ChatGPT.”

---

## Requirements

### Query Handling

The assistant should:
- Retrieve company information from a **local knowledge base** (Markdown files)  
- Use **internet search** for external or up-to-date details  
- Fall back to its **intrinsic knowledge** when appropriate  

> It should decide automatically which source to use and ask clarifying questions when uncertain.

#### Compliance & Safety

Block or neutralize harmful, inappropriate, or policy-violating queries, following ethical and company guidelines.

### User Interface

- Provide a Command-Line Interface (CLI) for users to interact with the assistant.
- Include clear instructions to install, configure, and run the system on at least one platform (Linux, macOS, or Windows).

### Implementation
- **Programming Language:** Any language may be used, though Python is preferred.
- **Frameworks:** You may use any software or AI framework except for no-code/low-code tools (e.g., n8n).
- **API Access:** You will receive an OpenRouter API key with $5 credit, but you can use your own API keys if you prefer.    

---

## Deliverables

- **Codebase:** Clean, documented, and runnable from the CLI. Better if published in a public Git repository (e.g., GitHub, GitLab). 
- **Documentation:** Includes setup steps, architecture overview, and rationale for design choices.  
- **Demo Scenarios:** Show example interactions for:
  1. A company-related query  
  2. A general knowledge query  
  3. An ambiguous query requiring clarification  
  4. A restricted or harmful query  

---

### Evaluation Criteria

- Design clarity and justification of technical choices  
- Functional correctness and reliability
- Cost-awareness and efficiency  
- Code quality and documentation  

**Notes**
- You are encouraged to explain your reasoning behind any architectural and implementation choices.
- The goal is not only to deliver a working prototype-don't worry, we are not expecting a production-ready system-but mostly to demonstrate your ability to design, justify, and communicate your technical solution effectively

