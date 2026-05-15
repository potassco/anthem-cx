#!/bin/bash
# Run all simple encoding problems. Usage: ./run_simple.sh <timeout_seconds>
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

# --- noprojection ---
NOPROJECTION_RESULTS=()
row=$(collect_results "nop0"  "false"   "$SCRIPT_DIR/noprojection/nop0/Q0a.lp"  "$SCRIPT_DIR/noprojection/nop0/Q0b.lp"  "$SCRIPT_DIR/noprojection/nop0/nop0.ug"   1)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop1"  "false"   "$SCRIPT_DIR/noprojection/nop1/Q1a.lp"  "$SCRIPT_DIR/noprojection/nop1/Q1b.lp"  "$SCRIPT_DIR/noprojection/nop1/nop1.ug"   1)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop2"  "true"    "$SCRIPT_DIR/noprojection/nop2/Q2a.lp"  "$SCRIPT_DIR/noprojection/nop2/Q2b.lp"  "$SCRIPT_DIR/noprojection/nop2/nop2.ug"   3)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop3"  "false"   "$SCRIPT_DIR/noprojection/nop3/Q3a.lp"  "$SCRIPT_DIR/noprojection/nop3/Q3b.lp"  "$SCRIPT_DIR/noprojection/nop3/nop3.ug"   2)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop4"  "false"   "$SCRIPT_DIR/noprojection/nop4/Q4c.lp"  "$SCRIPT_DIR/noprojection/nop4/Q4b.lp"  "$SCRIPT_DIR/noprojection/nop4/nop4.ug"   3)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop5"  "false"   "$SCRIPT_DIR/noprojection/nop5/Q6a.lp"  "$SCRIPT_DIR/noprojection/nop5/Q6b.lp"  "$SCRIPT_DIR/noprojection/nop5/nop5.ug"   3)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop6"  "false"   "$SCRIPT_DIR/noprojection/nop6/Q6a.lp"  "$SCRIPT_DIR/noprojection/nop6/Q6c.lp"  "$SCRIPT_DIR/noprojection/nop6/nop6.ug"   3)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop7"  "false"   "$SCRIPT_DIR/noprojection/nop7/Q6b.lp"  "$SCRIPT_DIR/noprojection/nop7/Q6c.lp"  "$SCRIPT_DIR/noprojection/nop7/nop7.ug"   3)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop8"  "false"   "$SCRIPT_DIR/noprojection/nop8/Q7a.lp"  "$SCRIPT_DIR/noprojection/nop8/Q7b.lp"  "$SCRIPT_DIR/noprojection/nop8/nop8.ug"  10)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop9"  "false"   "$SCRIPT_DIR/noprojection/nop9/Q8a.lp"  "$SCRIPT_DIR/noprojection/nop9/Q8b.lp"  "$SCRIPT_DIR/noprojection/nop9/nop9.ug"   4)
NOPROJECTION_RESULTS+=("$row")
row=$(collect_results "nop10" "false"   "$SCRIPT_DIR/noprojection/nop10/Q9a.lp" "$SCRIPT_DIR/noprojection/nop10/Q9b.lp" "$SCRIPT_DIR/noprojection/nop10/nop10.ug" 3)
NOPROJECTION_RESULTS+=("$row")

# --- projection ---
PROJECTION_RESULTS=()
row=$(collect_results "p0"  "false" "$SCRIPT_DIR/projection/p0/Q0a.lp"   "$SCRIPT_DIR/projection/p0/Q0b.lp"   "$SCRIPT_DIR/projection/p0/p0.ug"    1)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p1"  "false"   "$SCRIPT_DIR/projection/p1/Q11a.lp"  "$SCRIPT_DIR/projection/p1/Q11b.lp"  "$SCRIPT_DIR/projection/p1/p1.ug"    1)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p2"  "true"    "$SCRIPT_DIR/projection/p2/Q12a.lp"  "$SCRIPT_DIR/projection/p2/Q12b.lp"  "$SCRIPT_DIR/projection/p2/p2.ug"    3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p3"  "false"   "$SCRIPT_DIR/projection/p3/Q13a.lp"  "$SCRIPT_DIR/projection/p3/Q13b.lp"  "$SCRIPT_DIR/projection/p3/p3.ug"    2)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p4"  "false"   "$SCRIPT_DIR/projection/p4/Q14c.lp"  "$SCRIPT_DIR/projection/p4/Q14b.lp"  "$SCRIPT_DIR/projection/p4/p4.ug"    3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p5"  "false"   "$SCRIPT_DIR/projection/p5/Q15a.lp"  "$SCRIPT_DIR/projection/p5/Q15b.lp"  "$SCRIPT_DIR/projection/p5/p5.ug"    3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p6"  "false"   "$SCRIPT_DIR/projection/p6/Q16a.lp"  "$SCRIPT_DIR/projection/p6/Q16b.lp"  "$SCRIPT_DIR/projection/p6/p6.ug"    3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p7"  "false"   "$SCRIPT_DIR/projection/p7/Q16a.lp"  "$SCRIPT_DIR/projection/p7/Q16c.lp"  "$SCRIPT_DIR/projection/p7/p7.ug"    3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p8"  "false"   "$SCRIPT_DIR/projection/p8/Q17a.lp"  "$SCRIPT_DIR/projection/p8/Q17b.lp"  "$SCRIPT_DIR/projection/p8/p8.ug"   11)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p9"  "false"   "$SCRIPT_DIR/projection/p9/Q18a.lp"  "$SCRIPT_DIR/projection/p9/Q18b.lp"  "$SCRIPT_DIR/projection/p9/p9.ug"    4)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p10" "false"   "$SCRIPT_DIR/projection/p10/Q19a.lp" "$SCRIPT_DIR/projection/p10/Q19b.lp" "$SCRIPT_DIR/projection/p10/p10.ug"  3)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p11" "false"   "$SCRIPT_DIR/projection/p11/Q19c.lp" "$SCRIPT_DIR/projection/p11/Q19b.lp" "$SCRIPT_DIR/projection/p11/p11.ug"  4)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p12" "false"   "$SCRIPT_DIR/projection/p12/Q20a.lp" "$SCRIPT_DIR/projection/p12/Q20b.lp" "$SCRIPT_DIR/projection/p12/p12.ug"  9)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p13" "false"   "$SCRIPT_DIR/projection/p13/Q21a.lp" "$SCRIPT_DIR/projection/p13/Q21b.lp" "$SCRIPT_DIR/projection/p13/p13.ug"  6)
PROJECTION_RESULTS+=("$row")
row=$(collect_results "p14" "false"   "$SCRIPT_DIR/projection/p14/Q22a.lp" "$SCRIPT_DIR/projection/p14/Q22b.lp" "$SCRIPT_DIR/projection/p14/p14.ug"  2)
PROJECTION_RESULTS+=("$row")

# --- rdfs (schema already embedded in Q files) ---
RDFS_RESULTS=()
row=$(collect_results "rdfs0"  "false" "$SCRIPT_DIR/rdfs/rdfs0/Q39a.lp"  "$SCRIPT_DIR/rdfs/rdfs0/Q39c.lp"  "$SCRIPT_DIR/rdfs/rdfs0/rdfs0.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs1"  "false" "$SCRIPT_DIR/rdfs/rdfs1/Q39a.lp"  "$SCRIPT_DIR/rdfs/rdfs1/Q39c.lp"  "$SCRIPT_DIR/rdfs/rdfs1/rdfs1.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs2"  "false" "$SCRIPT_DIR/rdfs/rdfs2/Q39a.lp"  "$SCRIPT_DIR/rdfs/rdfs2/Q39b.lp"  "$SCRIPT_DIR/rdfs/rdfs2/rdfs2.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs3"  "false" "$SCRIPT_DIR/rdfs/rdfs3/Q39b.lp"  "$SCRIPT_DIR/rdfs/rdfs3/Q39c.lp"  "$SCRIPT_DIR/rdfs/rdfs3/rdfs3.ug"   1)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs4"  "false" "$SCRIPT_DIR/rdfs/rdfs4/Q39d.lp"  "$SCRIPT_DIR/rdfs/rdfs4/Q39e.lp"  "$SCRIPT_DIR/rdfs/rdfs4/rdfs4.ug"   3)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs5"  "false" "$SCRIPT_DIR/rdfs/rdfs5/Q40b.lp"  "$SCRIPT_DIR/rdfs/rdfs5/Q40d.lp"  "$SCRIPT_DIR/rdfs/rdfs5/rdfs5.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs6"  "false" "$SCRIPT_DIR/rdfs/rdfs6/Q40e.lp"  "$SCRIPT_DIR/rdfs/rdfs6/Q40b.lp"  "$SCRIPT_DIR/rdfs/rdfs6/rdfs6.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs7"  "false" "$SCRIPT_DIR/rdfs/rdfs7/Q41b.lp"  "$SCRIPT_DIR/rdfs/rdfs7/Q41c.lp"  "$SCRIPT_DIR/rdfs/rdfs7/rdfs7.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs8"  "false" "$SCRIPT_DIR/rdfs/rdfs8/Q41b.lp"  "$SCRIPT_DIR/rdfs/rdfs8/Q41d.lp"  "$SCRIPT_DIR/rdfs/rdfs8/rdfs8.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs9"  "false" "$SCRIPT_DIR/rdfs/rdfs9/Q41c.lp"  "$SCRIPT_DIR/rdfs/rdfs9/Q41d.lp"  "$SCRIPT_DIR/rdfs/rdfs9/rdfs9.ug"   2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs10" "false" "$SCRIPT_DIR/rdfs/rdfs10/Q41b.lp" "$SCRIPT_DIR/rdfs/rdfs10/Q41a.lp" "$SCRIPT_DIR/rdfs/rdfs10/rdfs10.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs11" "false" "$SCRIPT_DIR/rdfs/rdfs11/Q41e.lp" "$SCRIPT_DIR/rdfs/rdfs11/Q41a.lp" "$SCRIPT_DIR/rdfs/rdfs11/rdfs11.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs12" "false" "$SCRIPT_DIR/rdfs/rdfs12/Q43a.lp" "$SCRIPT_DIR/rdfs/rdfs12/Q43b.lp" "$SCRIPT_DIR/rdfs/rdfs12/rdfs12.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs13" "false" "$SCRIPT_DIR/rdfs/rdfs13/Q43a.lp" "$SCRIPT_DIR/rdfs/rdfs13/Q43c.lp" "$SCRIPT_DIR/rdfs/rdfs13/rdfs13.ug" 2)
RDFS_RESULTS+=("$row")
row=$(collect_results "rdfs14" "false" "$SCRIPT_DIR/rdfs/rdfs14/Q43b.lp" "$SCRIPT_DIR/rdfs/rdfs14/Q43c.lp" "$SCRIPT_DIR/rdfs/rdfs14/rdfs14.ug" 2)
RDFS_RESULTS+=("$row")

print_table "noprojection" "${NOPROJECTION_RESULTS[@]}"
print_table "projection" "${PROJECTION_RESULTS[@]}"
print_table "rdfs" "${RDFS_RESULTS[@]}"
