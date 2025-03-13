this script requires two lambda layers:
the `aoss-imports` (`arn:aws:lambda:us-east-1:936771282063:layer:aoss-imports:2`) and
the `psycopg-import` (`arn:aws:lambda:us-east-1:936771282063:layer:psycopg-import:1`)

it needs to be in the `mirrulationsdb` VPC (`vpc-00f6bc3c21d7d91d5`)

it needs to be in all the following subnets:
```
subnet-0548c79ad1faa1117
subnet-0157ddb92a2e1d6ad
subnet-049c40a73343487e5
subnet-06bae533696203b97
subnet-073247252e9c9fa78
subnet-0e157bfea98242a74
```

and apart of the security group `mirrulationsdb_security` (`sg-03e2bf8d3930f3c42`)

the lambda also needs to have the `334s25_lambda_execution_opensearch` role, or have the same permissions as the role.