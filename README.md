# ads-to-report

Use GoogleAds API to fetch campaigns and keywords then make recommendations based on metrics using algorithm or chatGPT

## Install dependencies
```commandline
pip3 install -r requirements.txt
```

## Create settings.py file in ads-to-report
```python
CLIENT_ID='YOUR_CLIENT_ID'
CLIENT_SECRET='YOUR_CLIENT_SECRET'
DEVELOPER_TOKEN='YOUR_DEVELOPER_TOKEN'
REFRESH_TOKEN='YOUR_REFRESH_TOKEN'

CUSTOMER_ID='YOUR_CUSTOMER_ID'
ACCOUNT_ID=0000000000

OPEN_API_KEY='YOUR_OPEN_API_KEY'
```

## Launch metrics recommendations
```commandline
python3 main.py
```

<br/>

### Conseils pour optimiser les campagnes en fonction de ses métriques

#### Analyser le CTR
Un CTR élevé (> 2% pour la recherche) indique que l'annonce est pertinente. Pour les mots-clés avec un faible CTR, 
il faut envisager de :
- améliorer le texte de l'annonce pour le rendre plus attractif
- vérifier la pertinence du mot-clé par rapport à l'offre
- ajuster le type de correspondance du mot-clé


#### Optimiser le CPC
En comparant le CPC au coût par conversion cible, si le CPC est trop élevé, voici quelques indications : 
- améliorer le Quality Score en travaillant sur la pertinence des annonces et des pages de destination
- ajuster les enchères manuellement ou utiliser des stratégies d'enchères automatiques


#### Améliorer le taux de conversion (faible taux)
- optimiser les pages de destination pour qu'elles correspondent mieux à l'intention de recherche.
- vérifier que l'offre est clairement présentée et attractive
- tester différents appels à l'action (CTA) dans les annonces


#### Réduire le coût par conversion
Pour les mots-clés avec un coût par conversion élevé :
- réduire les enchères pour ces mots-clés
- les mettre en pause s'ils ne sont pas rentables à long terme
- améliorer le parcours de conversion sur let site


#### Maximiser le ROAS (faible < 1 < élevé)
- réévaluer leur pertinence pour l'entreprise.
- ajuster les enchères à la baisse pour améliorer la rentabilité.
- améliorer la valeur moyenne des conversions (upsell, cross-sell).


#### Utiliser des mots-clés à correspondance négative :
- identifier les termes de recherche qui génèrent des clics mais pas de conversions.
- les ajouter en tant que mots-clés négatifs pour éviter de gaspiller du budget.
