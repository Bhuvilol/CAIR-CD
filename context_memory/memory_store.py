class ContextMemory:
    def __init__(self):
        self.active_outcome = None
        self.known_signals = set()
        self.used_conversations = set()
        self.query_history = []

    def update_from_task1(self, task1_output, query):
        self.active_outcome = task1_output.get("outcome_event")

        for e in task1_output.get("evidence", []):
            self.known_signals.add(e["signal"])
            self.used_conversations.add(e["conversation_id"])

        self.query_history.append(query)

    def to_dict(self):
        return {
            "active_outcome": self.active_outcome,
            "known_signals": list(self.known_signals),
            "used_conversations": list(self.used_conversations),
            "query_history": self.query_history
        }
