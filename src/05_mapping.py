"""
05_mapping.py — Carte du taux de complétion du primaire par pays africain (dernière année
disponible), pour visualiser les disparités territoriales à l'échelle continentale.

Sortie : reports/maps/primary_completion_map.png, reports/country_summary.csv
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), "..")
IN_PATH = os.path.join(BASE, "data", "processed", "education_africa_2005_2022.csv")
REPORT_DIR = os.path.join(BASE, "reports")
MAP_DIR = os.path.join(REPORT_DIR, "maps")
os.makedirs(MAP_DIR, exist_ok=True)


def run():
    df = pd.read_csv(IN_PATH)
    latest = df.dropna(subset=["primary_completion"]).sort_values("year").groupby("country").last().reset_index()
    latest.to_csv(os.path.join(REPORT_DIR, "country_summary.csv"), index=False)
    print(latest[["country", "year", "primary_completion"]].sort_values("primary_completion").to_string())

    try:
        import geopandas as gpd
        url = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
               "master/geojson/ne_110m_admin_0_countries.geojson")
        world = gpd.read_file(url)
        africa = world[world["CONTINENT"] == "Africa"]
        merged = africa.merge(latest, left_on="ISO_A3", right_on="country", how="left")

        fig, ax = plt.subplots(figsize=(10, 10))
        merged.plot(column="primary_completion", cmap="RdYlGn", legend=True, ax=ax,
                    edgecolor="black", linewidth=0.3, missing_kwds={"color": "lightgrey"},
                    legend_kwds={"label": "Taux de complétion du primaire (%), dernière année", "shrink": 0.6})
        ax.set_title("Taux de complétion du primaire — Afrique (World Bank EdStats)")
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(MAP_DIR, "primary_completion_map.png"), dpi=200, bbox_inches="tight")
        plt.close()
        print(f"Carte sauvegardée : {MAP_DIR}/primary_completion_map.png")
    except Exception as e:
        print(f"Carte non générée ({e}) — tableau country_summary.csv disponible en alternative.")

    return latest


if __name__ == "__main__":
    run()
