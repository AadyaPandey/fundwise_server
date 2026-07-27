# GrantGuard — AI-Powered Multi-Agent Grant Review System

## Overview

**GrantGuard** is a production-oriented AI system that automates the first-pass review of NGO grant applications using a **multi-agent architecture** built with **LangGraph**.

Instead of functioning as a chatbot, GrantGuard simulates the workflow of a human grant review committee by breaking the evaluation process into specialized agents. Each agent has a single responsibility and communicates through structured outputs, making the system modular, explainable, and easy to extend.

The goal is **not** to replace human reviewers, but to provide an intelligent, transparent, and secure recommendation before final approval.

---

# Features

- Multi-Agent AI workflow using LangGraph
- Planner-Worker architecture
- Modular tool execution
- Structured outputs using Pydantic
- Quality evaluation agent
- Hybrid security analysis
- Prompt injection detection
- Policy compliance via Retrieval-Augmented Generation (RAG) _(In Progress)_
- Explainable decision making
- Production-oriented architecture
- Easily extensible tool ecosystem

---

# Problem Statement

Grant applications typically require reviewers to manually verify:

- NGO registration
- Budget feasibility
- Eligibility requirements
- Policy compliance
- Risk factors
- Duplicate submissions
- Security concerns

Manual review is time-consuming, inconsistent, and difficult to scale.

GrantGuard automates this first-pass review while maintaining transparency and allowing human reviewers to make the final decision.

---

# Technology Stack

| Category        | Technology                                         |
| --------------- | -------------------------------------------------- |
| Language        | Python                                             |
| API Framework   | FastAPI _(Planned)_                                |
| Agent Framework | LangGraph                                          |
| LLM Framework   | LangChain                                          |
| LLM             | Gemini 2.5 Flash                                   |
| Data Validation | Pydantic                                           |
| Vector Database | ChromaDB _(Planned)_                               |
| Embeddings      | sentence-transformers/all-MiniLM-L6-v2 _(Planned)_ |
| Retrieval       | LangChain Retriever                                |
| Deployment      | Docker + Cloud _(Planned)_                         |

---

# System Architecture

```text
                    ┌─────────────────────┐
                    │ Grant Application   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Planner Agent     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Worker Agent     │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
 Registration Tool      Budget Tool       Eligibility Tool
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                    Quality Reviewer
                               │
                               ▼
                    Security Reviewer
                     ┌───────────────┐
                     │ Rule Scanner  │
                     └───────┬───────┘
                             │
              Threat Found?──┘
                     │Yes
                     ▼
            Immediate Security Result
                     │
                     │No
                     ▼
              Gemini Security Analysis
                     │
                     ▼
                 Judge Agent
                     │
                     ▼
             Final Recommendation
```

---

# Current Workflow

```text
START

↓

Planner Agent

↓

Worker Agent

↓

Quality Reviewer

↓

Security Reviewer
(Rule Scanner + Gemini)

↓

Judge Agent

↓

END
```

---

# Multi-Agent Design

## Planner Agent

### Responsibility

Determines **what work needs to be performed**.

The Planner never executes tools. It only creates an execution plan.

### Output

```python
ExecutionPlan
```

Each plan contains multiple `PlanStep` objects:

- tool
- reason
- required

---

## Worker Agent

### Responsibility

Executes tools requested by the planner.

Current tools:

- Registration Verification
- Budget Analysis
- Eligibility Check

Upcoming:

- Policy RAG
- Risk Assessment
- Duplicate Detection

Worker never makes decisions.

---

## Quality Reviewer

### Responsibility

Evaluates whether the Worker executed the plan correctly.

Checks:

- Required tools executed
- Missing evidence
- Failed tools
- Coverage score
- Evidence score
- Confidence score

Produces:

```python
QualityReview
```

---

## Security Reviewer

Hybrid security architecture.

### Stage 1

Rule-Based Scanner

Detects:

- Prompt Injection
- Policy Bypass
- Jailbreak Attempts
- Suspicious Instructions

If threats are found, the review stops immediately.

### Stage 2

Gemini Security Analyzer

Performs semantic analysis only when rule-based scanning passes.

Produces:

```python
SecurityReview
```

---

## Judge Agent

Consumes evidence from every previous stage.

Current evidence:

- Registration
- Budget
- Eligibility
- Quality Review
- Security Review

Future evidence:

- Policy Compliance
- Risk Score
- Duplicate Detection

Produces:

```python
GrantDecision
```

Containing:

- decision
- confidence
- reasons
- recommendations
- summary

The Judge is the only component responsible for making the final recommendation.

---

# Folder Structure

```text
GrantGuard/
│
├── agents/
│   ├── planner.py
│   ├── worker.py
│   ├── reviewer.py
│   ├── security_reviewer.py
│   └── judge.py
│
├── graph/
│   ├── state.py
│   └── workflow.py
│
├── models/
│   ├── application.py
│   ├── planner_models.py
│   ├── review_models.py
│   ├── security_models.py
│   ├── judge_models.py
│   └── tool_models.py
│
├── security/
│   ├── scanner.py
│   ├── patterns.py
│   ├── gemini_analyzer.py
│   └── prompts.py
│
├── tools/
│   ├── registration.py
│   ├── eligibility.py
│   ├── budget.py
│   └── policy.py            # Planned
│
├── rag/                     # Planned
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── retriever.py
│   ├── prompts.py
│   └── ingest.py
│
├── policies/
│
├── llm.py
├── config.py
└── app.py
```

---

# Tool Architecture

Every tool follows the same contract.

```text
Planner
    │
    ▼
Worker
    │
    ▼
Tool
    │
    ▼
Structured Result
```

Each tool focuses on producing evidence rather than making approval decisions.

---

# Retrieval-Augmented Generation (RAG)

**Status:** In Progress

The Policy RAG module will allow GrantGuard to evaluate applications against funding policies.

Workflow:

```text
Grant Application
        │
        ▼
Policy Tool
        │
        ▼
Retriever
        │
        ▼
ChromaDB
        │
        ▼
Relevant Policy Chunks
        │
        ▼
Gemini
        │
        ▼
PolicyResult
```

Benefits:

- Prevents hallucinated policy references
- Grounds responses in actual policy documents
- Makes decisions explainable
- Easy to update policies without retraining the model

---

# Security Features

GrantGuard includes a hybrid security pipeline designed to protect against prompt injection attacks.

Rule-Based Detection:

- Ignore previous instructions
- System prompt extraction
- Prompt injection
- Policy bypass
- Suspicious keywords

Semantic Detection:

- Gemini-based contextual analysis
- Social engineering detection
- Hidden malicious intent
- Jailbreak attempts

---

# Current Test Scenarios

The application includes multiple integration scenarios:

- Valid Application
- Registration Failure
- Large Budget Request
- Prompt Injection
- Policy Bypass
- Social Engineering
- Multiple Security Attacks
- Clean Application

Each scenario executes the complete LangGraph workflow.

---

# Design Principles

- Single Responsibility Principle
- Modular Architecture
- Structured Outputs
- Explainable AI
- Security by Design
- Production-Oriented Engineering
- Reusable Components
- Extensible Tool Registry

---

# Project Roadmap

## Phase 1 ✅

- Planner Agent
- Worker Agent
- Registration Tool
- Budget Tool
- Eligibility Tool
- Quality Reviewer
- Hybrid Security Reviewer
- Judge Agent

---

## Phase 2 🚧

- Policy RAG
- ChromaDB
- Vector Embeddings
- Policy Retriever

---

## Phase 3

- Risk Assessment Tool
- Duplicate Detection Tool

---

## Phase 4

- Judge v2
- Evidence-based decision engine

---

## Phase 5

- FastAPI Backend
- REST API
- Authentication
- Logging
- Error Handling

---

## Phase 6

- Frontend Dashboard
- Human Review Interface
- Grant Upload Portal
- Decision Visualization

---

## Phase 7

- PostgreSQL
- Persistent Storage
- User Management
- Audit Logs

---

## Phase 8

- Docker
- CI/CD
- Cloud Deployment
- Monitoring
- Observability
- Metrics
- Production Scaling

---

# Future Enhancements

- OCR for scanned grant documents
- PDF parsing
- Multi-language grant support
- Human-in-the-loop approvals
- Reviewer feedback learning
- Grant similarity search
- Advanced analytics dashboard
- Notification system
- Role-Based Access Control (RBAC)
- Distributed task execution
- Model evaluation and benchmarking

---

# Getting Started

Clone the repository:

```bash
git clone <repository-url>
cd GrantGuard
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

# Vision

GrantGuard aims to demonstrate how modern AI engineering techniques—including multi-agent orchestration, structured outputs, retrieval-augmented generation, security analysis, and explainable decision-making—can be combined to build a reliable, production-ready grant review platform.

The long-term objective is to create an extensible system that assists human reviewers by automating repetitive verification tasks while preserving transparency, accountability, and security throughout the review process.
