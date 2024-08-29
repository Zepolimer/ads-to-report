import json
import pandas as pd


class Extractor:
    def __init__(self):
        self.campaigns = {}
        self.keywords = None

    @staticmethod
    def from_csv(csv):
        df = pd.read_csv(csv, sep=',', header=2, encoding='utf-8')
        return df

    @staticmethod
    def to_json(data):
        return json.dumps(data, indent=2, ensure_ascii=False)

    def get_campaigns(self, csv):
        df = self.from_csv(csv)

        for _, row in df.iterrows():
            campaign_name = row['Campagne']

            if pd.isna(campaign_name) or campaign_name == '':
                campaign_name = row["État de la campagne"]

            if campaign_name not in self.campaigns:
                self.campaigns[campaign_name] = {}

            self.campaigns[campaign_name] = {
                'avg_cpc': row["CPC moy."],
                'ctr': row["CTR"],
                'clicks': row["Clics"],
                'currency': row["Code de la devise"],
                'cost': row["Coût"],
                'impressions': row["Impr."],
                "optimisation_rate": row.get("Taux d'optimisation", '-'),
            }

    def get_keywords(self, csv):
        df = self.from_csv(csv)

        for _, row in df.iterrows():
            campaign_name = row['Campagne']

            if campaign_name in self.campaigns:
                if 'keywords' not in self.campaigns[campaign_name]:
                    self.campaigns[campaign_name]['keywords'] = []

                keyword_info = {
                    'keyword': row['Mot clé'],
                    'match_type': row['Type de correspondance'],
                    'impressions': row['Impr.'],
                    'clicks': row['Clics'],
                    'cost': row['Coût'],
                    'ctr': row['CTR'],
                    'avg_cpc': row['CPC moy.'],
                    'conv_rate': row['Taux de conv.'],
                    'conversions': row['Conversions'],
                    'cost_per_conv': row['Coût/conv.']
                }

                self.campaigns[campaign_name]['keywords'].append(keyword_info)