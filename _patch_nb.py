import json

path = r"c:\projs\furb\data-science\Untitled1.ipynb"
with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Cell indices from earlier inspection:
#  9 = Phase 1 (Schema Catalog)
# 10 = Phase 2 (LLM Config)
# 11 = Phase 3 (Plan Executor)

changed = 0

# ── Cell 9: fix SAMPLED_COLUMNS ───────────────────────────────────────────────
c9 = nb["cells"][9]
src9 = "".join(c9["source"])
assert "Schema Catalog" in src9, f"Cell 9 sanity check failed: {src9[:80]}"

old9 = 'SAMPLED_COLUMNS = ["ref_area", "measure", "unit_measure", "activity", "sector"]'
new9 = ('SAMPLED_COLUMNS = ["ref_area", "reference_area", "measure", "measure_1",\n'
        '                   "unit_measure", "unit_of_measure", "sector"]')
if old9 in src9:
    src9 = src9.replace(old9, new9)
    dead = ('_CATALOG_PATH   = os.path.join(os.path.dirname(os.path.abspath("__file__")),\n'
            '                               r"c:\\projs\\furb\\data-science\\catalog.json")\n\n')
    src9 = src9.replace(dead, "")
    c9["source"] = [l + "\n" for l in src9.splitlines()]
    print("Cell 9  patched: SAMPLED_COLUMNS")
    changed += 1
else:
    print("Cell 9  SKIP (already updated or pattern differs)")

# ── Cell 10: add Rule 9 ───────────────────────────────────────────────────────
c10 = nb["cells"][10]
src10 = "".join(c10["source"])
assert "LLM Config" in src10, f"Cell 10 sanity check failed: {src10[:80]}"

marker10 = '(NOT "dataset", NOT "file").\n\nChart mark type mapping:'
if marker10 in src10:
    r9 = (
        '(NOT "dataset", NOT "file").\n'
        '9. CRITICAL \u2014 HAVING vs WHERE: HAVING is ONLY for filtering aggregated results\n'
        '   (e.g. HAVING SUM(obs_value) > 100). NEVER use HAVING to filter a plain column\n'
        '   like time_period or ref_area \u2014 that causes "no such column" errors.\n'
        '   When filtering on a non-aggregated column inside a UNION ALL subquery,\n'
        '   include that column in the inner SELECTs and use WHERE in the outer query:\n'
        '   Example: SELECT ref_area, SUM(obs_value) AS total\n'
        '            FROM (SELECT ref_area, obs_value, time_period FROM "t1"\n'
        '                  UNION ALL SELECT ref_area, obs_value, time_period FROM "t2")\n'
        '            WHERE time_period <= 2020\n'
        '            GROUP BY ref_area ORDER BY total DESC LIMIT 10\n'
        '\n'
        'Chart mark type mapping:'
    )
    src10 = src10.replace(marker10, r9)
    c10["source"] = [l + "\n" for l in src10.splitlines()]
    print("Cell 10 patched: Rule 9 added")
    changed += 1
else:
    print("Cell 10 SKIP (already updated or marker differs)")
    idx = src10.find('NOT "file"')
    print("  nearby:", repr(src10[max(0, idx - 20):idx + 100]))

# ── Cell 11: dynamic height ───────────────────────────────────────────────────
c11 = nb["cells"][11]
src11 = "".join(c11["source"])
assert "Plan Executor" in src11, f"Cell 11 sanity check failed: {src11[:80]}"

old11 = '        fig.update_layout(template="plotly_dark", margin=dict(t=50, l=20, r=20, b=20))'
new11 = (
    '        n_cats = df[x].nunique() if (x and x in df.columns) else 1\n'
    '        height = max(500, min(900, 400 + n_cats * 20))\n'
    '        fig.update_layout(template="plotly_dark", height=height,\n'
    '                          margin=dict(t=60, l=60, r=40, b=80))'
)
if old11 in src11:
    src11 = src11.replace(old11, new11)
    c11["source"] = [l + "\n" for l in src11.splitlines()]
    print("Cell 11 patched: dynamic height")
    changed += 1
else:
    print("Cell 11 SKIP (already updated or pattern differs)")
    idx = src11.find("update_layout")
    print("  nearby:", repr(src11[max(0, idx - 20):idx + 100]))

print(f"\nTotal: {changed} cells patched")
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Saved (always writes to preserve cell order).")
