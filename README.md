# API
# How to run the API for testing
## Locally
- If any changes have been made to `template.yaml` run `sam validate` to check for errors
- Make sure to install [docker](https://www.docker.com/get-started/) and allow the default docker socket to be used (info [here](https://stackoverflow.com/a/77926411))
- To run locally, run `sam local start-api`
- The API should be running at `http://127.0.0.1:3000`
## On AWS
- Run `sam deploy --guided` and enter the following options from the sample output below to create the resources need on AWS:
```
Configuring SAM deploy
======================

    Looking for config file [samconfig.toml] :  Found
    Reading default arguments  :  Success

    Setting default arguments for 'sam deploy'
    =========================================
    Stack Name [sam-app]: ENTER
    AWS Region [us-west-2]: ENTER
    #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
    Confirm changes before deploy [Y/n]: n
    #SAM needs permission to be able to create roles to connect to the resources in your template
    Allow SAM CLI IAM role creation [Y/n]: ENTER
    #Preserves the state of previously provisioned resources when an operation fails
    Disable rollback [y/N]: ENTER
    *FUNCTIONNAME* may not have authorization defined, Is this okay? [y/N]: y
    Save arguments to configuration file [Y/n]: ENTER
    SAM configuration file [samconfig.toml]: ENTER
    SAM configuration environment [default]: ENTER
```
- Run `sam list endpoints --output json` to get the link for the endpoint you're testing.
- If you'd like to update the API on AWS in real time, run `sam sync --watch`
    - Warning: This takes a couple minutes to start up
    - Ready once you see `Infra sync completed.`
- When done, run `sam delete` to avoid leaving resources up.

Adapted from this [AWS Tutorial](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html#serverless-getting-started-hello-world-delete)
