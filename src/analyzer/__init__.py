

class MetricAnalyser:
    def __init__(self, metrics):
        self.metrics = metrics

    @staticmethod
    def calculate_mean(numbers):
        return sum(numbers) / len(numbers) if numbers else 0

    @staticmethod
    def suggest_keywords(keywords):
        suggested_keywords = []
        top_keywords = sorted(keywords, key=lambda k: k['conversions'], reverse=True)[:5]

        for kw in top_keywords:
            suggested_keywords.append(f"{kw['text']} service")
            suggested_keywords.append(f"meilleur {kw['text']}")
            suggested_keywords.append(f"{kw['text']} professionnel")

            if kw['match_type'] != 'EXACT':
                suggested_keywords.append(f"[{kw['text']}]")

        return list(set(suggested_keywords))

    def analyze_performance(self, campaign):
        cost = campaign['cost']
        conversions = campaign['conversions']
        impressions = campaign['impressions']

        return {
            "total_cost": cost,
            "total_conversions": conversions,
            "conversion_rate": (conversions / impressions) * 100 if impressions > 0 else 0,
            "cost_per_conversion": cost / conversions if conversions > 0 else 0,
            "roas": campaign['conversions_value'] / cost if cost > 0 else 0,
            "click_through_rate": self.calculate_mean([kw['click_rate'] for kw in campaign['keywords']]) if campaign['keywords'] else 0
        }

    def generate_recommendations(self, campaign):
        recommendations = []
        performance = self.analyze_performance(campaign)

        if performance['conversion_rate'] < 1:
            recommendations.append(
                "Le taux de conversion est faible. Examinez la pertinence de vos annonces et pages de destination."
            )
        if performance['roas'] < 1:
            recommendations.append(
                "Le ROAS est inférieur à 1. Réévaluez votre stratégie de tarification et vos enchères."
            )
        if performance['click_through_rate'] < 1:
            recommendations.append(
                "Le taux de clic est faible. Améliorez le texte de vos annonces pour les rendre plus attrayantes."
            )

        if campaign['keywords']:
            click_rates = [kw['click_rate'] for kw in campaign['keywords']]
            avg_click_rate = self.calculate_mean(click_rates)

            for keyword in campaign['keywords']:
                if keyword['click_rate'] < avg_click_rate / 2:
                    recommendations.append(
                        f"Le mot-clé '{keyword['text']}' a un taux de clic faible ({keyword['click_rate']:.2f}%). Envisagez de le revoir ou de le supprimer."
                    )
                if keyword['cost_per_conversion'] > performance['cost_per_conversion'] * 1.5:
                    recommendations.append(
                        f"Le mot-clé '{keyword['text']}' a un coût par conversion élevé ({keyword['cost_per_conversion']:.2f}). Optimisez-le ou réduisez son enchère."
                    )

        return recommendations

    def get_recommendation(self, campaign):
        result = {
            "campaign_name": campaign['name'],
            "performance_analysis": self.analyze_performance(campaign),
            "recommendations": self.generate_recommendations(campaign),
            "suggested_keywords": []
        }

        if len(campaign['keywords']) > 0 :
            result["suggested_keywords"] = self.suggest_keywords(campaign['keywords'])

        return result

    def get_recommendations(self):
        return [self.get_recommendation(metric) for metric in self.metrics]
