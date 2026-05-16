"""
API Response Utilities - Copy for authentication app
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
        """Standard success response"""
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
        """Standard error response"""
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


class ResponseMessages:
    """Centralized response messages for consistency"""
    
    # Authentication Messages
    USER_REGISTERED = "User registered successfully"
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logout successful"
    TOKEN_REFRESHED = "Token refreshed successfully"
    PROFILE_RETRIEVED = "Profile retrieved successfully"
    PROFILE_UPDATED = "Profile updated successfully"
    
    # Error Messages
    VALIDATION_ERROR = "Validation failed. Please check your input"
    INVALID_TOKEN = "Invalid or expired token"
