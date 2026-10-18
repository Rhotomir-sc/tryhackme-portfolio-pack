# Repository checks

Run `python tools/check_links.py` from the repository root with Python 3.10+.
The check verifies inline local Markdown paths and balanced code fences. It does not verify external URLs, heading anchors, reference-style links, or the contents of screenshots.

The Portfolio checks workflow runs these checks on pushes and pull requests. Repositories with analysis code also run the relevant automated checks.
Workflow setup follows [GitHub's Python workflow guidance](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

New evidence should state its source, environment, date/timezone when known, observation, and limitation. Keep planned exercises, simulated results, and completed lab work distinct.
