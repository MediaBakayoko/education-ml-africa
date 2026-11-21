# Machine Learning for Education Analysis: Dropout Risk and Territorial Inequalities in Africa

## Problématique
Quels facteurs expliquent le risque d'abandon scolaire et les inégalités territoriales et
socioéconomiques d'accès à l'éducation en Afrique ?

## Données
**World Bank EdStats / UNESCO Institute for Statistics (UIS)**, via l'API World Bank Open Data,
accès libre sans inscription.
- Source : https://api.worldbank.org/v2/
- Couverture : 53 pays africains, 2005-2022 (861 observations pays-année)
- Indicateurs : taux de complétion primaire/secondaire, enfants non scolarisés, taux de
  redoublement, dépenses publiques d'éducation (% PIB), alphabétisation adulte/jeunes,
  complétion primaire désagrégée par milieu (rural/urbain) et quintile de richesse

## Objectifs
1. Analyser les tendances de complétion scolaire en Afrique (2005-2022).
2. Identifier les facteurs associés à un risque élevé d'abandon scolaire (classification).
3. Cartographier les inégalités territoriales (urbain/rural) et socioéconomiques (riche/pauvre)
   d'achèvement du primaire.
4. Distinguer clairement le **quintile de richesse** (indicateur relatif utilisé ici uniquement
   pour mesurer l'écart d'accès à l'éducation) du niveau absolu de scolarisation.

## Méthodologie
1. **Construction du panel** (`src/01_build_dataset.py`) : fusion de 11 indicateurs World
   Bank/UIS, plus calcul des écarts urbain-rural et riche-pauvre.
2. **EDA** (`src/02_eda.py`) : tendances temporelles, distributions, corrélations, inégalités.
3. **Classification** (`src/03_classification.py`) : prédiction du risque d'abandon élevé
   (complétion primaire <70%) par Random Forest vs régression logistique.
4. **Analyse des inégalités** (`src/04_inequality_analysis.py`) : classement des pays par écart
   urbain-rural et riche-pauvre d'achèvement du primaire.
5. **Cartographie** (`src/05_mapping.py`) : carte choroplèthe du taux de complétion primaire.

## Résultats clés
- Écart riche-pauvre d'achèvement du primaire allant jusqu'à **71 points de pourcentage**
  (Madagascar), contre moins de 13 points en Afrique du Nord et australe.
- Classification : AUC=0,96 (test) mais échantillon réduit (69 observations avec toutes les
  variables disponibles) et forte variance en validation croisée (std=0,16) — résultat
  informatif mais à interpréter avec prudence (voir Limites).
- Alphabétisation adulte et taux de redoublement sont les facteurs les plus discriminants.
- Carte : gradient net Nord/Sud vs bande sahélienne, Soudan du Sud (29%) et Centrafrique (38%)
  les plus en difficulté, Maroc/Cap-Vert/Seychelles au-dessus de 99%.

## Reproductibilité
```bash
pip install -r requirements.txt
python src/01_build_dataset.py
python src/02_eda.py
python src/03_classification.py
python src/04_inequality_analysis.py
python src/05_mapping.py
```

## Article complet
Voir [`ARTICLE.md`](ARTICLE.md) pour l'analyse narrative complète avec interprétation et
recommandations.

## Auteur
Média Marcel Bakayoko — Expert géomatique / données géospatiales & agricoles / GeoAI / Suivi-Évaluation.

## Licence des données
World Bank Open Data / UNESCO Institute for Statistics — CC BY 4.0.
