class Story(object):
    def __init__(self, row):
        self.key = row[1]
        self.summary = row[0]
        self.epic = row[74]

class StoryGroup(object):
    def __init__(self):
        self.epic = ""
        self.stories = []
