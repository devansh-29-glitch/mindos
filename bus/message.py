class Message:
    def __init__(self, topic, payload, source=None):
        self.topic = topic
        self.payload = payload
        self.source = source
