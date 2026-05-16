"""
API Response Utilities
Standardized response formatting for consistent API responses
"""
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from datetime import datetime
from typing import Any, Dict, List, Optional


class ApiResponse:
    """
    Centralized API response handler
    Ensures consistent response structure across all endpoints
    """
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
        meta: Optional[Dict] = None
    ) -> DRFResponse:
        """
        Standard success response
        
        Args:
            data: Response payload (dict, list, or None)
            message: Success message
            status_code: HTTP status code
            meta: Optional metadata (pagination, counts, etc.)
        
        Returns:
            DRFResponse with standardized format
        """
        response_data = {
            'success': True,
            'message': message,
            'data': data if data is not None else [],
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        if meta:
            response_data['meta'] = meta
            
        return DRFResponse(response_data, status=status_code)
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        errors: Optional[Any] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: Optional[str] = None
    ) -> DRFResponse:
        """
        Standard error response
        
        Args:
            message: Error message
            errors: Detailed error information
            status_code: HTTP status code
            error_code: Optional error code for client handling
        
        Returns:
            DRFResponse with standardized error format
        """
        response_data = {
            'success': False,
            'message': message,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        if errors:
            response_data['errors'] = errors
            
        if error_code:
            response_data['error_code'] = error_code
            
        return DRFResponse(response_data, status=status_code)
    
    @staticmethod
    def created(
        data: Any,
        message: str = "Resource created successfully"
    ) -> DRFResponse:
        """Convenience method for 201 Created responses"""
        return ApiResponse.success(
            data=data,
            message=message,
            status_code=status.HTTP_201_CREATED
        )
    
    @staticmethod
    def no_content(
        message: str = "Operation completed successfully"
    ) -> DRFResponse:
        """Convenience method for 204 No Content responses"""
        return DRFResponse(
            {
                'success': True,
                'message': message,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            },
            status=status.HTTP_204_NO_CONTENT
        )
    
    @staticmethod
    def not_found(
        message: str = "Resource not found",
        resource: Optional[str] = None
    ) -> DRFResponse:
        """Convenience method for 404 Not Found responses"""
        error_message = f"{resource} not found" if resource else message
        return ApiResponse.error(
            message=error_message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND"
        )
    
    @staticmethod
    def unauthorized(
        message: str = "Authentication required"
    ) -> DRFResponse:
        """Convenience method for 401 Unauthorized responses"""
        return ApiResponse.error(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED"
        )
    
    @staticmethod
    def forbidden(
        message: str = "You don't have permission to perform this action"
    ) -> DRFResponse:
        """Convenience method for 403 Forbidden responses"""
        return ApiResponse.error(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN"
        )
    
    @staticmethod
    def validation_error(
        errors: Dict,
        message: str = "Validation failed"
    ) -> DRFResponse:
        """Convenience method for validation errors"""
        return ApiResponse.error(
            message=message,
            errors=errors,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR"
        )
    
    @staticmethod
    def paginated(
        data: List,
        page: int,
        page_size: int,
        total: int,
        message: str = "Data retrieved successfully"
    ) -> DRFResponse:
        """
        Paginated response with metadata
        
        Args:
            data: List of items for current page
            page: Current page number
            page_size: Items per page
            total: Total number of items
            message: Success message
        
        Returns:
            DRFResponse with pagination metadata
        """
        total_pages = (total + page_size - 1) // page_size
        
        meta = {
            'pagination': {
                'current_page': page,
                'page_size': page_size,
                'total_items': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1
            }
        }
        
        return ApiResponse.success(
            data=data,
            message=message,
            meta=meta
        )


class ResponseMessages:
    """
    Centralized response messages for consistency
    Makes it easy to change messages globally or support i18n
    """
    
    # Stock Item Messages
    STOCK_LIST_SUCCESS = "Stock items retrieved successfully"
    STOCK_CREATED = "Stock item created successfully"
    STOCK_UPDATED = "Stock item updated successfully"
    STOCK_DELETED = "Stock item deleted successfully"
    STOCK_NOT_FOUND = "Stock item not found"
    STOCK_QUANTITY_INCREASED = "Stock quantity increased successfully"
    STOCK_QUANTITY_DECREASED = "Stock quantity decreased successfully"
    
    # Authentication Messages
    USER_REGISTERED = "User registered successfully"
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logout successful"
    TOKEN_REFRESHED = "Token refreshed successfully"
    PROFILE_RETRIEVED = "Profile retrieved successfully"
    PROFILE_UPDATED = "Profile updated successfully"
    
    # Error Messages
    VALIDATION_ERROR = "Validation failed. Please check your input"
    UNAUTHORIZED = "Authentication credentials were not provided or are invalid"
    FORBIDDEN = "You don't have permission to perform this action"
    NOT_FOUND = "The requested resource was not found"
    SERVER_ERROR = "An internal server error occurred. Please try again later"
    INVALID_TOKEN = "Invalid or expired token"
    
    # Generic Messages
    SUCCESS = "Operation completed successfully"
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"
