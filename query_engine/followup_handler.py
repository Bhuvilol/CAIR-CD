def handle_followup(query, context):
    """
    Handles follow-up questions using stored context
    """
    if not context.has_context():
        return {"error": "No prior context available"}

    q = query.lower()
    last = context.last_result

    if "most important" in q or "matters most" in q:
        factors = last.get("causal_factors", [])
        if not factors:
            return {"answer": "No dominant causal factor identified."}

        return {
            "answer": f"The most influential factor appears to be '{factors[0]}', "
                      f"as it recurs frequently before the outcome."
        }

    if "confidence" in q:
        ml = last.get("ml_prediction", {})
        return {
            "answer": f"The model predicts this outcome with confidence "
                      f"{ml.get('confidence', 'unknown')}."
        }

    return {"answer": "Follow-up question not understood."}
