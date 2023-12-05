import requests
import xmltodict
import logging

from pendulum import parse
from singer_sdk.streams import Stream
from netsuitesdk.internal.client import NetSuiteClient

from singer_sdk import typing as th

class SavedSearchesClient(Stream):
    name = "saved_search"
    ns_type = "TransactionSearchAdvanced"
    ns_urn_type = "sales_2017_2.transactions.webservices.netsuite.com"

    def __init__(self, *args, **kwargs):
        self.ns_client = NetSuiteClient(
            account=self.config.get("ns_account"),
            caching=True
        )
        self.ns_client.connect_tba(
            consumer_key=self.config.get("ns_consumer_key"),
            consumer_secret=self.config.get("ns_consumer_secret"),
            token_key=self.config.get("ns_token_key"),
            token_secret=self.config.get("ns_token_secret")
        )
        self._prepared_schema = self.prepare_schema()
        self._schema = self._prepared_schema
        self._downloaded_items = []
        kwargs["schema"] = self._prepared_schema
        super().__init__(*args, **kwargs)

    def prepare_schema(self):
        saved_search_ids = self.config.get("TransactionSearchAdvanced")
        if saved_search_ids == None:
            return th.PropertiesList().to_dict()

        if isinstance(saved_search_ids, str):
            saved_search_ids = saved_search_ids.split(",")

        id = saved_search_ids[0]
        records, _ = self.get_all_items_from_saved_searches(
            saved_search_id=id,
            saved_search_type=self.ns_type,
            saved_search_type_urn=self.ns_urn_type,
            page_size=5
        )
        record = next(self._parse_response_to_json(records))
        fields = []

        for k, v in record.items():
            try:
                parse(v)
                fields.append(th.Property(k, th.DateTimeType))
            except:
                fields.append(th.Property(k, th.StringType))

        return th.PropertiesList(*fields).to_dict()

    def get_records(self, context=None):
        if isinstance(self.config.get(self.ns_type), str):
            saved_search_ids = self.config.get(self.ns_type).split(",")
        else:
            saved_search_ids = self.config.get(self.ns_type, [])

        for search_id in saved_search_ids:
            page = 1
            page_size = 1000
            total_pages = 2

            while page <= int(total_pages):
                self.logger.info(f"Getting saved search {search_id} page {page}")

                search_response, total_pages = self.get_all_items_from_saved_searches(
                    saved_search_id=search_id,
                    saved_search_type=self.ns_type,
                    saved_search_type_urn=self.ns_urn_type,
                    page=page,
                    page_size=page_size
                )
                for item in self._parse_response_to_json(search_response):
                    if item not in self._downloaded_items:
                        self._downloaded_items.append(item)
                        yield item
                page += 1

    def _parse_search_response(self, response_xml):
        parsed_response = xmltodict.parse(response_xml)
        search_response = parsed_response["soapenv:Envelope"]["soapenv:Body"]["searchResponse"]
        search_response = search_response["platformCore:searchResult"]
        return search_response

    def _parse_response_to_json(self, search_response):
        modified_search_response = search_response["platformCore:searchRowList"]
        records = modified_search_response["platformCore:searchRow"]
        type_nickname = records[0]["@xsi:type"].split(":")[0]

        for record in records:
            formatted_record = {}
            for k, v in record[f"{type_nickname}:basic"].items():
                if "@" in k:
                    continue

                field = k.split(":")[1]
                value = v["platformCore:searchValue"]
                if isinstance(value, dict):
                    formatted_record[f"{field}Id"] = value["@internalId"]
                else:
                    formatted_record[field] = value

            yield formatted_record

    def get_all_items_from_saved_searches(
            self,
            saved_search_id=1,
            saved_search_type_urn="sales_2017_2.transactions.webservices.netsuite.com",
            saved_search_type="TransactionSearchAdvanced",
            page_size=1000,
            page=1
        ):
        url = f"https://{self.config['ns_account']}.suitetalk.api.netsuite.com/services/NetSuitePort_2017_2"
        oauth_creds = self.ns_client._build_soap_headers()
        oauth_creds = oauth_creds["tokenPassport"]

        base_request = f"""<soap:Envelope xmlns:platformFaults="urn:faults_2017_2.platform.webservices.netsuite.com" xmlns:platformMsgs="urn:messages_2017_2.platform.webservices.netsuite.com" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="urn:platform_2017_2.webservices.netsuite.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <soap:Header>
                <searchPreferences xmlns:ns7="urn:messages_2020_2.platform.webservices.netsuite.com">
                    <bodyFieldsOnly>true</bodyFieldsOnly>
                    <pageIndex>{page}</pageIndex>
                    <pageSize>{page_size}</pageSize>
                </searchPreferences>
                <tokenPassport>
                    <account>{oauth_creds["account"]}</account>
                    <consumerKey>{oauth_creds["consumerKey"]}</consumerKey>
                    <token>{oauth_creds["token"]}</token>
                    <nonce>{oauth_creds["nonce"]}</nonce>
                    <timestamp>{oauth_creds["timestamp"]}</timestamp>
                    <signature algorithm="HMAC-SHA256">{oauth_creds["signature"]["_value_1"]}</signature>
                </tokenPassport>
            </soap:Header>
            <soap:Body>
                <search>
                    <searchRecord xmlns:q1="urn:{saved_search_type_urn}" xsi:type="q1:{saved_search_type}" savedSearchId="{saved_search_id}" />
                </search>
            </soap:Body>
        </soap:Envelope>"""

        headers = {"SOAPAction": "search", "Content-Type": "text/xml"}
        logging.info(f"Getting saved search for type {self.ns_type}... Page: {page} and Page Size: {page_size}")
        res = requests.post(url, headers=headers, data=base_request)
        if res.status_code >= 400 or 'isSuccess="false"' in res.text:
            raise Exception(f"Failed to get saved search for type {saved_search_type} - {res.text}")

        search_response = self._parse_search_response(res.text)
        total_pages = search_response["platformCore:totalPages"]
        return search_response, total_pages
