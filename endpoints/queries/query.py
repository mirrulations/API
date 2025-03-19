from queries.utils.query_opensearch import query_OpenSearch
from queries.utils.query_sql import append_docket_titles
from queries.utils.sql import connect

def search(search_term): 
    os_results = query_OpenSearch(search_term)
    print(os_results)
    return append_docket_titles(os_results, connect())

