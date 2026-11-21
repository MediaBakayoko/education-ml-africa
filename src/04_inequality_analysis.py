"""
04_inequality_analysis.py — Analyse des inégalités territoriales (rural/urbain) et
socioéconomiques (quintile de richesse) d'achèvement scolaire primaire en Afrique.

Sortie : reports/inequality_summary.txt, reports/figures/inequality_by_country.png,
         reports/regional_inequality.csv
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), "..")
URBAN_RURAL_PATH = os.path.join(BASE, "data", "processed", "inequality_urban_rural.csv")
WEALTH_PATH = os.path.join(BASE, "data", "processed", "inequality_wealth.csv")
REPORT_DIR = os.path.join(BASE, "reports")
FIG_DIR = os.path.join(REPORT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def run():
    ur = pd.read_csv(URBAN_RURAL_PATH)
    wealth = pd.read_csv(WEALTH_PATH)

    # Dernière observation disponible par pays pour chaque indicateur
    ur_latest = ur.sort_values("year").groupby("country").last().reset_index()
    wealth_latest = wealth.sort_values("year").groupby("country").last().reset_index()

    summary = ur_latest[["country", "year", "ecart_urbain_rural"]].merge(
        wealth_latest[["country", "ecart_riche_pauvre"]], on="country", how="outer"
    ).sort_values("ecart_riche_pauvre", ascending=False)
    summary.to_csv(os.path.join(REPORT_DIR, "regional_inequality.csv"), index=False)
    print(summary.to_string())

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    top_ur = ur_latest.nlargest(15, "ecart_urbain_rural")
    axes[0].barh(top_ur["country"], top_ur["ecart_urbain_rural"], color="steelblue")
    axes[0].invert_yaxis()
    axes[0].set_title("Écart urbain-rural le plus élevé\n(complétion primaire, points de %)")
    axes[0].set_xlabel("Points de pourcentage (urbain - rural)")

    top_wealth = wealth_latest.nlargest(15, "ecart_riche_pauvre")
    axes[1].barh(top_wealth["country"], top_wealth["ecart_riche_pauvre"], color="darkorange")
    axes[1].invert_yaxis()
    axes[1].set_title("Écart riche-pauvre le plus élevé\n(complétion primaire, points de %)")
    axes[1].set_xlabel("Points de pourcentage (Q5 - Q1)")

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "inequality_by_country.png"), dpi=150)
    plt.close()

    with open(os.path.join(REPORT_DIR, "inequality_summary.txt"), "w", encoding="utf-8") as f:
        f.write("=== Inégalités d'achèvement du primaire en Afrique ===\n\n")
        f.write(f"Écart urbain-rural moyen : {ur_latest['ecart_urbain_rural'].mean():.1f} points\n")
        f.write(f"Écart riche-pauvre moyen : {wealth_latest['ecart_riche_pauvre'].mean():.1f} points\n\n")
        f.write(summary.to_string())

    return summary


if __name__ == "__main__":
    run()
