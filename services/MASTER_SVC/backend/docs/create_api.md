# Create API Documentation

**Endpoint:** `/create/`
**Method:** POST

## Headers
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

## Request Body
```
{
  "table_name": "tbl_command_master", // or any allowed table
  "data": { /* fields required for creation */ }
}
```

## Example
```
{
  "table_name": "tbl_command_master",
  "data": {
    "command": "Test Command",
    "hq": "HQ1",
    "code": "CMD001"
  }
}
```

## Response
- 201 Created: Created record
- 400: Error message
