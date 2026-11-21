"""
02_eda.py — Analyse exploratoire des indicateurs d'éducation en Afrique (2005-2022).
Sortie : reports/figures/completion_trend.png, distributions.png, correlation_heatmap.png,
         inequality_scatter.png
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE = os.path.join(os.path.dirname(__file__), "..")
IN_PATH = os.path.join(BASE, "data", "processed", "education_africa_2005_2022.csv")
WEALTH_PATH = os.path.join(BASE, "data", "processed", "inequality_wealth.csv")
FIG_DIR = os.path.join(BASE, "reports", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

NUM_COLS = ["primary_completion", "lower_sec_completion", "repetition_primary",
            "govt_exp_education_gdp", "adult_literacy", "youth_literacy"]


def run():
    df = pd.read_csv(IN_PATH)
    print(f"{df.shape[0]} observations pays-année, {df['country'].nunique()} pays")

    trend = df.groupby("year")["primary_completion"].mean()
    plt.figure(figsize=(8, 5))
    plt.plot(trend.index, trend.values, marker="o", color="darkorange")
    plt.title("Taux de complétion du primaire — moyenne Afrique (2005-2022)")
    plt.xlabel("Année"); plt.ylabel("Taux de complétion (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "completion_trend.png"), dpi=150)
    plt.close()

    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    for ax, col in zip(axes.flat, NUM_COLS):
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color="teal")
        ax.set_title(col)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "distributions.png"), dpi=130)
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.heatmap(df[NUM_COLS].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Corrélations — indicateurs d'éducation (Afrique)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "correlation_heatmap.png"), dpi=150)
    plt.close()

    # Inégalités socioéconomiques : complétion riche vs pauvre
    wealth = pd.read_csv(WEALTH_PATH)
    plt.figure(figsize=(7, 7))
    plt.scatter(wealth["primary_completion_q1"], wealth["primary_completion_q5"], alpha=0.6, color="purple")
    plt.plot([0, 100], [0, 100], "k--", label="Égalité parfaite (Q1=Q5)")
    plt.xlabel("Taux de complétion — quintile le plus pauvre (Q1, %)")
    plt.ylabel("Taux de complétion — quintile le plus riche (Q5, %)")
    plt.title("Inégalités socioéconomiques d'achèvement du primaire")
    plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "inequality_scatter.png"), dpi=150)
    plt.close()

    return df


if __name__ == "__main__":
    run()
