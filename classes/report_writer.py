import csv
import os
import shutil
import csv
import sys
from dotenv import load_dotenv
from docx import Document
from docx.shared import Cm
from docx.enum.section import WD_ORIENT
from docx.oxml.shared import OxmlElement, qn
from datetime import datetime
from dateutil.relativedelta import relativedelta

from classes.story import Story, StoryGroup


class ReportWriter(object):
    def __init__(self):
        self.get_date_string()
        self.get_config()
        self.get_latest_csv()
        self.read_csv()
        self.group_stories()

    def get_date_string(self):
        d = datetime.now()
        day = int(d.strftime("%d"))
        month = int(d.strftime("%-m"))
        if day < 15:
            d = d - relativedelta(months=1)
        self.year = d.strftime("%y")
        self.month = d.strftime("%m")
        self.month_name = d.strftime("%b")

    def get_config(self):
        self.resources_folder = os.path.join(os.getcwd(), "resources")
        self.csv_folder = os.path.join(self.resources_folder, "csv")
        self.report_folder = os.path.join(self.resources_folder, "report")
        self.template_folder = os.path.join(self.resources_folder, "template")
        self.stories = []

        self.template_filename = os.path.join(self.template_folder, "report_template.docx")
        self.report_filename = os.path.join(self.report_folder, "OTT Monthly Deliverables {year}-{month}.docx".format(
            year=self.year,
            month=self.month,
        ))
        self.title = "OTT Monthly Deliverables {month} {year}".format(
            year=self.year,
            month=self.month_name,
        )

    def read_csv(self):
        with open(self.csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    story = Story(row)
                    self.stories.append(story)
                    # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                    line_count += 1
            print(f'Processed {line_count} lines.')

    def group_stories(self):
        self.story_groups = []
        previous_epic = "dummy"
        story_group = StoryGroup()

        if (len(self.stories)) > 0:
            for story in self.stories:
                if story.epic != previous_epic:
                    if len(story_group.stories) > 0:
                        self.story_groups.append(story_group)
                    story_group = StoryGroup()
                    story_group.epic = story.epic
                    story_group.stories.append(story)
                else:
                    story_group.stories.append(story)

                previous_epic = story.epic

        story_group.epic = story.epic
        self.story_groups.append(story_group)
        a = 1

    def set_repeat_table_header(self, row):
        """ set repeat table row on every new page
        """
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        tblHeader = OxmlElement('w:tblHeader')
        tblHeader.set(qn('w:val'), "true")
        trPr.append(tblHeader)
        return row

    def write(self):
        self.document = Document(self.template_filename)
        self.document.add_heading(self.title, 0)

        for story_group in self.story_groups:
            self.document.add_heading(story_group.epic, 1)
            table = self.document.add_table(rows=len(story_group.stories) + 1, cols=2)
            table.style = "List Table 3"
            widths = (Cm(2.5), Cm(13.5))
            for row in table.rows:
                for idx, width in enumerate(widths):
                    row.cells[idx].width = width

            self.set_repeat_table_header(table.rows[0])
            hdr_cells = table.rows[0].cells
            headers = ["Story", "Description"]
            for i in range(0, len(headers)):
                hdr_cells[i].text = headers[i]

            row_count = 1
            for story in story_group.stories:
                hdr_cells = table.rows[row_count].cells
                hdr_cells[0].text = str(story.key)
                hdr_cells[1].text = str(story.summary)

                row_count += 1

        self.document.save(self.report_filename)
        self.copy_to_governance_folder()

    def copy_to_governance_folder(self):
        load_dotenv('.env')
        filename = os.path.basename(self.report_filename)
        self.governance_folder = os.getenv('governance_folder')
        dest = os.path.join(self.governance_folder, filename)
        shutil.copy(self.report_filename, self.governance_folder)

    def get_latest_csv(self):
        files = os.listdir(self.csv_folder)
        paths = [os.path.join(self.csv_folder, basename) for basename in files]
        self.csv_file = max(paths, key=os.path.getctime)
