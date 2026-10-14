# CampusFlow Next
## Two-Engineer Campus Resource and Ticket Management System

### 1. Project Overview

CampusFlow Next is a Python command-line application designed to manage campus service requests and tickets. It helps users create and manage tickets, maintain consistent records, search for requests, prioritize outstanding work, and understand the overall workload through reports.

The project is developed through a two-engineer collaboration. Engineer A focuses on ticket validation, workflow rules, and data storage, while Engineer B focuses on search, reporting, queue management, and command-line integration.

Together, both engineers contribute to a more reliable, maintainable, and useful application.

### 2. Problem Statement

Managing campus requests can become difficult when records are incomplete, ticket statuses are inconsistent, or users cannot easily identify urgent requests.

CampusFlow Next addresses these challenges by organizing ticket records, enforcing workflow rules, saving information, and providing tools to find and analyze tickets.

### 3. Project Objectives

- Validate ticket information and prevent invalid records.
- Apply consistent ticket assignment and status-transition rules.
- Store ticket data persistently using JSON.
- Provide search and filtering capabilities.
- Generate reports that summarize tickets and workload.
- Organize open tickets by priority.
- Use automated tests to maintain software quality.
- Demonstrate teamwork, modular programming, documentation, and code review.

### 4. Technologies Used

- **Python 3:** Application logic and command-line interface.
- **JSON:** Local ticket data storage.
- **Python unittest:** Automated testing.
- **Git and GitHub:** Version control and collaborative development.
- **Visual Studio Code:** Development environment.

### 5. Project Architecture

The project is organized into modules with distinct responsibilities.

| File or module | Purpose |
|---|---|
| `main.py` | Starts the application and handles user interaction. |
| `campusflow/tickets.py` | Defines ticket-related data and validation. |
| `campusflow/workflow.py` | Handles assignment and ticket status changes. |
| `campusflow/storage.py` | Loads and saves ticket records. |
| `campusflow/search.py` | Searches for tickets and applies filters. |
| `campusflow/reports.py` | Produces ticket and workload summaries. |
| `campusflow/queue.py` | Organizes open tickets by priority. |
| `campusflow/understanding_check.py` | Provides questions to test engineers' understanding. |
| `tests/` | Contains automated tests for application behavior. |

The final merged repository is the authoritative reference for the actual file names and implemented features.

### 6. Engineer A: Responsibilities and Impact

**Primary responsibility: Data integrity, workflow reliability, and persistence.**

Engineer A is responsible for the foundational rules that keep the ticket system consistent.

#### Responsibilities

1. Validate ticket information before accepting it.
2. Enforce assignment and status-transition rules.
3. Implement follow-up notes where required.
4. Load and save ticket records using JSON.
5. Handle malformed or invalid stored data safely.
6. Write automated tests for validation, workflow, and storage.
7. Document design decisions and communicate shared interfaces to Engineer B.

#### Impact of Engineer A

Engineer A helps ensure that ticket records are trustworthy and that users cannot accidentally perform unsupported operations.

For example, if the application requires a ticket to be assigned before it can move to `in_progress`, Engineer A implements and tests that rule.

This work benefits the entire application because search results, reports, and queues depend on reliable ticket data.

**Key contribution:** Engineer A strengthens the correctness, consistency, and persistence of the system.

### 7. Engineer B: Responsibilities and Impact

**Primary responsibility: Search, reporting, prioritization, and user interaction.**

Engineer B focuses on helping users locate tickets, understand the workload, and decide which requests require attention.

#### Responsibilities

1. Implement ticket search and filtering.
2. Support filters such as title, category, status, and priority where required.
3. Generate reports summarizing tickets and workload.
4. Organize open tickets in a priority-based queue.
5. Integrate these features into the command-line interface.
6. Implement the understanding check where required.
7. Write automated tests for search, reporting, queue ordering, and integration.
8. Coordinate with Engineer A to ensure both modules use compatible data structures and function interfaces.

#### Impact of Engineer B

Engineer B makes ticket information easier to find and act upon.

For example, a user can search for open tickets in a particular category rather than reviewing every ticket individually. A prioritized queue can help users focus on important outstanding work, while reports can provide an overview of ticket distribution and unresolved requests.

**Key contribution:** Engineer B improves the usability, visibility, and decision-making capabilities of the system.

### 8. How Engineer A and Engineer B Work Together

Both engineers have different responsibilities, but their contributions are interconnected.

- Engineer A ensures that ticket records and workflow transitions are reliable.
- Engineer B uses those records to provide useful searches, queues, and reports.
- Both engineers agree on shared data structures, function signatures, and error-handling behavior.
- Each engineer reviews the other's work and tests the combined application.
- Both engineers contribute documentation and explain their work during the final demonstration.

For example, Engineer A ensures that ticket statuses are updated correctly. Engineer B uses those statuses to filter open tickets and calculate report totals.

This division of responsibility reduces unnecessary duplication and supports modular development.

### 9. GitHub Collaboration Workflow

The recommended workflow is:

1. Both engineers begin from the agreed `main` branch.
2. Engineer A creates a feature branch and implements their assigned changes.
3. Engineer B creates a separate feature branch and implements their assigned changes.
4. Each engineer commits their changes and opens a pull request.
5. Each engineer reviews the other's pull request.
6. Both engineers address genuine review feedback.
7. Approved pull requests are merged into `main`.
8. The team runs the complete test suite against the merged code.
9. The team records the actual pull-request links, commit SHA, test results, and demonstration evidence.

Pull requests, reviews, and approvals must be completed and documented in GitHub; they should not be claimed before they actually occur.

### 10. Installation and Execution

#### Requirements

- Python 3 installed.
- Visual Studio Code or another code editor.
- A terminal opened in the project root, where `main.py` is located.

Check the Python installation:

```bash
python3 --version
```

Run the application:

```bash
python3 main.py
```

Run the automated tests:

```bash
python3 -m unittest discover -s tests -v
```

If a virtual environment is needed, create and activate one:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If the repository contains a `requirements.txt` file, install its dependencies inside the activated environment:

```bash
python -m pip install -r requirements.txt
```

### 11. Testing and Quality Assurance

Testing helps ensure that the original functionality continues to work after new features are introduced.

The team should test:

- Valid and invalid ticket creation.
- Assignment and status transitions.
- Saving and loading JSON records.
- Handling malformed stored data.
- Search matching and combined filters.
- Report totals and calculations.
- Open queue contents and priority ordering.
- Command-line integration and error handling.
- Regression cases from the original project.

Both engineers should run the complete test suite after merging. The final test count and results should be reported only after testing the exact version submitted.

### 12. Expected Project Impact

CampusFlow Next is intended to provide the following benefits:

- More consistent recording and updating of campus service requests.
- Fewer errors caused by invalid ticket information or unsupported status changes.
- Persistent records between application runs.
- Faster access to relevant tickets through search and filtering.
- Better prioritization of outstanding work.
- Improved visibility into workload through reports.
- More maintainable software through modular design and automated testing.
- Practical experience with Git branches, pull requests, peer reviews, and collaborative engineering.

These are expected benefits. Actual operational improvements should be assessed through testing, user feedback, and observed usage.

### 13. Limitations and Future Improvements

The current command-line and JSON-based design is suitable for a small project and demonstration. A larger deployment could benefit from:

- A database for concurrent users and larger data volumes.
- Authentication and role-based permissions.
- An audit trail for important ticket changes.
- A web or graphical interface.
- Automated backups and structured logging.
- Continuous integration to run tests automatically.
- Exportable reports and configurable priority rules.

These improvements would require additional implementation and testing.

### 14. Final Submission Checklist

- [ ] Engineer A's changes are integrated.
- [ ] Engineer B's changes are integrated.
- [ ] Both pull requests have been reviewed and merged.
- [ ] The application starts successfully.
- [ ] The complete test suite passes.
- [ ] Both engineers can explain their contributions.
- [ ] Learning logs and bug-hunter reports contain genuine evidence.
- [ ] The final repository URL and commit SHA are recorded where required.
- [ ] Known limitations are documented.

### Conclusion

CampusFlow Next combines dependable ticket management with search, reporting, and prioritization. Engineer A provides the foundation by ensuring that ticket data and workflow rules remain consistent. Engineer B builds on that foundation by making the information easier to locate, understand, and use.

Their combined contributions demonstrate the importance of modular design, data integrity, automated testing, documentation, and collaborative software development.
