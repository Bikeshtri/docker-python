# Monkey patches BigQuery client creation to use proxy.

# Import torch before anything else. This is a hacky workaround to an error on dlopen
# reporting a limit on static TLS, tracked in https://github.com/pytorch/pytorch/issues/2575
import torch
import os

kaggle_proxy_token = os.getenv("KAGGLE_DATA_PROXY_TOKEN")
if kaggle_proxy_token:
    from google.auth import credentials
    from google.cloud import bigquery
    from google.cloud.bigquery._http import Connection

    Connection.API_BASE_URL = os.getenv("KAGGLE_DATA_PROXY_URL")
    Connection._EXTRA_HEADERS["X-KAGGLE-PROXY-DATA"] = kaggle_proxy_token

    bq_client = bigquery.Client
    bigquery.Client = lambda *args, **kwargs: bq_client(
        *args,
        credentials=credentials.AnonymousCredentials(),
        project=os.getenv("KAGGLE_DATA_PROXY_PROJECT"),
        **kwargs)

    credentials.AnonymousCredentials.refresh = lambda *args: None
