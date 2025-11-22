# Performance Evaluation — Multi-Agent Publication Reviewer

## Goals
- Measure pipeline robustness and human-in-the-loop latency
- Verify output quality (manual scoring)
- Record failure modes and recovery rates

## Test setup
- Local machine: Intel Core i3, 8GB RAM
- Test repositories: small README-based sample (3 repos)
- Repetitions per test: 10 runs

## Metrics
- Fetch latency (s)
- Tag suggestion time (s)
- Human-in-the-loop average wait time (s)
- Success rate (fraction of runs producing final report)
- Recovery rate (fraction of simulated failures that succeed after retry)

## Example results (to be filled after run)
- fetch_latency_avg: ...
- tags_time_avg: ...
- hitl_wait_avg: ...
- success_rate: ...
- recovery_rate: ...

## Notes
Record command output logs in `outputs/` for reproducibility.