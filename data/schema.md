# Canonical Conversational Schema

This schema defines the single source of truth for representing conversational
data across notebooks (Google Colab), preprocessing scripts, causal analysis,
and inference-time systems.

---

## Conversation Object

| Field | Type | Description |
|------|------|-------------|
| conversation_id | string | Unique identifier for the conversation |
| domain | string | Business domain (e.g., Banking, Healthcare) |
| intent | string | Primary intent of the interaction |
| outcome_event | string / null | Observed outcome event (e.g., Escalation, Refund) |
| timestamp | string / null | Start time of interaction |
| turns | list | Ordered list of turn objects |

---

## Turn Object

| Field | Type | Description |
|------|------|-------------|
| turn_id | int | Sequential identifier starting from 0 |
| speaker | enum | Either `Agent` or `Customer` |
| text | string | Utterance content |
| position | int | Redundant ordering safeguard |
| timestamp | string / null | Optional timestamp |
| features | dict | Placeholder for extracted signals |

---

## Design Principles

- Outcome events are **conversation-level labels**
- Causal attribution is inferred post hoc
- Turn order must be strictly preserved
- No feature extraction or labeling occurs at ingestion
- Schema is shared between Colab and Python inference code


causal-conversational-reasoning/
│
├── notebooks/                ← Colab-exported notebooks
│   ├── 01_explore.ipynb
│   ├── 02_features.ipynb
│   ├── 03_causal_signals.ipynb
│   └── 04_counterfactuals.ipynb
│
├── artifacts/                ← GENERATED IN COLAB
│   ├── evidence_index.json
│   ├── causal_signals.json
│   ├── counterfactual_rules.json
│   └── model.pkl
│
├── preprocessing/
├── causal_analysis/
├── query_engine/
├── context_memory/
├── app/
├── evaluation/
├── data/
├── requirements.txt
├── README.md
└── LLM_USAGE.md

