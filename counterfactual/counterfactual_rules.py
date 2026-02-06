COUNTERFACTUAL_RULES = {
    "high_question_ratio": {
        "intervention": "Agent proactively clarifies constraints and provides a single consolidated response.",
        "expected_change": "Reduce back-and-forth questioning.",
        "estimated_effect": "Lower escalation likelihood."
    },
    "customer_last_turn": {
        "intervention": "Agent de-escalates with empathy and proposes a concrete resolution before customer ends the call.",
        "expected_change": "Customer does not end on a frustrated turn.",
        "estimated_effect": "Lower escalation likelihood."
    },
    "long_silence": {
        "intervention": "Agent responds within SLA (e.g., <30 seconds).",
        "expected_change": "Reduced perceived neglect.",
        "estimated_effect": "Lower escalation likelihood."
    }
}
