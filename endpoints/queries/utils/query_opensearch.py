from queries.utils.opensearch import connect as create_client

def query_OpenSearch(search_term, index_name, field_name):
    client = create_client()

    query = {
        "size": 0,  # No need to fetch individual documents
        "aggs": {
            "docketId_stats": {
                "terms": {
                    "field": "docketId.keyword",  # Use .keyword for exact match on text fields
                    "size": 1000000  # Adjust size for expected number of unique docketIds
                },
                "aggs": {
                    "matching_comments": {
                        "filter": {
                            "match_phrase": {
                                field_name: search_term
                            }
                        }
                    }
                }
            }
        }
    }

    # Execute the query
    response = client.search(index=index_name, body=query)

    # Extract the aggregation results
    dockets = response["aggregations"]["docketId_stats"]["buckets"]

    # creates a dictionary of dockets that map the docketID to the number of total comments and the number of matching comments
    dockets_dict = {}

    for docket in dockets:
        docket_id = docket["key"]
        total_comments = docket["doc_count"]
        matching_comments = docket["matching_comments"]["doc_count"]

        dockets_dict[docket_id] = {
            "total": total_comments,
            "match": matching_comments
        }
    
    return dockets_dict