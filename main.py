from pprint import pprint

import settings
from src.google.metrics import GoogleAdsClient

from src.analyzer import MetricAnalyser
from src.extractor import Extractor


def from_api():
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


def from_csv():
    extractor = Extractor()

    with (open('csv/campaigns.csv', 'r') as csv_file):
        extractor.get_campaigns(csv=csv_file)

    with (open('csv/keywords.csv', 'r') as csv_file):
        extractor.get_keywords(csv=csv_file)

    pprint(extractor.campaigns)


if __name__ == '__main__':
    # from_api()
    from_csv()
