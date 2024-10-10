import settings
from datetime import datetime, timedelta

from src.google.metrics import GoogleAdsClient

from src.analyzer import MetricAnalyser
from src.extractor import Extractor

from src.openai import OpenAiClient


def from_api():
    client = GoogleAdsClient(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        developer_token=settings.DEVELOPER_TOKEN,
        refresh_token=settings.REFRESH_TOKEN,
    )

    metrics_from = datetime.now()
    metrics_to = metrics_from - timedelta(days=60)
    print(metrics_from)
    print(metrics_to)

    metrics = client.get_metrics(
        account_id=settings.ACCOUNT_ID
    )

    analyzer = MetricAnalyser(metrics=metrics)
    analyzer.get_recommendations()

    # OpenAiClient().generate_strategy(
    #     account_id='gse',
    #     campaign_metrics=analyzer.metrics,
    # )


def from_csv():
    extractor = Extractor()

    with (open('csv/campaigns.csv', 'r') as csv_file):
        extractor.get_campaigns(csv=csv_file)

    with (open('csv/keywords.csv', 'r') as csv_file):
        extractor.get_keywords(csv=csv_file)

    OpenAiClient().generate_strategy(
        account_id='nom_client',
        campaign_metrics=extractor.campaigns,
    )


if __name__ == '__main__':
    from_api()
    # from_csv()
