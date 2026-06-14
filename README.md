# SmartDesk-AI
AI-Powered Customer Support System using RAG and LLMs


# SmartDesk AI Architecture

SmartDesk AI is an AI-powered customer support platform that combines Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), conversation summarization, sentiment analysis, ticket generation, and email automation.

## High-Level Architecture

```text
Customer
    |
    v
Frontend (React / Next.js)
    |
    v
FastAPI Backend
    |
    +------------------------------------+
    |                                    |
    v                                    |
RAG Pipeline                             |
    |                                    |
    +--> Vector Database (ChromaDB)      |
    |                                    |
    +--> Knowledge Base                  |
          - FAQs                         |
          - Company Policies             |
          - Refund Policies              |
          - Shipping Policies            |
          - Product Documentation        |
          - Support Guides               |
    |                                    |
    +------------------------------------+
                    |
                    v
          Large Language Model
                    |
                    v
            Customer Response

================================================

Conversation History
        |
        v
PostgreSQL Database
        |
        v
Fine-Tuned FLAN-T5
(DialogSum + LoRA/PEFT)
        |
        +--> Conversation Summary
        |
        +--> Sentiment Analysis
        |
        +--> Priority Classification

================================================

Business Logic Layer
        |
        +--> Create Support Ticket
        |
        +--> Generate Ticket ID
        |
        +--> Store Ticket in Database
        |
        +--> Notify Customer Service Team
        |
        +--> Send Confirmation Email to Customer
        |
        +--> Request Customer Feedback
```

---

## Workflow

### Step 1: Customer Interaction

The customer interacts with the chatbot through the web interface.

### Step 2: Retrieval-Augmented Generation (RAG)

The chatbot retrieves relevant information from the company knowledge base:

- FAQs
- Company Policies
- Refund Policies
- Shipping Policies
- Product Documentation
- Support Guides

The retrieved context is injected into the prompt before generating the response.

### Step 3: Conversation Storage

All messages are stored in PostgreSQL for future processing and auditing.

### Step 4: Conversation Analysis

When the conversation ends, a fine-tuned FLAN-T5 model processes the full conversation and generates:

- Conversation Summary
- Customer Sentiment
- Ticket Priority

Example Output:

```json
{
  "summary": "Customer requested a refund for a delayed order.",
  "sentiment": "angry",
  "priority": "high"
}
```

### Step 5: Ticket Creation

If the issue requires human intervention:

- A support ticket is automatically created.
- A unique Ticket ID is generated.
- Ticket information is stored in the database.

### Step 6: Email Automation

#### Customer Service Team

An email is sent containing:

- Ticket ID
- Conversation Summary
- Sentiment
- Priority
- Customer Contact Information

#### Customer

A confirmation email is sent:

```text
Thank you for contacting SmartDesk AI.

Your request has been received successfully.

Ticket ID: SD-2026-001

Our support team will review your request and contact you shortly.
```

### Step 7: Customer Feedback

After the ticket is created, the customer receives a satisfaction survey to evaluate the support experience.

---

## Technology Stack

### AI & Machine Learning

- Large Language Models (GPT / Gemini / Llama)
- FLAN-T5
- LoRA / PEFT
- DialogSum Dataset
- Hugging Face Transformers

### RAG

- ChromaDB
- Sentence Transformers
- Embeddings
- Retrieval-Augmented Generation

### Backend

- FastAPI
- Python

### Database

- PostgreSQL

### Deployment

- Docker
- Docker Compose
- AWS EC2

### Automation

- SMTP Email Service
- Ticket Management System
