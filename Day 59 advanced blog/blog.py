class Blog:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.subtitle = data['subtitle']
        self.body = data['body']
        