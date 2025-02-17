# How to set up a static domain for an API Gateway
## Prerequisites
- Your domain registered in Route 53 (ask Coleman)
- A Route 53 Hosted Zone (see this [document](./referenceDocuments/route53HostedZone.md)) 
- An ACM (amazon certificate manager) certificate for your subdomain. (see this [document](./referenceDocuments/ACMCertificate.md))

## Manual Setup
- Create an API with a deployed stage. (see [this tutorial](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html))
- Enter Domain into API Gateway:
    - Go to API Gateway -> "Custom Domain names" and click "Add domain name."
    - Enter your subdomain, select your certificate, and click "Add domain name." ![Adding your domain name to API Gateway](Images/api_gateway_domain_setup.png)
- Map your domain to your API:
    - Click "Configure API mappings."
    - Select your API and stage from the drop downs and click "Save."
        - "Path" is not needed for a regular API.
- Route Route 53 Record to API:
    - Go to Route 53 -> Hosted Zones.
    - Create a hosted zone for your upper level domain and record for subdomain. (see certificate tutorial in Prerequisites)
        - Instead of selecting "CNAME" when defining the record, select "A" for Record type, choose the endpoint "Alias to API Gateway," and select your region and API.
- You should now be able to run `curl https://<your_subdomain>/<endpoint>` and see the correct return value.

Adapted from [this](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains.html) AWS Documentation.

## Common issues with SAM Setup
- Sam deploy process stalling on creating `APIBaseMapping`
    - Remove any record from the hosted zone that is linked to an API Gateway. One might be left over from the manual setup
- Sam deploy process fails because `The domain name you provided already exists`.
    - If it exists, remove the custom domain for API Gateway in the AWS Console.
- Sam deploy process fails because `<DOMAINNAME> already exists in stack <ARN>`
    - Go to AWS CloudFormation and delete any stack with the domain name. This will usually be a stack that failed and is labeled `FAILED_TO_CREATE`.