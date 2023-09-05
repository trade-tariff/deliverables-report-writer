import classes.globals as g


class Story(object):
    def __init__(self, row, themes):
        self.key = row[g.fields["key"]["actual"]]
        self.summary = row[g.fields["summary"]["actual"]]
        self.epic = row[g.fields["epic"]["actual"]]
        self.story_points = row[g.fields["story_points"]["actual"]].strip()
        self.themes = themes
        self.get_theme()

        self.format_story_points()

    def get_theme(self):
        if self.epic in self.themes:
            self.theme = self.themes[self.epic]["theme"]
            self.priority = self.themes[self.epic]["priority"]
        else:
            self.theme = "BAU"
            self.priority = 99

    def format_story_points(self):
        if self.story_points != "":
            self.story_points = str(int(float(self.story_points)))


class StoryGroup(object):
    def __init__(self):
        self.epic = ""
        self.theme = ""
        self.stories = []


class StoryTheme(object):
    def __init__(self):
        self.theme = ""
        self.priority = -1
        self.story_groups = []
