# View/List API Documentation

**Endpoint:** `/view/`
**Method:** GET

## Headers
- `Authorization: Bearer <JWT_TOKEN>`

## Query Parameters
- `table_name`: The table to list (e.g., `tbl_command_master`)

## Example
`GET /view/?table_name=tbl_command_master`

## Response
- 200 OK: List of records
- 400: Error message
