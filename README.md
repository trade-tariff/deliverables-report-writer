# Monthly JIRA report writer

Writes monthly reports based on JIRA CSV data extracts.

## Implementation steps

- Create a virtual environment: `python3 -m venv venv/`.
- Depending on your local python set up, you may need to use the term `python` instead of `python3` and `pip` instead of `pip3`.

## Implementation steps (Windows)

- Activate the virtual environment (Mac): `source venv/bin/activate`.
- Activate the virtual environment (Windows): `.\venv\Scripts\activate`.

## Implementation steps (common)

- Install development Python modules via `pip3 install -r requirements-dev.txt`.

- Install necessary Python modules via `pip3 install -r requirements.txt`.

- Copy the `env.sample` file to `.env` and then populate with required environment variables.

## Environment variable setting

- `governance_folder`

  set to the folder to which reports are to be copied / stored permanently. If this is not set, then the file will not be copied.

- `write_story_points`

  Set to `1` to write a story points column, or `0` (or omit) to not write the story points column.

## Preparation

## JIRA preparation

Make sure that all story titles (summary field) make sense out of context of JIRA, and are gramatically sound.

### JIRA report

- Set up a filter in JIRA, using the JQL statement:

  `project = HOTT AND key > 'HOTT-2100' AND status in (Done) AND labels = ott_report_2023_june ORDER BY Parent ASC, updated DESC, created DESC`

  where the `labels` variable is replaced with an appropriate value for the required month. This lists out all of the stories which have been set to done in the given month period, provided the labels have been set correctly on JIRA.

- Extract a data file from JIRA and save it to the `/resources/jira` folder.

- Save the file with a filename in the format `2306 Sample monthly report (JIRA).csv`, replacing the yymm with the year and month that are relevant.

## JIRA fields of interest

|Column|About|
|-|-|
|0|Summary, i.e. the title of the story|
|1|Issue key (unique ID)|
|81|Parent summary, i.e. the name of the epic to which the story belongs.|

## Usage (Mac)

Execute the application via `python write.py`

## Usage (PC)

Execute the application via `python write.py`

This:

- looks for the latest CSV file in the `/resources/jira` folder.

- writes an equivalent `.docx` Word document to the `report` folder, using the template stored in the `/resources/template` folder.

- copies the file to the destination folder specified in the .env file (`governance_folder` key)

## Theme configuration

- As of September 2023, the content is sorted into themes, e.g. BAU, major incidents, Windsor Framework-related.

- The stucture is now theme > epic > story.

- These themes, and how the epis relate to them are configured in the `config.json` JSON file available in the folder `resources/config`.

- Amend the content of this file to adjust the content (i.e. epics) of each of the themes and the sequence. The lower the priority number, the higher up the resultant document the content is positioned.

### Example configuration

```JSON
{
    "theme_assignments": {
        "Windsor Framework FPO": {
            "priority": 1,
            "epics": [
                "Bulk search POC (Windsor Framework FPOs)",
                "The Windsor Framework - FPO"
            ]
        },
        "Windsor Framework Green Lane": {
            "priority": 2,
            "epics": [
                "Windsor Framework - Green Lanes & interface to TGP (Trader Goods Profile)"
            ]
        },
        "CDS major incidents": {
            "priority": 3,
            "epics": [
                "CDS major incidents"
            ]
        }
    }
}
```