"""
Security utilities and configurations for SFD service
"""
import re
from typing import Any, Optional
from django.core.exceptions import ValidationError


class SecurityValidator:
    """Security validation utilities"""
    
    # Allowed patterns for different input types
    TABLE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]+$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+$')
    
    @staticmethod
    def validate_table_name(table_name: str, allowed_tables: dict) -> bool:
        """Validate table name against whitelist and pattern"""
        if not table_name or not isinstance(table_name, str):
            return False
        if not SecurityValidator.TABLE_NAME_PATTERN.match(table_name):
            return False
        return table_name in allowed_tables
    
    @staticmethod
    def sanitize_for_logging(value: Any, max_length: int = 200) -> str:
        """Sanitize input for safe logging"""
        if value is None:
            return 'None'
        # Convert to string and remove control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(value))
        # Limit length to prevent log flooding
        return sanitized[:max_length] if len(sanitized) > max_length else sanitized
    
    @staticmethod
    def validate_method_name(method_name: str) -> bool:
        """Validate CRUD method names"""
        allowed_methods = {'create', 'view', 'update', 'delete', 'list'}
        return method_name in allowed_methods
    
    @staticmethod
    def validate_pk(pk: Any) -> bool:
        """Validate primary key format"""
        if pk is None:
            return False
        try:
            int(pk)
            return True
        except (ValueError, TypeError):
            return False


class AuditLogger:
    """Secure audit logging utility"""
    
    @staticmethod
    def log_crud_operation(logger, operation: str, table_name: str, 
                          user_id: Optional[str] = None, record_id: Optional[str] = None):
        """Log CRUD operations securely"""
        sanitized_operation = SecurityValidator.sanitize_for_logging(operation)
        sanitized_table = SecurityValidator.sanitize_for_logging(table_name)
        sanitized_user = SecurityValidator.sanitize_for_logging(user_id or 'unknown')
        
        log_message = f"{sanitized_operation} {sanitized_table} by user {sanitized_user}"
        if record_id:
            sanitized_record_id = SecurityValidator.sanitize_for_logging(record_id)
            log_message += f" record_id={sanitized_record_id}"
        
        logger.info(log_message)