#!/bin/bash
# Run all reify encoding problems. Usage: ./run_reify.sh <timeout_seconds>
TIMEOUT="${1:-60}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

collect_results() {
    local start end elapsed result match output exit_code
    local name="$1" expected="$2" left="$3" right="$4" guide="$5" max="$6"
    start=$(date +%s%N)
    output=$(timeout "$TIMEOUT" anthem-cx "$left" "$right" "$guide" --max "$max" 2>&1)
    exit_code=$?
    end=$(date +%s%N)
    if [ "$exit_code" -eq 124 ]; then
        result="-"
        elapsed="timeout"
    else
        elapsed=$(awk "BEGIN{printf \"%.2f\", ($end-$start)/1000000000}")
        if echo "$output" | grep -q "Found a counterexample"; then result="CE"
        elif echo "$output" | grep -q "No counterexample was found"; then result="no-CE"
        else result="error"; fi
    fi
    if [ "$elapsed" = "timeout" ] || [ "$result" = "error" ]; then match="-"
    elif [ "$expected" = "unknown" ]; then match="N/A"
    elif { [ "$expected" = "false" ] && [ "$result" = "CE" ]; } ||
         { [ "$expected" = "true" ] && [ "$result" = "no-CE" ]; }; then match="yes"
    else match="no"; fi
    echo "$name $expected $result $elapsed $match"
}

print_table() {
    local domain="$1"; shift
    local results=("$@")
    echo ""
    echo "## $domain"
    echo ""
    printf "| %-10s | %-10s | %-9s | %8s | %-5s |\n" "Problem" "Expected" "Result" "Runtime" "Match"
    printf "| %s | %s | %s | %s | %s |\n" "----------" "----------" "---------" "--------" "-----"
    local timeouts=0 correct=0 total=0
    for row in "${results[@]}"; do
        read -r name expected result elapsed match <<< "$row"
        if [ "$elapsed" = "timeout" ]; then
            printf "| %-10s | %-10s | %-9s | %8s | %-5s |\n" "$name" "$expected" "$result" "timeout" "$match"
            timeouts=$((timeouts+1))
        else
            printf "| %-10s | %-10s | %-9s | %7ss | %-5s |\n" "$name" "$expected" "$result" "$elapsed" "$match"
        fi
        total=$((total+1))
        [ "$match" = "yes" ] && correct=$((correct+1))
    done
    echo ""
    echo "Summary: $total problems, $timeouts timeouts, $correct correct"
}

# --- noprojection (nop5/nop6/nop7 skipped: reify fallback uses triple/3) ---
NOPROJECTION_RESULTS=()
row=$(collect_results "nop0"  "false"   "$SCRIPT_DIR/noprojection/nop0/Q0a.reify.lp"  "$SCRIPT_DIR/noprojection/nop0/Q0b.reify.lp"  "$SCRIPT_DIR/noprojection/nop0/nop0.reify.ug"   1)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop1"  "false"   "$SCRIPT_DIR/noprojection/nop1/Q1a.reify.lp"  "$SCRIPT_DIR/noprojection/nop1/Q1b.reify.lp"  "$SCRIPT_DIR/noprojection/nop1/nop1.reify.ug"   1)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop2"  "true"    "$SCRIPT_DIR/noprojection/nop2/Q2a.reify.lp"  "$SCRIPT_DIR/noprojection/nop2/Q2b.reify.lp"  "$SCRIPT_DIR/noprojection/nop2/nop2.reify.ug"   3)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop3"  "false"   "$SCRIPT_DIR/noprojection/nop3/Q3a.reify.lp"  "$SCRIPT_DIR/noprojection/nop3/Q3b.reify.lp"  "$SCRIPT_DIR/noprojection/nop3/nop3.reify.ug"   2)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop4"  "false"   "$SCRIPT_DIR/noprojection/nop4/Q4c.reify.lp"  "$SCRIPT_DIR/noprojection/nop4/Q4b.reify.lp"  "$SCRIPT_DIR/noprojection/nop4/nop4.reify.ug"   4)
NOPROJECTION_RESULTS+=("$row")
# skip nop5 (reify fallback)
# skip nop6 (reify fallback)
# skip nop7 (reify fallback)
row=$(collect_results "nop8"  "false"   "$SCRIPT_DIR/noprojection/nop8/Q7a.reify.lp"  "$SCRIPT_DIR/noprojection/nop8/Q7b.reify.lp"  "$SCRIPT_DIR/noprojection/nop8/nop8.reify.ug"  10)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop9"  "false"   "$SCRIPT_DIR/noprojection/nop9/Q8a.reify.lp"  "$SCRIPT_DIR/noprojection/nop9/Q8b.reify.lp"  "$SCRIPT_DIR/noprojection/nop9/nop9.reify.ug"   4)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop10" "false"   "$SCRIPT_DIR/noprojection/nop10/Q9a.reify.lp" "$SCRIPT_DIR/noprojection/nop10/Q9b.reify.lp" "$SCRIPT_DIR/noprojection/nop10/nop10.reify.ug" 3)
NOPROJECTION_RESULTS+=("$row")

# --- projection (p5/p6/p7 skipped: reify fallback uses triple/3) ---
PROJECTION_RESULTS=()
row=$(collect_results "p0"  "false" "$SCRIPT_DIR/projection/p0/Q0a.reify.lp"   "$SCRIPT_DIR/projection/p0/Q0b.reify.lp"   "$SCRIPT_DIR/projection/p0/p0.reify.ug"    1)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p1"  "false"   "$SCRIPT_DIR/projection/p1/Q11a.reify.lp"  "$SCRIPT_DIR/projection/p1/Q11b.reify.lp"  "$SCRIPT_DIR/projection/p1/p1.reify.ug"    1)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p2"  "true"    "$SCRIPT_DIR/projection/p2/Q12a.reify.lp"  "$SCRIPT_DIR/projection/p2/Q12b.reify.lp"  "$SCRIPT_DIR/projection/p2/p2.reify.ug"    3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p3"  "false"   "$SCRIPT_DIR/projection/p3/Q13a.reify.lp"  "$SCRIPT_DIR/projection/p3/Q13b.reify.lp"  "$SCRIPT_DIR/projection/p3/p3.reify.ug"    2)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p4"  "false"   "$SCRIPT_DIR/projection/p4/Q14c.reify.lp"  "$SCRIPT_DIR/projection/p4/Q14b.reify.lp"  "$SCRIPT_DIR/projection/p4/p4.reify.ug"    4)
PROJECTION_RESULTS+=("$row")
# skip p5 (reify fallback)
# skip p6 (reify fallback)
# skip p7 (reify fallback)
row=$(collect_results "p8"  "false"   "$SCRIPT_DIR/projection/p8/Q17a.reify.lp"  "$SCRIPT_DIR/projection/p8/Q17b.reify.lp"  "$SCRIPT_DIR/projection/p8/p8.reify.ug"   11)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p9"  "false"   "$SCRIPT_DIR/projection/p9/Q18a.reify.lp"  "$SCRIPT_DIR/projection/p9/Q18b.reify.lp"  "$SCRIPT_DIR/projection/p9/p9.reify.ug"    4)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p10" "false"   "$SCRIPT_DIR/projection/p10/Q19a.reify.lp" "$SCRIPT_DIR/projection/p10/Q19b.reify.lp" "$SCRIPT_DIR/projection/p10/p10.reify.ug"  3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p11" "false"   "$SCRIPT_DIR/projection/p11/Q19c.reify.lp" "$SCRIPT_DIR/projection/p11/Q19b.reify.lp" "$SCRIPT_DIR/projection/p11/p11.reify.ug"  4)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p12" "false"   "$SCRIPT_DIR/projection/p12/Q20a.reify.lp" "$SCRIPT_DIR/projection/p12/Q20b.reify.lp" "$SCRIPT_DIR/projection/p12/p12.reify.ug"  9)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p13" "false"   "$SCRIPT_DIR/projection/p13/Q21a.reify.lp" "$SCRIPT_DIR/projection/p13/Q21b.reify.lp" "$SCRIPT_DIR/projection/p13/p13.reify.ug"  6)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p14" "false"   "$SCRIPT_DIR/projection/p14/Q22a.reify.lp" "$SCRIPT_DIR/projection/p14/Q22b.reify.lp" "$SCRIPT_DIR/projection/p14/p14.reify.ug"  2)
PROJECTION_RESULTS+=("$row")

# --- rdfs (schema already embedded in Q files) ---
RDFS_RESULTS=()
row=$(collect_results "rdfs0"  "false" "$SCRIPT_DIR/rdfs/rdfs0/Q39a.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs0/Q39c.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs0/rdfs0.reify.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs1"  "false" "$SCRIPT_DIR/rdfs/rdfs1/Q39a.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs1/Q39c.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs1/rdfs1.reify.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs2"  "false" "$SCRIPT_DIR/rdfs/rdfs2/Q39a.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs2/Q39b.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs2/rdfs2.reify.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs3"  "false" "$SCRIPT_DIR/rdfs/rdfs3/Q39b.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs3/Q39c.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs3/rdfs3.reify.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs4"  "false" "$SCRIPT_DIR/rdfs/rdfs4/Q39d.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs4/Q39e.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs4/rdfs4.reify.ug"   3)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs5"  "false" "$SCRIPT_DIR/rdfs/rdfs5/Q40b.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs5/Q40d.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs5/rdfs5.reify.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs6"  "false" "$SCRIPT_DIR/rdfs/rdfs6/Q40e.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs6/Q40b.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs6/rdfs6.reify.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs7"  "false" "$SCRIPT_DIR/rdfs/rdfs7/Q41b.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs7/Q41c.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs7/rdfs7.reify.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs8"  "false" "$SCRIPT_DIR/rdfs/rdfs8/Q41b.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs8/Q41d.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs8/rdfs8.reify.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs9"  "false" "$SCRIPT_DIR/rdfs/rdfs9/Q41c.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs9/Q41d.reify.lp"  "$SCRIPT_DIR/rdfs/rdfs9/rdfs9.reify.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs10" "false" "$SCRIPT_DIR/rdfs/rdfs10/Q41b.reify.lp" "$SCRIPT_DIR/rdfs/rdfs10/Q41a.reify.lp" "$SCRIPT_DIR/rdfs/rdfs10/rdfs10.reify.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs11" "false" "$SCRIPT_DIR/rdfs/rdfs11/Q41e.reify.lp" "$SCRIPT_DIR/rdfs/rdfs11/Q41a.reify.lp" "$SCRIPT_DIR/rdfs/rdfs11/rdfs11.reify.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs12" "false" "$SCRIPT_DIR/rdfs/rdfs12/Q43a.reify.lp" "$SCRIPT_DIR/rdfs/rdfs12/Q43b.reify.lp" "$SCRIPT_DIR/rdfs/rdfs12/rdfs12.reify.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs13" "false" "$SCRIPT_DIR/rdfs/rdfs13/Q43a.reify.lp" "$SCRIPT_DIR/rdfs/rdfs13/Q43c.reify.lp" "$SCRIPT_DIR/rdfs/rdfs13/rdfs13.reify.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs14" "false" "$SCRIPT_DIR/rdfs/rdfs14/Q43b.reify.lp" "$SCRIPT_DIR/rdfs/rdfs14/Q43c.reify.lp" "$SCRIPT_DIR/rdfs/rdfs14/rdfs14.reify.ug" 2)
RDFS_RESULTS+=("$row")

print_table "noprojection" "${NOPROJECTION_RESULTS[@]}"
print_table "projection" "${PROJECTION_RESULTS[@]}"
print_table "rdfs" "${RDFS_RESULTS[@]}"
