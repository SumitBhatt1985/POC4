# Direct CRUD API Endpoints

These endpoints allow you to perform CRUD operations directly, without using the wrapper API.

## Create
- **Endpoint:** `/create/`
- **Method:** POST
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
  - `Content-Type: application/json`
- **Body:**
```
{
  "table_name": "tbl_command_master",
  "data": { "command": "Test", "hq": "HQ1", "code": "CMD001" }
}
```
- **Response:** 201 Created or 400 Error

## View/List
- **Endpoint:** `/view/`
- **Method:** GET
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Query:** `table_name=tbl_command_master`
- **Response:** 200 OK (list) or 400 Error

## Update
- **Endpoint:** `/update/<int:pk>/`
- **Method:** PUT
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
  - `Content-Type: application/json`
- **Body:**
```
{
  "table_name": "tbl_command_master",
  "data": { "command": "Updated" }
}
```
- **Response:** 200 OK or 400/404 Error

## Delete
- **Endpoint:** `/delete/<int:pk>/`
- **Method:** DELETE
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
  - `Content-Type: application/json`
- **Body:**
```
{
  "table_name": "tbl_command_master" 
}
```
- **Response:** 200 OK or 400/404 Error

---

## Notes
- These endpoints use the generic CRUD API classes in `views.py`.
- You can use either these direct endpoints or the wrapper API for all operations.
