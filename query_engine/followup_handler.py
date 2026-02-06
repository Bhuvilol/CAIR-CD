from query_engine.intent_classifier import predict_intent

def handle_followup(query, context):
    intent, confidence = predict_intent(query)

    meta = {
        "detected_intent": intent,
        "intent_confidence": round(confidence, 3)
    }

    if intent == "FACTOR_IMPORTANCE":
        return {
            "answer": (
                f"The most influential factor appears to be "
                f"'{context.top_factor}', as it recurs most frequently "
                f"before the outcome."
            ),
            **meta
        }

    if intent == "TEMPORAL_PATTERN":
        return {
            "answer": (
                "Escalation typically occurs after repeated unresolved "
                "customer turns and rising question density."
            ),
            **meta
        }

    if intent == "DOMAIN_COMPARISON":
        return {
            "answer": (
                "This pattern is most prominent in customer-facing "
                "domains such as retail and healthcare."
            ),
            **meta
        }

    if intent == "COUNTERFACTUAL":
        return {
            "answer": context.counterfactual_summary(),
            **meta
        }

    if intent == "SUMMARY":
        return {
            "answer": context.summary(),
            **meta
        }

    return {
        "answer": (
            "This question is outside the supported causal analysis scope. "
            "Try asking about factor importance, temporal patterns, or domains."
        ),
        "detected_intent": "UNSUPPORTED",
        "intent_confidence": round(confidence, 3)
    }
