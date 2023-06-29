import classes.globals as g


class Story(object):
    def __init__(self, row):
        self.key = row[g.fields["key"]["actual"]]
        self.summary = row[g.fields["summary"]["actual"]]
        self.epic = row[g.fields["epic"]["actual"]]
        self.story_points = row[g.fields["story_points"]["actual"]].strip()

        self.format_story_points()

    def format_story_points(self):
        if self.story_points != "":
            self.story_points = str(int(float(self.story_points)))

class StoryGroup(object):
    def __init__(self):
        self.epic = ""
        self.stories = []
