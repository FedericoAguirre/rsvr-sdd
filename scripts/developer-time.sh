#!/bin/sh
# developer-time.sh — Analyze git history and output developer activity CSV
#
# Usage: developer-time.sh [-o <output_path>] [--help]
#
# Analyzes the git repository at the current working directory and generates
# a CSV report with columns: Developer, Date, First Commit, Last Commit, Minutes, Journal Minutes, Commits, Files Count, Branches.
#
# Dependencies: git, standard POSIX utilities (awk, sort, uniq, cut)

set -u

OUTPUT_PATH="developer-time.csv"

usage() {
    cat <<'EOF'
Usage: developer-time.sh [-o <output_path>] [--help]

Analyze git history and generate a CSV report of developer activity.

Options:
  -o <path>   Output CSV file path (default: developer-time.csv)
  --help      Print this usage information and exit

Exit codes:
  0   Success
  1   Error — repository issue (not a git repo, no commits)
  2   Error — invalid arguments

Examples:
  developer-time.sh
  developer-time.sh -o /tmp/team-activity.csv
EOF
}

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --help)
            usage
            exit 0
            ;;
        -o)
            if [ -z "${2-}" ]; then
                echo "Error: -o requires a file path argument" >&2
                exit 2
            fi
            OUTPUT_PATH="$2"
            shift 2
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            echo "Usage: developer-time.sh [-o <path>] [--help]" >&2
            exit 2
            ;;
        *)
            echo "Error: Unexpected argument: $1" >&2
            echo "Usage: developer-time.sh [-o <path>] [--help]" >&2
            exit 2
            ;;
    esac
done

# Check if inside a git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: Not a git repository: $(pwd)" >&2
    exit 1
fi

# Check if repository has commits
if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo '"Developer","Date","First Commit","Last Commit",Minutes,"Journal Minutes",Commits,"Files Count",Branches' > "$OUTPUT_PATH"
    echo "Generated: $OUTPUT_PATH (empty repository — no commits found)" >&2
    exit 0
fi

echo "Analyzing git history..." >&2

# Use single git log call combining format and name-only, then pipe through awk.
# Output format from git log:
#   hash|email|name|epoch|datetime
#   file1\nfile2\n...
#   (empty line)
# datetime = YYYY-MM-DDTHH:MM:SS (parsed into date + time in awk)
# Then sort by email|date|epoch and group by email+date.
# Files = distinct file paths per group.
# Branches = distinct branch names per group (queried via git branch --contains).
git log --all --reverse --format="%H|%ae|%an|%at|%ad" --date=format:%Y-%m-%dT%H:%M:%S --name-only \
| awk '
BEGIN {
    FS = "|"
    OFS = "|"
    commit_count = 0
}

# Lines containing commit metadata: hash|email|name|epoch|datetime — starts with hex hash
/^[0-9a-f]{40}\|/ {
    if (commit_count > 0) {
        commits[commit_count, "files"] = file_list
    }
    commit_count++
    commits[commit_count, "hash"] = $1
    commits[commit_count, "email"] = $2
    commits[commit_count, "name"] = $3
    commits[commit_count, "epoch"] = $4
    split($5, dt, "T")
    commits[commit_count, "date"] = dt[1]
    commits[commit_count, "time"] = substr(dt[2], 1, 5)
    file_list = ""
    next
}

# Blank line separator
/^$/ { next }

# File path lines
{
    if (file_list == "") file_list = $0
    else file_list = file_list "," $0
}

END {
    if (commit_count > 0) {
        commits[commit_count, "files"] = file_list
    }

    # Sort commits by email, date, epoch using insertion sort
    for (i = 1; i <= commit_count; i++) {
        for (j = i + 1; j <= commit_count; j++) {
            key_i = commits[i, "email"] "|" commits[i, "date"] "|" sprintf("%012d", commits[i, "epoch"])
            key_j = commits[j, "email"] "|" commits[j, "date"] "|" sprintf("%012d", commits[j, "epoch"])
            if (key_i > key_j) {
                swap(commits, i, j)
            }
        }
    }

    # Group by email+date and output CSV
    # Minutes calculation:
    #   - 1-2 commits: simple (last - first) / 60 (span between saves is work time)
    #   - 3+ commits: detect gaps >= 3600s between consecutive commits.
    #     Each gap splits the work into blocks. Total = sum of block durations.
    #     (The gap separates distinct work sessions with activity on both sides.)
    printf "\"Developer\",\"Date\",\"First Commit\",\"Last Commit\",Minutes,\"Journal Minutes\",Commits,\"Files Count\",Branches\n"
    prev_key = ""
    group_count = 0
    block_start = 0
    block_last = 0
    first_ts = 0
    last_ts = 0
    first_time = ""
    last_time = ""
    total_min = 0
    author_name = ""
    current_date = ""
    file_set = ""
    branch_set = ""
    delete branch_cache

    for (i = 1; i <= commit_count; i++) {
        key = commits[i, "email"] "|" commits[i, "date"]
        ts = commits[i, "epoch"] + 0
        tm = commits[i, "time"]
        files = commits[i, "files"]

        if (key != prev_key) {
            # Finalize previous group
            if (prev_key != "") {
                if (group_count <= 2) {
                    total_min = int((last_ts - first_ts) / 60 + 0.5)
                } else {
                    total_min = int(total_min + (block_last - block_start) / 60 + 0.5)
                }
                if (total_min < 0) total_min = 0
                count = count_distinct(file_set)
                branch_count = count_distinct(branch_set)
                journal_min = int((last_ts - first_ts) / 60 + 0.5)
                if (journal_min < 0) journal_min = 0
                printf "\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,%d,%d,%d\n", author_name, current_date, first_time, last_time, total_min, journal_min, group_count, count, branch_count
            }

            # Start new group
            prev_key = key
            group_count = 1
            block_start = ts
            block_last = ts
            first_ts = ts
            last_ts = ts
            first_time = tm
            last_time = tm
            total_min = 0
            author_name = commits[i, "name"]
            current_date = commits[i, "date"]
            file_set = (files != "" ? files : "")
            branch_set = get_branches(commits[i, "hash"])
        } else {
            group_count++
            if (group_count > 2) {
                if (ts - block_last >= 3600) {
                    total_min += int((block_last - block_start) / 60 + 0.5)
                    block_start = ts
                }
                block_last = ts
            } else {
                if (ts - block_last >= 3600) {
                    total_min += int((block_last - block_start) / 60 + 0.5)
                    block_start = ts
                }
                block_last = ts
            }
            if (ts < first_ts) { first_ts = ts; first_time = tm }
            if (ts > last_ts) { last_ts = ts; last_time = tm }
            if (files != "") {
                if (file_set == "") file_set = files
                else file_set = file_set "," files
            }
            branches_this = get_branches(commits[i, "hash"])
            if (branches_this != "") {
                if (branch_set == "") branch_set = branches_this
                else branch_set = branch_set "," branches_this
            }
        }
    }

    # Output last group
    if (prev_key != "") {
        if (group_count <= 2) {
            total_min = int((last_ts - first_ts) / 60 + 0.5)
        } else {
            total_min = int(total_min + (block_last - block_start) / 60 + 0.5)
        }
        if (total_min < 0) total_min = 0
        count = count_distinct(file_set)
        branch_count = count_distinct(branch_set)
        journal_min = int((last_ts - first_ts) / 60 + 0.5)
        if (journal_min < 0) journal_min = 0
        printf "\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,%d,%d,%d\n", author_name, current_date, first_time, last_time, total_min, journal_min, group_count, count, branch_count
    }
}

function swap(arr, i, j) {
    tmp_hash = arr[i, "hash"]; arr[i, "hash"] = arr[j, "hash"]; arr[j, "hash"] = tmp_hash
    tmp_email = arr[i, "email"]; arr[i, "email"] = arr[j, "email"]; arr[j, "email"] = tmp_email
    tmp_name = arr[i, "name"]; arr[i, "name"] = arr[j, "name"]; arr[j, "name"] = tmp_name
    tmp_epoch = arr[i, "epoch"]; arr[i, "epoch"] = arr[j, "epoch"]; arr[j, "epoch"] = tmp_epoch
    tmp_date = arr[i, "date"]; arr[i, "date"] = arr[j, "date"]; arr[j, "date"] = tmp_date
    tmp_files = arr[i, "files"]; arr[i, "files"] = arr[j, "files"]; arr[j, "files"] = tmp_files
}

function get_branches(hash) {
    if (hash in branch_cache) return branch_cache[hash]
    result = ""
    cmd = "git branch --contains " hash " 2>/dev/null"
    while ((cmd | getline line) > 0) {
        sub(/^\* /, "", line)
        sub(/^  /, "", line)
        gsub(/^ +| +$/, "", line)
        if (line != "" && line != "(" && line !~ /^\(.*\)$/) {
            if (result == "") result = line
            else result = result "," line
        }
    }
    close(cmd)
    branch_cache[hash] = result
    return result
}

function count_distinct(file_str) {
    if (file_str == "") return 0
    n = split(file_str, arr, ",")
    delete seen
    count = 0
    for (k = 1; k <= n; k++) {
        if (arr[k] != "" && !(arr[k] in seen)) {
            seen[arr[k]] = 1
            count++
        }
    }
    return count
}
' > "$OUTPUT_PATH"

echo "Done. CSV written to: $OUTPUT_PATH" >&2
