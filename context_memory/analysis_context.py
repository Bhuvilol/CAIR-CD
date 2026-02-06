class AnalysisContext:
    """
    Stores the state of the last analytical response
    """
    def __init__(self):
        self.last_result = None
        self.last_query = None

    def update(self, query, result):
        self.last_query = query
        self.last_result = result

    def has_context(self):
        return self.last_result is not None
