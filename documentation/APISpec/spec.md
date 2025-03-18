# /search Endpoint
## Input
- searchTerm
	- Query Parameter
	- Type: String
	- Bad request if common word or too short (need to define this better)
- pageNumber
	- Query Parameter
	- Type: Int
	- between 0-9, likely to change in the future
- sessionID
	- Header
	- Type: Str
	- [JSON Web Token from Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html)
- sortParams
	- Body
	- Type: Dict
		- desc: Bool
			- whether results are ascending or descending 
			- default: True
		- sortType: Str
			- dateModified, relevance, or alphaByTitle.
			- default: relevance
- filterParams
	- Body
	- Type: Dict
		- agencies: Str[]
			- if empty then all agencies are allowed, otherwise just the ones listed are allowed
            - abbreviations, not full names
			- default: [] (empty list)
		- dateRange: Dict
			- gets dockers modified between the two dates
			- start: str (ISO-8601, parsable in JS)
				- defaults to Jan 1st 1970
			- end: str (ISO-8601, parsable in JS)
				- defaults to current date
		- docketType: Str
			- "Rulemaking", "Nonrulemaking", or "" (empty string, return both)
			- defaults to ""
## Output
- currentPage: int
    - between 0-9, likely to change in the future 
- totalPages: int
- dockets: docket[]
	- id: str
	- comments: dict
		- match: int
		- total: int
	- title: str
	- matchQuality: num
		- we need to make an equation that combines total matching, the ratio of matching, and the recency of the date into one number for the relevance search.
	- dateModified: str (ISO-8601, parsable in JS)
	- agencyName: str
# /agencies Endpoint
## Input
Has no input
## Output
- Dict of all agencies
	- agencyId : agencyName