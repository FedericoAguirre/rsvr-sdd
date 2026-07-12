# Track Developer Invested Time (CSV Export)

## User story

As a project manager, I want a CLI tool that creates a CSV file with developer time tracking data (developer, date, hours worked, created/updated files count), so that I can analyze team productivity across the entire git history.

## Acceptance criteria

Given the repository has commit history, when I run the CLI tool, then a CSV file is generated with columns: Developer, Date, Hours, Files Count.

Given a developer has activity on a specific date, when their commits are analyzed, then "Hours" reflects the time between their first and last commit on that date (first file created/updated to last push).

Given there is a gap of one hour or more between activity blocks on the same date, when the hours are calculated, then each gap is counted separately and summed together.

Given the CSV is generated, when I inspect the "Files Count" column, then it shows the count of created and/or updated files by that developer on that date.

Given the tool runs on a machine with only standard shell utilities, when executed, then it completes without requiring any external dependencies beyond standard shell commands.

## Definition of Done

- [ ] Shell script created and committed to the repository
- [ ] Script accepts no required arguments and defaults to analyzing the full git history
- [ ] Output CSV includes headers: Developer, Date, Hours, Files Count
- [ ] Hours calculation logic handles 1+ hour gaps correctly (sums multiple activity blocks)
- [ ] No external dependencies beyond standard shell/built-in commands
- [ ] Script tested against the current repository and produces valid output
- [ ] Usage documented in a README or inline help (--help flag)
