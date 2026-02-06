from query_engine.intent_classifier import predict_intent

def handle_followup(query, context):
    intent = predict_intent(query)

    if intent == "FACTOR_IMPORTANCE":
        return {
            "answer": (
                f"The most influential factor appears to be "
                f"'{context.top_factor}', as it recurs most frequently "
                f"before the outcome."
            )
        }

    if intent == "TEMPORAL_PATTERN":
        return {
            "answer": (
                "Escalation typically occurs after repeated unresolved "
                "customer turns and increasing question density."
            )
        }

    if intent == "DOMAIN_COMPARISON":
        return {
            "answer": (
                "The pattern is most prominent in customer-facing "
                "service domains such as retail and healthcare."
            )
        }

    if intent == "COUNTERFACTUAL":
        return context.counterfactual_summary()

    if intent == "SUMMARY":
        return {
            "answer": context.summary()
        }

    return {
        "answer": (
            "This question is outside the supported causal analysis scope. "
            "Try asking about factor importance, temporal patterns, or domains."
        )
    }
