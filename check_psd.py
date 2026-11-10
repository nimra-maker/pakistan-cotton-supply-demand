import pandas as pd

KG_PER_BALE = 217.72  # one 480-lb bale in kilograms


TEXT_COLUMNS = {"Commodity", "Year", "Country", "Unit Description"}


def load(path):
    df = pd.read_csv(path, dtype=str)            # read everything as text first
    df.columns = df.columns.str.strip()          # remove stray spaces in headers
    for c in df.columns:
        if c not in TEXT_COLUMNS:                # turn "2,900" into 2900 and so on
            cleaned = df[c].str.replace(",", "", regex=False).str.strip()
            df[c] = pd.to_numeric(cleaned, errors="coerce")
            if df[c].isna().any():
                print(f"WARNING: some values in '{c}' could not be read as numbers")
    df["Year"] = df["Year"].str.strip()
    return df.sort_values("Year").reset_index(drop=True)


def run_checks(df):
    out = df.copy()
    out["supply_check"] = (out["Beginning Stocks"] + out["Production"]
                           + out["Imports"] - out["Total Supply"])
    out["distribution_check"] = (out["Exports"] + out["Domestic Use"] + out["Loss"]
                                 + out["Ending Stocks"] - out["Total Distribution"])
    out["carryover_check"] = out["Ending Stocks"] - out["Beginning Stocks"].shift(-1)
    out["yield_check"] = out["Production"] * KG_PER_BALE / out["Area Harvested"] - out["Yield"]
    out["stu_check"] = (out["Ending Stocks"] / (out["Exports"] + out["Domestic Use"]) * 100
                        - out["Stocks-To-Use"])
    return out


RULES = {                      # check name: allowed absolute error
    "supply_check": 0,
    "distribution_check": 0,
    "carryover_check": 0,
    "yield_check": 1,          # rounding in the yield column
    "stu_check": 0.01,
}


def report(checked):
    all_ok = True
    for name, tol in RULES.items():
        bad = checked[checked[name].abs() > tol]    # NaN (last row carry-over) is skipped
        if bad.empty:
            print(f"PASS  {name}")
        else:
            all_ok = False
            print(f"FAIL  {name}: check years {list(bad['Year'])}")
    print("\nOVERALL:", "ALL CHECKS PASS" if all_ok else "REVIEW NEEDED")
    return all_ok


def revisions(old, new):
    skip = {"Year", "Commodity", "Country", "Unit Description"}
    cols = [c for c in new.columns if c not in skip and c in old.columns]
    merged = old.merge(new, on="Year", suffixes=("_old", "_new"))
    rows = []
    for c in cols:
        changed = merged[merged[c + "_old"] != merged[c + "_new"]]
        for _, r in changed.iterrows():
            rows.append((r["Year"], c, r[c + "_old"], r[c + "_new"]))
    log = pd.DataFrame(rows, columns=["Year", "Column", "Old", "New"])
    added = sorted(set(new["Year"]) - set(old["Year"]))
    return log, added


if __name__ == "__main__":
    new = load("psd_cotton.csv")                 # latest download
    checked = run_checks(new)
    report(checked)
    checked.to_csv("psd_checked.csv", index=False)

    try:                                         # optional: compare with last month's file
        old = load("psd_cotton_previous.csv")
        log, added = revisions(old, new)
        print(f"\nREVISIONS since previous file: {len(log)} changed values")
        print(log.to_string(index=False) if len(log) else "no changes")
        if added:
            print("New years added:", added)
        log.to_csv("psd_revision_log.csv", index=False)
    except FileNotFoundError:
        print("\n(No previous file found, so no revision log this time.)")
