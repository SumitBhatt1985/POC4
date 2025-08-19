# Update API Documentation

**Endpoint:** `/update/<int:pk>/`
**Method:** PUT

## Headers
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

## Request Body
```
{
  "table_name": "tbl_command_master", // or any allowed table
  "data": { /* fields to update */ }
}
```

## Example
`PUT /update/1/`
```
{
  "table_name": "tbl_command_master",
  "data": {
    "command": "Updated Command"
  }
}
```

## Response
- 200 OK: Updated record
- 400/404: Error message
