# Master Service CRUD API Documentation

## Overview
The Master Service provides two main API endpoints for CRUD operations on master tables:

**Flexible Wrapper API** - For advanced CRUD operations using any column for identification

---

## 🔗 API Endpoints

### Standard Wrapper API
**Full URL:** `http://your-domain/api/master/wrapper/`
**Method:** `POST`

### Flexible Example Wrapper API  
**Full URL:** `http://127.0.0.1:8001/api/v1/master/wrapper/`
**Method:** `POST`

---

## 🔐 Authentication
Both endpoints require JWT authentication:
```
Headers:
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

---

## 📋 Supported Tables
All operations support these master tables:
- `tbl_command_master`
- `tbl_department_master` 
- `tbl_equipment_category_master`
- `tbl_ship_category_master`
- `tbl_role_master`
- `tbl_ship_state_master`
- `tbl_ship_location_master`
- `tbl_activity_type_master`
- `tbl_activity_details_master`
- `tbl_lubricant_master`

---

## 🛠️ CRUD Operations

### 1. CREATE (`crud_create`)

#### Standard Wrapper API
**URL:** `http://127.0.0.1:8001/api/v1/master/wrapper/`
**Method:** `POST`

**Request:**
```json
{
  "table_name": "tbl_command_master",
  "method_name": "create",
  "data": {
    "command_id": "CMD001",
    "command": "Test Command",
    "hq": "Headquarters Location",
    "code": "CMD001"
  }
}
```

**Response (Both APIs):**
```json
{
  "success": true,
  "message": "Record created successfully.",
  "data": {
    "id": 1,
    "command_id": "CMD001",
    "command": "Test Command",
    "hq": "Headquarters Location",
    "code": "CMD001",
    "is_active": 1
  }
}
```

**Notes:**
- Automatically sets `is_active = 1` for new records
- Validates data using model serializers
- Returns 201 status code on success

---

### 2. LIST/VIEW (`crud_list`)

#### Standard Wrapper API
**URL:** `http://127.0.0.1:8001/api/v1/master/wrapper/`
**Method:** `POST`

**Request:**
```json
{
  "table_name": "tbl_command_master",
  "method_name": "list"
}
```
*OR*
```json
{
  "table_name": "tbl_command_master", 
  "method_name": "view"
}
```

**Response (Both APIs):**
```json
{
  "success": true,
  "message": "Records fetched successfully.",
  "data": [
    {
      "id": 1,
      "command_id": "CMD001", 
      "command": "Test Command",
      "hq": "Headquarters Location",
      "code": "CMD001",
      "is_active": 1
    },
    {
      "id": 2,
      "command_id": "CMD002",
      "command": "Another Command", 
      "hq": "Another HQ",
      "code": "CMD002",
      "is_active": 1
    }
  ]
}
```

**Notes:**
- Only returns active records (`is_active = 1` or `is_active = True`)
- Returns all fields for each record
- Empty array if no active records found

---

### 3. UPDATE

---

#### Flexible Wrapper API (`flexible_crud_update`)
**URL:** `http://127.0.0.1:8001/api/v1/master/wrapper/`
**Method:** `POST`

**Request:**
```json
{
  "table_name": "tbl_command_master",
  "method_name": "update",
  "column_name": "command_id",
  "column_value": "CMD001", 
  "data": {
    "command": "Updated Command Name",
    "hq": "Updated Headquarters",
    "code": "NEW001"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Record updated successfully (old record archived, new record created).",
  "data": {
    "id": 15,
    "command_id": "CMD001",
    "command": "Updated Command Name", 
    "hq": "Updated Headquarters",
    "code": "NEW001",
    "is_active": 1
  }
}
```

**Process:**
1. Finds record where `command_id = "CMD001"` AND `is_active = 1`
2. Sets `is_active = 0` for old record (soft delete/archive)
3. Creates new record with updated data
4. Preserves the `column_value` in new record

**Notes:**
- Creates audit trail by preserving old records
- Can use any column name for identification
- Automatically restores old record if new record creation fails
- `column_name` must be a valid field in the model

---


---

#### 4. Flexible Wrapper API (`flexible_crud_delete`)
**URL:** `http://your-domain/api/master-service/flexible-wrapper/`
**Method:** `POST`

**Request:**
```json
{
  "table_name": "tbl_command_master", 
  "method_name": "delete",
  "column_name": "command_id",
  "column_value": "CMD001"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Record soft deleted successfully.",
  "data": null
}
```

**Process:**
1. Finds record where `command_id = "CMD001"` AND `is_active = 1`
2. Sets `is_active = 0` (soft delete)
3. Record is preserved for audit purposes

**Notes:**
- Both APIs perform soft delete only
- Records are never physically deleted
- Can use any column name for identification

---

### 5. LIST DISTINCT COLUMN VALUES (`crud_col_values`)

**Flexible Wrapper API**
**URL:** `http://127.0.0.1:8001/api/v1/master/wrapper/`
**Method:** `POST`

**Request:**
```json
{
  "table_name": "vw_sfd_section_add",
  "method_name": "col_values",
  "column_list": ["department_id", "department_name"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Distinct values for columns ['department_id', 'department_name'] from vw_sfd_section_add.",
  "data": [
    {"department_id": 1, "department_name": "Engineering"},
    {"department_id": 2, "department_name": "Logistics"},
    {"department_id": 3, "department_name": "Medical"}
  ]
}
```

**Notes:**
- Returns all unique combinations of the requested columns.
- Works for any allowed table or view.
- Returns validation errors for missing/invalid columns or tables.

---

## 🚨 Error Responses

### Invalid Table Name
```json
{
  "success": false,
  "message": "Invalid table name.",
  "data": null
}
```

### Record Not Found
```json
{
  "success": false,
  "message": "Active record not found with command_id=CMD999",
  "data": null
}
```

### Invalid Column Name (Flexible API)
```json
{
  "success": false,
  "message": "Invalid column name: invalid_column",
  "data": null
}
```

### Multiple Records Found (Flexible API)
```json
{
  "success": false,
  "message": "Multiple active records found with name=Duplicate Name", 
  "data": null
}
```

### Missing Required Fields
```json
{
  "success": false,
  "message": "Missing required field: column_name for update.",
  "data": null
}
```

### Validation Errors
```json
{
  "success": false,
  "message": "Invalid data.",
  "data": {
    "field_name": ["This field is required."],
    "another_field": ["This field must be unique."]
  }
}
```

---

## 📊 Comparison: Standard vs Flexible APIs

| Feature | Standard Wrapper | Flexible Wrapper |
|---------|------------------|------------------|
| **URL** | `/wrapper/` | `/flexible-wrapper/` |
| **Identification** | `id` field only | Any column name |
| **Update Behavior** | Modifies in place | Archive old + Create new |
| **Audit Trail** | Limited | Full history |
| **Use Cases** | Simple operations | Advanced operations |
| **Backward Compatible** | Yes | Yes |

---

## 💡 Usage Recommendations

### Use Standard Wrapper API when:
- Simple CRUD operations
- Working with `id` field
- No audit trail requirements
- Existing frontend integration

### Use Flexible Wrapper API when:
- Need to identify records by business keys (`command_id`, `role_id`, etc.)
- Require full audit trail
- Want to preserve history of changes
- Advanced data management needs

---

## 🔧 Frontend Integration Examples

### JavaScript/Fetch API
```javascript
// Create record
const createRecord = async (tableName, recordData) => {
  const response = await fetch('http://your-domain/api/master-service/flexible-wrapper/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      table_name: tableName,
      method_name: 'create', 
      data: recordData
    })
  });
  return await response.json();
};

// Update using business key
const updateRecord = async (tableName, columnName, columnValue, updateData) => {
  const response = await fetch('http://your-domain/api/master-service/flexible-wrapper/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      table_name: tableName,
      method_name: 'update',
      column_name: columnName,
      column_value: columnValue,
      data: updateData
    })
  });
  return await response.json();
};
```

### React Hook Example
```jsx
const useCRUDOperations = (baseURL, token) => {
  const flexibleUpdate = async (tableName, columnName, columnValue, data) => {
    try {
      const response = await fetch(`${baseURL}/flexible-wrapper/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          table_name: tableName,
          method_name: 'update',
          column_name: columnName, 
          column_value: columnValue,
          data: data
        })
      });
      return await response.json();
    } catch (error) {
      console.error('Update failed:', error);
      throw error;
    }
  };

  return { flexibleUpdate };
};
```

---

## ✅ Best Practices

1. **Always validate column names** before sending to flexible API
2. **Use business keys** (command_id, role_id) when available
3. **Handle multiple record scenarios** for non-unique columns
4. **Implement proper error handling** for all API responses
5. **Use flexible API for audit requirements**
6. **Keep standard API for simple operations**
