## Auth (namespaces/auth.py)
api | type | input-parametres (JSON for POST, args for GET) | Output (On Error) | Output (On Success)
--- | --- | --- | --- | ---
`/api/auth/register` | POST | `{['zID': 'z5161616'], ['password': "11111111" (8 digits or above)], ["firstName": "Steven"], ["lastName": "Shen"], ["isArc": True], ["commencementYear": 2020], ["studentType": "undergraduate"], ["degreeType": "undergraduate"]}` | 400, `Malformed Request` | 200