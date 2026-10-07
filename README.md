# AI-Powered Smart Construction Planning System

## Project Overview

The AI-Powered Smart Construction Planning System is an intelligent
preliminary construction planning application.

It helps users estimate construction cost, material requirements,
construction timeline, budget optimization, conceptual 2D floor plans,
and conceptual 3D building visualization based on project requirements.

The system also provides a construction knowledge assistant using RAG.

## Key Features

- Project requirement collection
- AI-based construction cost prediction
- Material quantity estimation
- Labour and cost breakdown
- Construction timeline estimation
- Estimated completion date
- AI budget scenario optimization
- Conceptual 2D floor plan generation
- Conceptual 3D building visualization
- Construction Knowledge Assistant using RAG
- PDF project report generation
- FastAPI REST API
- LangGraph multi-agent workflow

## Technologies Used

- Python
- Streamlit
- FastAPI
- LangGraph
- Scikit-learn
- Pandas
- NumPy
- Plotly
- Sentence Transformers
- FAISS
- Google Gemini
- ReportLab

## System Architecture

User
↓
Streamlit Application
↓
FastAPI
↓
LangGraph Workflow
↓
Requirement Agent
↓
Cost Agent
↓
Material Agent
↓
Timeline Agent
↓
Planning Agent
↓
Visualization Agent
↓
Budget Optimization Agent
↓
Report Agent

## Machine Learning

A Gradient Boosting based machine learning model is used for
preliminary construction cost prediction.

Input features include:

- Plot area
- Built-up area
- Number of floors
- Bedrooms
- Bathrooms
- Location
- Construction quality
- Material quality
- Parking

Target:

- Total construction cost

## RAG Knowledge Assistant

The system uses a Retrieval-Augmented Generation pipeline:

Documents
→ Chunking
→ Embeddings
→ Similarity Retrieval
→ Relevant Context
→ Gemini
→ Final Answer

The knowledge base contains information related to:

- Site preparation
- Foundation
- Structural work
- Brick and plaster work
- Electrical and plumbing
- Flooring and painting
- Finishing
- Construction cost factors
- Construction safety

## API

FastAPI provides REST endpoints for:

- Complete project analysis
- Cost estimation
- Material estimation
- Timeline estimation
- Floor plan generation
- 3D visualization

Swagger API documentation is available at:

http://127.0.0.1:8000/docs

## Running the Project

### 1. Create virtual environment

```bash
python -m venv venv