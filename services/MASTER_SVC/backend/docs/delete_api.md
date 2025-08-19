# Delete API Documentation

**Endpoint:** `/delete/<int:pk>/`
**Method:** DELETE

## Headers
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

## Request Body
```
{
  "table_name": "tbl_command_master" // or any allowed table
}
```

## Example
`DELETE /delete/1/`
```
{
  "table_name": "tbl_command_master"
}
```

## Response
- 200 OK: `{ "success": true }`
- 400/404: Error message
