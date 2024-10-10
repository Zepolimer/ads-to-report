from datetime import datetime

from google.ads.googleads.client import GoogleAdsClient as GAC
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v17.errors.types.authorization_error import AuthorizationErrorEnum

import settings


class GoogleAdsClient:
    CUSTOMER_ID = settings.CUSTOMER_ID
    COST_RATE = 1000000

    def __init__(self, developer_token, client_id, client_secret, refresh_token):
        self.client = GAC.load_from_dict({
            'developer_token': developer_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'login_customer_id': self.CUSTOMER_ID,
            'use_proto_plus': True,
        })
        self.service = self.client.get_service("GoogleAdsService")

    @staticmethod
    def __check_kwargs(**kwargs):
        metrics_from = kwargs.get('metrics_from', None)
        metrics_to = kwargs.get('metrics_to', None)

        if metrics_from or metrics_to:
            if not (isinstance(metrics_from, datetime) and isinstance(metrics_to, datetime)):
                raise Exception('`metrics_from` and `metrics_to` must be a datetime')

        account_id = kwargs.get('account_id', None)
        if not account_id:
            raise Exception('`account_id` is required')

    @staticmethod
    def __get_range_extra_query(**kwargs):
        metrics_from = kwargs.get('metrics_from', None)
        metrics_to = kwargs.get('metrics_to', None)

        if metrics_from and metrics_to:
            fmt = '%Y-%m-%d'
            return f" AND segments.date BETWEEN '{metrics_from.strftime(fmt)}' AND '{metrics_to.strftime(fmt)}'"
        return f" AND segments.date DURING LAST_MONTH"

    def do_call(self, account_id, query):
        try:
            results = self.service.search(customer_id=str(account_id), query=query)
        except GoogleAdsException as e:
            if e.failure.errors[0].error_code.authorization_error == AuthorizationErrorEnum.AuthorizationError.CUSTOMER_NOT_ENABLED:
                results = []
            else:
                raise e
        return results

    def get_metrics(self, **kwargs):
        self.__check_kwargs(**kwargs)
        metrics = []

        query = """
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                
                metrics.conversions,
                metrics.conversions_value,
                metrics.cost_micros,
                metrics.impressions,
                metrics.cost_per_conversion,
                metrics.current_model_attributed_conversions_value_per_cost,
                segments.date
            FROM campaign
            WHERE campaign.status = 'ENABLED'
                AND metrics.cost_micros > 0
        """ + self.__get_range_extra_query(**kwargs)

        results = self.do_call(kwargs['account_id'], query)
        for row in results:
            keywords = []

            if row.campaign.advertising_channel_type.name == 'SEARCH':
                keywords = self.get_keywords(campaign_id=row.campaign.id, **kwargs)

            metrics.append({
                'id': row.campaign.id,
                'date': row.segments.date,
                'name': row.campaign.name,
                'cost': row.metrics.cost_micros / self.COST_RATE,
                'impressions': row.metrics.impressions,
                'conversions': row.metrics.conversions,
                'conversions_value': row.metrics.conversions_value,
                'cost_per_conversion': row.metrics.cost_per_conversion / self.COST_RATE,
                'purchase_roas': row.metrics.current_model_attributed_conversions_value_per_cost,
                'campaign_type': row.campaign.advertising_channel_type.name,
                'provider': 'Google',
                'keywords': keywords
            })
        return metrics

    def get_keywords(self, campaign_id, **kwargs):
        metrics = []

        query = f"""
            SELECT
                ad_group_criterion.criterion_id,
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value
            FROM keyword_view
            WHERE campaign.id = '{campaign_id}'
                AND metrics.cost_micros > 0
        """ + self.__get_range_extra_query(**kwargs)

        results = self.do_call(kwargs['account_id'], query)
        for row in results:
            cost = row.metrics.cost_micros / self.COST_RATE
            clicks = row.metrics.clicks
            conversions = row.metrics.conversions
            conversions_value = row.metrics.conversions_value

            metrics.append({
                'id': row.ad_group_criterion.criterion_id,
                'text': row.ad_group_criterion.keyword.text.strip('+'),
                'match_type': row.ad_group_criterion.keyword.match_type.name,
                'cost': cost,
                'impressions': row.metrics.impressions,
                'clicks': clicks,
                'click_rate': (clicks / row.metrics.impressions) * 100 if row.metrics.impressions > 0 else 0,
                'cost_per_click': cost / clicks if clicks > 0 else 0,
                'conversions': conversions,
                'conversions_value': conversions_value,
                'conversion_rate': (conversions / clicks) * 100 if clicks > 0 else 0,
                'cost_per_conversion': cost / conversions if conversions > 0 else 0,
                'roas': conversions_value / cost if cost > 0 else 0
            })
        return metrics
