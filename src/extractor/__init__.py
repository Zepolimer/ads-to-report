import json
import re
import unicodedata

import pandas as pd


class Extractor:
    COST_RATE = 1000000

    def __init__(self):
        self.campaigns = []
        self.keywords = None

    @staticmethod
    def from_csv(csv):
        df = pd.read_csv(csv, sep=',', header=2, encoding="utf-8")
        return df

    @staticmethod
    def to_json(data):
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def normalize_string(value):
        normalized = unicodedata.normalize("NFKD", value)
        ascii_string = normalized.encode("ASCII", "ignore").decode("ASCII")
        return re.sub(r'[^a-zA-Z0-9\s]', "", ascii_string)

    def get_campaigns(self, csv):
        df = self.from_csv(csv)

        for _, row in df.iterrows():
            campaign_name = row["Campagne"]

            if pd.isna(campaign_name) or campaign_name == '':
                campaign_name = row["État de la campagne"]

            self.campaigns.append({
                "name": campaign_name,
                "avg_cpc": row["CPC moy."],
                "ctr": row["Coût"],
                "clicks": self.normalize_string(row["Clics"]),
                "currency": row["Code de la devise"],
                "cost": row["Coût"],
                "impressions": self.normalize_string(row["Impr."]),
                "optimisation_rate": row.get("Taux d'optimisation", "-"),
                "keywords": []
            })

    def get_keywords(self, csv):
        df = self.from_csv(csv)

        for _, row in df.iterrows():
            campaign_name = row["Campagne"]

            for campaign in self.campaigns:
                if campaign['name'] == campaign_name:
                    campaign['keywords'].append({
                    "keyword": row["Mot clé"],
                    "match_type": row["Type de correspondance"],
                    "impressions": self.normalize_string(row["Impr."]),
                    "clicks": self.normalize_string(row["Clics"]),
                    "cost": row["Coût"],
                    "ctr": row["CTR"],
                    "avg_cpc": row["CPC moy."],
                    "conv_rate": row["Taux de conv."],
                    "conversions": row["Conversions"],
                    "cost_per_conv": row["Coût/conv."],
                })
