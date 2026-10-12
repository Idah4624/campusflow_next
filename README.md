# CampusFlow — Complete Project README

CampusFlow is a simple, terminal-based campus IT helpdesk application. It lets a user create and track support tickets, assign tickets to staff, update ticket statuses, view an unresolved work queue, and see a basic report.

This is the **combined project for Fredrick Ogbodo and Onuh Idah**. Keep `main.py`, the `campusflow/` package, and the `tests/` folder together in the same project directory.

## Features

- Create support tickets with a title, category, urgency, and number of affected users.
- Calculate ticket priority through the ticket module.
- List all saved tickets.
- Assign tickets to a staff member.
- Change ticket status (`open`, `in_progress`, or `resolved`).
- View the unresolved work queue.
- View ticket totals grouped by status and priority.
- Save tickets to a local JSON file so they can be loaded the next time the app starts.
- Run automated tests using Python's built-in `unittest` module.

## Requirements

- Python 3.10 or newer is recommended.
- Visual Studio Code (VS Code) is recommended but not required.
- No third-party Python packages are required.

## Project structure

```text
CampusFlow_Complete_Merged/
├── main.py
├── README.md
├── tickets.json                 # Created when ticket data is saved
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py               # Ticket creation, validation, and priority
│   ├── workflow.py              # Assignment and status changes
│   ├── queue.py                 # Unresolved work queue
│   ├── reports.py               # Summary report
│   └── storage.py               # Load and save ticket data
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   └── test_storage.py
└── docs/
    ├── design-decisions.md
    └── ai-learning-log.md
```

` tickets.json ` is created by the application when data is saved; it may not exist before the first run. Do not move the individual Python modules out of their folders, because the imports depend on this structure.

## Open the project in VS Code

1. Download and extract the complete CampusFlow ZIP file.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Select the extracted `CampusFlow_Complete_Merged` folder—the folder containing `main.py`.
5. Select **Terminal → New Terminal**.

Make sure the terminal is inside the project folder before running the commands below.

## Run the application

On Linux or macOS, run:

```bash
python3 main.py
```

On Windows, run:

```powershell
python main.py
```

A menu will appear:

```text
====== CAMPUSFLOW HELPDESK ======
1. Create ticket
2. List tickets
3. Assign ticket
4. Change ticket status
5. View work queue
6. View report
7. Save and exit
```

Enter the number of the action you want and follow the prompts. For a new ticket, enter a title, a category (`Network`, `Hardware`, `Software`, or `Other`), urgency (`low`, `medium`, or `high`), and the number of affected users. Choose **7** to save and exit.

## Run the tests

Tests use Python's built-in `unittest` module, so installing a test package is not necessary.

Linux or macOS:

```bash
python3 -m unittest discover -s tests -v
```

Windows:

```powershell
python -m unittest discover -s tests -v
```

A successful test run ends with `OK`. If a test fails, read the failure message and the test name to identify the issue.

## How the modules work together

- **`main.py`** displays the menu, collects input, and connects the modules.
- **`campusflow/tickets.py`** creates and validates ticket information and determines priority.
- **`campusflow/workflow.py`** handles ticket assignment and status changes.
- **`campusflow/queue.py`** prepares the unresolved work queue.
- **`campusflow/reports.py`** builds ticket summaries.
- **`campusflow/storage.py`** loads and saves tickets in JSON format.
- **`tests/`** contains automated checks for the main features.

## Team split

- **Person 1 — Questions 1–5:** Focus on understanding the product, ticket structure and validation, priority calculation, planning, Git workflow, and learning documentation. Main code ownership: `campusflow/tickets.py` and `tests/test_tickets.py`.
- **Person 2 — Questions 6–11:** Focus on testing, review, documentation, and engineering checks. Main code ownership: `campusflow/workflow.py`, `campusflow/queue.py`, `campusflow/reports.py`, and `tests/test_workflow.py`.
- **Shared integration:** `main.py`, `campusflow/storage.py`, `tests/test_storage.py`, and the final combined project should be reviewed and tested together.

Both people should understand how their files connect to the rest of the application. When combining contributions, copy files into the matching folders and avoid replacing `main.py` or shared files unless the team intends to change them.

## Troubleshooting

**`python3: command not found` or `python: command not found`**  
Install Python 3, then reopen the terminal. On Windows, try `python`; on Linux, try `python3`.

**`ModuleNotFoundError: No module named 'campusflow'`**  
Make sure VS Code opened the project folder containing `main.py`, and run the command from that folder—not from inside `tests/` or `campusflow/`.

**The app starts with no tickets**  
That is normal on the first run. Create a ticket and save before exiting.

**Ticket data is not where you expected**  
The application reads and writes `tickets.json` relative to the folder from which you run `main.py`. Run the app from the project root to keep the data file in the project folder.

## Project notes

This is a learning project intended to practise Python modules, input validation, data structures, file persistence, testing, and collaborative development. Review the code and tests as a team so both contributors can explain the decisions and demonstrate the application.
