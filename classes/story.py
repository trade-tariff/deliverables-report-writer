import classes.globals as g


class Story(object):
    def __init__(self, row):
        self.key = row[g.fields["key"]["actual"]]
        self.summary = row[g.fields["summary"]["actual"]]
        self.epic = row[g.fields["epic"]["actual"]]

class StoryGroup(object):
    def __init__(self):
        self.epic = ""
        self.stories = []
