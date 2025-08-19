# API Usage Overview

This service supports two ways to perform CRUD operations:

## 1. Wrapper API (Recommended for Dynamic Routing)
- **Endpoint:** `/wrapper/` (POST)
- Pass `table_name`, `method_name`, and `data` in the body.
- Handles all CRUD operations via a single endpoint.
- See: `wrapper_api.md`

## 2. Direct CRUD Endpoints
- **Endpoints:** `/create/`, `/view/`, `/update/<int:pk>/`, `/delete/<int:pk>/`
- Use standard HTTP methods and pass `table_name` (and `data` as needed).
- See: `direct_crud_api.md`

## Security
- All endpoints require a valid JWT access token with a `userlogin` claim.
- Permissions and allowed tables are enforced in the backend.

## Example Table Names
- `tbl_command_master`
- `tbl_department_master`
- `tbl_equipment_category_master`
- `tbl_ship_category_master`
- `tbl_role_master`

## See Also
- `create_api.md`, `view_api.md`, `update_api.md`, `delete_api.md` for detailed usage.
