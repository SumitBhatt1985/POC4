# Wrapper API Documentation

**Endpoint:** `/wrapper/`
**Method:** POST

## Headers
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

---

## 1. Create
- **Request Body:**
```
{
  "table_name": "tbl_command_master",
  "method_name": "create",
  "data": {
    "command": "Test Command",
    "hq": "HQ1",
    "code": "CMD001"
  }
}
```
- **Response:** 201 Created, created record or 400 error

---

## 2. View/List
- **Request Body:**
```
{
  "table_name": "tbl_command_master",
  "method_name": "view",
  "data": {}
}
```
- **Response:** 200 OK, list of records or 400 error

---

## 3. Update
- **Request Body:**
```
{
  "table_name": "tbl_command_master",
  "method_name": "update",
  "data": {
    "id": 1,
    "command": "Updated Command"
  }
}
```
- **Response:** 200 OK, updated record or 400/404 error

---

## 4. Delete
- **Request Body:**
```
{
  "table_name": "tbl_command_master",
  "method_name": "delete",
  "data": {
    "id": 1
  }
}
```
- **Response:** 200 OK `{ "success": true }` or 400/404 error

---

## Notes
- All CRUD operations are routed through this endpoint by specifying `method_name`.
- For update/delete, `data` must include `id`.
- Table names must be in the allowed list.
- All requests require a valid JWT access token with a `userlogin` claim.
