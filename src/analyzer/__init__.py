
class Analyzer:
    def __init__(self):
        pass

    @staticmethod
    def _calculate_mean(numbers):
        return sum(numbers) / len(numbers) if numbers else 0


class CampaignAnalyzer(Analyzer):
    def __init__(self, campaign):
        super().__init__()

        self.campaign = campaign
        self.performances = {}
        self.recommendations = []
        self.suggested_keywords = []

    def _suggest_keywords(self):
        suggested = []
        keywords = self.campaign.get('keywords', None)

        if keywords is not None:
            top_keywords = sorted(
                keywords,
                key=lambda k: k['conversions'],
                reverse=True
            )[:5]

            for kw in top_keywords:
                suggested.append(f"{kw['text']} service")
                suggested.append(f"meilleur {kw['text']}")
                suggested.append(f"{kw['text']} professionnel")

                if kw["match_type"] != "EXACT":
                    suggested.append(f"[{kw['text']}]")

            self.suggested_keywords = list(set(suggested))

    def _get_performance(self):
        cost = self.campaign["cost"]
        conversions = self.campaign["conversions"]
        impressions = self.campaign["impressions"]

        self.performances = {
            "total_cost": cost,
            "total_conversions": conversions,
            "conversion_rate": (conversions / impressions) * 100 if impressions > 0 else 0,
            "cost_per_conversion": cost / conversions if conversions > 0 else 0,
            "roas": self.campaign["conversions_value"] / cost if cost > 0 else 0,
            "click_through_rate": self._calculate_mean([kw['click_rate'] for kw in self.campaign["keywords"]]) if self.campaign["keywords"] else 0
        }

    def _get_recommendations(self):
        if self.performances["conversion_rate"] < 1:
            self.recommendations.append(
                "Le taux de conversion est faible. Examinez la pertinence de vos annonces et pages de destination."
            )
        if self.performances["roas"] < 1:
            self.recommendations.append(
                "Le ROAS est inférieur à 1. Réévaluez votre stratégie de tarification et vos enchères."
            )
        if self.performances["click_through_rate"] < 1:
            self.recommendations.append(
                "Le taux de clic est faible. Améliorez le texte de vos annonces pour les rendre plus attrayantes."
            )

        if self.campaign["keywords"]:
            click_rates = [kw["click_rate"] for kw in self.campaign["keywords"]]
            avg_click_rate = self._calculate_mean(click_rates)

            for keyword in self.campaign["keywords"]:
                if keyword["click_rate"] < avg_click_rate / 2:
                    self.recommendations.append(
                        f"Le mot-clé '{keyword['text']}' a un taux de clic faible ({keyword['click_rate']:.2f}%). Envisagez de le revoir ou de le supprimer."
                    )
                if keyword['cost_per_conversion'] > self.performances['cost_per_conversion'] * 1.5:
                    self.recommendations.append(
                        f"Le mot-clé '{keyword['text']}' a un coût par conversion élevé ({keyword['cost_per_conversion']:.2f}). Optimisez-le ou réduisez son enchère."
                    )

    def analyze(self):
        self._get_performance()
        self._get_recommendations()
        self._suggest_keywords()

    def get_report(self):
        return {
            "campaign_name": self.campaign['name'],
            "performances": self.performances,
            "recommendations": self.recommendations,
            "suggested_keywords": self.suggested_keywords
        }


class MetricAnalyser:
    def __init__(self, metrics):
        self.metrics = metrics

    def get_recommendations(self):
        results = []

        for metric in self.metrics:
            campaign = CampaignAnalyzer(metric)
            campaign.analyze()

            results.append(campaign.get_report())
        return results
