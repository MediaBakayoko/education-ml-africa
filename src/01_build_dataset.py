"""
01_build_dataset.py — Construit le panel pays-année des indicateurs d'éducation pour l'Afrique
(World Bank EdStats / UIS), couvrant complétion primaire/secondaire, abandon, répétition,
dépenses publiques, littératie et disparités rural/urbain et riche/pauvre.

Source : World Bank Open Data API, accès libre sans inscription.
    https://api.worldbank.org/v2/country/all/indicator/<CODE>?format=json

Sortie : data/processed/education_africa_full.csv, education_africa_2005_2022.csv,
         data/processed/inequality_urban_rural.csv, inequality_wealth.csv
"""
import os
import json
import requests
import pandas as pd
from functools import reduce

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

INDICATORS = {
    "primary_completion": "SE.PRM.CMPT.ZS",
    "lower_sec_completion": "SE.SEC.CMPT.LO.ZS",
    "out_of_school_primary": "SE.PRM.UNER",
    "repetition_primary": "UIS.REPR.1",
    "govt_exp_education_gdp": "SE.XPD.TOTL.GD.ZS",
    "adult_literacy": "SE.ADT.LITR.ZS",
    "youth_literacy": "SE.ADT.1524.LT.ZS",
    "primary_completion_rural": "UIS.CR.1.RUR",
    "primary_completion_urban": "UIS.CR.1.URB",
    "primary_completion_q1": "UIS.CR.1.Q1",
    "primary_completion_q5": "UIS.CR.1.Q5",
}
NORTH_AFRICA_NAMES = {"Algeria", "Egypt, Arab Rep.", "Libya", "Morocco", "Tunisia"}


def fetch_wb(code, per_page=20000):
    all_data, page = [], 1
    while True:
        url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page={per_page}&page={page}"
        r = requests.get(url, timeout=60)
        data = r.json()
        if len(data) < 2 or not data[1]:
            break
        all_data.extend(data[1])
        if page >= data[0]["pages"]:
            break
        page += 1
    return all_data


def get_africa_iso3():
    r = requests.get("https://api.worldbank.org/v2/country?format=json&per_page=400", timeout=60)
    countries = r.json()[1]
    ssa = {c["id"] for c in countries if c["region"]["value"].strip() == "Sub-Saharan Africa"}
    na = {c["id"] for c in countries if c["name"] in NORTH_AFRICA_NAMES}
    return ssa | na


def load_or_fetch(key, code, force=False):
    path = os.path.join(RAW_DIR, f"{key}.json")
    if not os.path.exists(path) or force:
        print(f"Téléchargement {key} ({code})...")
        data = fetch_wb(code)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def to_df(records, value_name, africa_iso3):
    rows = [
        {"country": r["countryiso3code"], "year": int(r["date"]), value_name: r["value"]}
        for r in records
        if r.get("countryiso3code") in africa_iso3 and r.get("value") is not None
    ]
    return pd.DataFrame(rows)


def build():
    africa_iso3 = get_africa_iso3()
    dfs = []
    for key, code in INDICATORS.items():
        records = load_or_fetch(key, code)
        dfs.append(to_df(records, key, africa_iso3))

    merged = reduce(lambda a, b: pd.merge(a, b, on=["country", "year"], how="outer"), dfs)
    merged.to_csv(os.path.join(OUT_DIR, "education_africa_full.csv"), index=False)

    subset = merged[(merged["year"] >= 2005) & (merged["year"] <= 2022)].copy()
    subset.to_csv(os.path.join(OUT_DIR, "education_africa_2005_2022.csv"), index=False)

    # Indicateurs d'inégalité territoriale et socioéconomique
    ineq = merged.dropna(subset=["primary_completion_rural", "primary_completion_urban"]).copy()
    ineq["ecart_urbain_rural"] = ineq["primary_completion_urban"] - ineq["primary_completion_rural"]
    ineq.to_csv(os.path.join(OUT_DIR, "inequality_urban_rural.csv"), index=False)

    wealth = merged.dropna(subset=["primary_completion_q1", "primary_completion_q5"]).copy()
    wealth["ecart_riche_pauvre"] = wealth["primary_completion_q5"] - wealth["primary_completion_q1"]
    wealth.to_csv(os.path.join(OUT_DIR, "inequality_wealth.csv"), index=False)

    print(f"Panel complet : {merged.shape[0]} lignes, {merged['country'].nunique()} pays")
    print(f"Panel 2005-2022 : {subset.shape[0]} lignes")
    return merged, subset, ineq, wealth


if __name__ == "__main__":
    build()
