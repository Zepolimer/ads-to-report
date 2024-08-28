from pprint import pprint

import settings
from src.analyzer import MetricAnalyser
from src.google.metrics import GoogleAdsClient


def main():
    client = GoogleAdsClient(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        developer_token=settings.DEVELOPER_TOKEN,
        refresh_token=settings.REFRESH_TOKEN,
    )

    metrics = client.get_metrics(
        account_id=settings.ACCOUNT_ID
    )

    analyzer = MetricAnalyser(metrics=metrics)
    recommendations = analyzer.get_recommendations()

    pprint(recommendations)

    # OpenAiClient().generate_strategy(
    #     account_id=metrics['account_id'],
    #     campaign_metrics=metrics['campaigns'],
    #     keyword_metrics=metrics['keywords']
    # )


if __name__ == '__main__':
    main()
