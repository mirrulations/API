import json

def test_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": json.dumps([
            {
                "docketId": "BIS-2024-0053",
                "numComments": "70/100",
                "docketTitle": "Public Briefing on Revisions to Space Related Export Controls Under Export Administration Regulations and International Traffic in Arms Regulations",
                "matchQuality": ".85"
            },
            {
                "docketId": "DOS-2022-0004",
                "numComments": "24/100",
                "docketTitle": "International Traffic in Arms Regulations: Consolidation and Restructuring of Purposes and Definitions",
                "matchQuality": ".6"
            },
            {
                "docketId": "DOS-2010-0194",
                "numComments": "2/50",
                "docketTitle": "2008 - Amendment to the International Arms Traffic in Arms Regulations: Eritrea",
                "matchQuality": ".2"
            }
        ]),
    }
