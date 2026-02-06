# Conversational Dataset Schema

## Conversation Object
| Field | Type | Description |
|-----|----|------------|
| conversation_id | string | Unique identifier for each conversation |
| domain | string | Business domain (e.g., Healthcare, Banking) |
| intent | string | Primary intent of the call |
| outcome_event | string/null | Final outcome (e.g., Escalation, Refund) |
| timestamp | string | Start time of interaction |
| turns | list | Ordered list of dialogue turns |

## Turn Object
| Field | Type | Description |
|-----|----|------------|
| turn_id | int | Sequential identifier starting from 0 |
| speaker | enum | Agent or Customer |
| text | string | Utterance text |
| position | int | Redundant ordering safeguard |
| timestamp | string/null | Optional timestamp |
| features | dict | Placeholder for extracted signals |

## Design Principles
- Outcome events are conversation-level labels
- Causal attribution is inferred post hoc
- Turn order is strictly preserved
- No assumptions about causality at ingestion
