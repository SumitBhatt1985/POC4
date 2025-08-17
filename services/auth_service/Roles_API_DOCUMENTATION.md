ADD ROLE:

Endpoint: http://localhost:8000/api/v1/auth/roles/


Method: POST


Header: 

Content-Type: application/json

Input: 
{
  "name": "New-Admin2",
  "level": "High"
}

Response: 
{
    "role_id": 12,
    "name": "New-Admin2",
    "status": 1
}
----------------------------------------------------------
LIST ALL ROLES:

Endpoint: http://localhost:8000/api/v1/auth/roles/


Method: GET


Header: 

Content-Type: application/json

Input: 

Response: 
[
    {
        "role_id": 2,
        "name": "ABERTRANS",
        "status": 1
    },
.
.
.
    {
        "role_id": 10,
        "name": "D38FILLING",
        "status": 1
    }
]

----------------------------------------------------------
EDIT ROLE:

Endpoint: http://localhost:8000/api/v1/auth/roles/edit/


Method: PUT


Header: 

Content-Type: application/json

Input: 
    {
  	"role_id": 12,
  	"name": "New-Admin",
  	"level": "L4"
    }

Response: 
[
    {
        "role_id": 12,
        "name": "New-Admin",
        "status": 1
    }
]

----------------------------------------------------------
DELETE ROLE:

Endpoint: http://localhost:8000/api/v1/auth/roles/delete/


Method: DELETE


Header: 

Content-Type: application/json

Input: 
    {
  	"role_id": 12,
    }

Response: 
[
    {
        "message": "Role deleted (status set to 0)"    
    }
]
----------------------------------------------------------