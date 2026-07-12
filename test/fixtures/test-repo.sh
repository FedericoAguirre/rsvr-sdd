#!/bin/sh
# test-repo.sh — Create controlled test repos for validating developer-time.sh
#
# Each test creates a temp git repo with known commit timestamps, runs
# developer-time.sh inside it, and compares output against expected CSV.
# Exits 0 if all pass, 1 if any fail.

set -u

SCRIPT="$(cd "$(dirname "$0")/../.." && pwd)/scripts/developer-time.sh"
DATE="2026-07-11"
HDR='"Developer","Date","First Commit","Last Commit",Minutes,"Journal Minutes",Commits,"Files Count"'

pass=0; fail=0

check() {
    if [ "$1" = "$2" ]; then
        echo "PASS: $3"; pass=$((pass+1))
    else
        echo "FAIL: $3"
        echo "  expected: $1"
        echo "  actual:   $2"
        fail=$((fail+1))
    fi
}

# Test 1: Empty repo — header only
echo "=== Empty repo ==="
d=$(mktemp -d); (cd "$d" && git init -q && $SCRIPT -o "$d/out.csv" >/dev/null 2>&1)
check "$HDR" "$(cat "$d/out.csv")" "header only"
rm -rf "$d"

# Test 2: Single commit — 0 min, 1 file, same time
echo "=== Single commit ==="
d=$(mktemp -d); (cd "$d" && git init -q && git config user.email "t@t.com" && git config user.name "Test Dev" && echo "x" > f && git add f && GIT_AUTHOR_DATE="2026-07-11T09:00:00" GIT_COMMITTER_DATE="2026-07-11T09:00:00" git commit -q -m "c1" && $SCRIPT -o "$d/out.csv" >/dev/null 2>&1)
ROW='"Test Dev","'"$DATE"'","09:00","09:00",0,0,1,1'
check "$ROW" "$(sed -n '2p' "$d/out.csv")" "single commit"
rm -rf "$d"

# Test 3: Two commits 2.5h apart — span = 2.50h
echo "=== Two commits ==="
d=$(mktemp -d); (cd "$d" && git init -q && git config user.email "t@t.com" && git config user.name "Test Dev" && echo "1" > a && git add a && GIT_AUTHOR_DATE="2026-07-11T09:00:00" GIT_COMMITTER_DATE="2026-07-11T09:00:00" git commit -q -m "c1" && echo "2" >> a && git add a && GIT_AUTHOR_DATE="2026-07-11T11:30:00" GIT_COMMITTER_DATE="2026-07-11T11:30:00" git commit -q -m "c2" && $SCRIPT -o "$d/out.csv" >/dev/null 2>&1)
ROW='"Test Dev","'"$DATE"'","09:00","11:30",150,150,2,1'
check "$ROW" "$(sed -n '2p' "$d/out.csv")" "two commits span"
rm -rf "$d"

# Test 4: 4 commits with 2h gap — two blocks, sum to 1.0h
echo "=== Gap detection ==="
d=$(mktemp -d); (cd "$d" && git init -q && git config user.email "t@t.com" && git config user.name "Test Dev" && echo "1" > a && git add a && GIT_AUTHOR_DATE="2026-07-11T09:00:00" GIT_COMMITTER_DATE="2026-07-11T09:00:00" git commit -q -m "c1" && echo "2" >> a && git add a && GIT_AUTHOR_DATE="2026-07-11T09:30:00" GIT_COMMITTER_DATE="2026-07-11T09:30:00" git commit -q -m "c2" && echo "1" > b && git add b && GIT_AUTHOR_DATE="2026-07-11T11:30:00" GIT_COMMITTER_DATE="2026-07-11T11:30:00" git commit -q -m "c3" && echo "2" >> b && git add b && GIT_AUTHOR_DATE="2026-07-11T12:00:00" GIT_COMMITTER_DATE="2026-07-11T12:00:00" git commit -q -m "c4" && $SCRIPT -o "$d/out.csv" >/dev/null 2>&1)
ROW='"Test Dev","'"$DATE"'","09:00","12:00",60,180,4,2'
check "$ROW" "$(sed -n '2p' "$d/out.csv")" "gap detection"
rm -rf "$d"

# Test 5: Same file modified 3x — distinct count = 1
echo "=== Distinct files ==="
d=$(mktemp -d); (cd "$d" && git init -q && git config user.email "t@t.com" && git config user.name "Test Dev" && echo "1" > s && git add s && GIT_AUTHOR_DATE="2026-07-11T09:00:00" GIT_COMMITTER_DATE="2026-07-11T09:00:00" git commit -q -m "c1" && echo "2" >> s && git add s && GIT_AUTHOR_DATE="2026-07-11T09:30:00" GIT_COMMITTER_DATE="2026-07-11T09:30:00" git commit -q -m "c2" && echo "3" >> s && git add s && GIT_AUTHOR_DATE="2026-07-11T10:00:00" GIT_COMMITTER_DATE="2026-07-11T10:00:00" git commit -q -m "c3" && $SCRIPT -o "$d/out.csv" >/dev/null 2>&1)
ROW='"Test Dev","'"$DATE"'","09:00","10:00",60,60,3,1'
check "$ROW" "$(sed -n '2p' "$d/out.csv")" "distinct files count"
rm -rf "$d"

# Test 6: --help flag
echo "=== Help flag ==="
if $SCRIPT --help 2>&1 | grep -q "Usage:"; then
    echo "PASS: help flag"
    pass=$((pass+1))
else
    echo "FAIL: help flag"
    fail=$((fail+1))
fi

echo ""
echo "=== $pass passed, $fail failed ==="
exit $fail
