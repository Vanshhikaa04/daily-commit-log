# daily-commit-log

A small GitHub Actions bot that keeps this private repo active with 5–9
commits per day, spread out naturally instead of dumped all at once.

## How it works

- `.github/workflows/daily-commits.yml` runs on a schedule every 2 hours.
- On the first run of a UTC day, it rolls a random daily target between 5
  and 9 and stores it in `.state/commit-count.json`.
- Each subsequent run that day appends a timestamped line to
  `activity-log.md` and commits it, until the day's target is reached —
  then it stops committing until the next day.
- Commits are attributed to the repo owner's GitHub noreply email so they
  count toward the profile contribution graph (works even though the repo
  is private, as long as "Include private contributions" is enabled in
  your GitHub profile settings).

## Manual run

You can trigger it on demand from the Actions tab ("Run workflow") or with:

```
gh workflow run daily-commits.yml
```

## Note

This produces cosmetic activity (a padded contribution graph), not real
project work — it's meant to keep a streak alive, not to represent actual
contributions. If you ever show this repo to someone, its commit history
will make that obvious.
