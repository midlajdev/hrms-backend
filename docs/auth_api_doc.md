# HRMS Authentication & Profile API Documentation

### Base URL

``` /api/ ```

### 1. User Signup
### Creates a new user account.

### Endpoint
```POST /api/signup/```
### Request Body

```
 {
  "email": "user@test.com",
  "password": "password123",
  "password_confirm": "password123",
  "role": "candidate"
} 
```
### Response
```
{
  "success": true,
  "data": {
    "email": "user@test.com",
    "role": "candidate"
  },
  "message": "User created successfully",
  "access": "access_token",
  "refresh": "refresh_token"
}
```
## 2. Logout

### Invalidates the refresh token.

### Endpoint
```POST /api/logout/ ```

### Headers
```Authorization: Bearer <access_token>```

### Request Body
```
{
  "refresh": "refresh_token"
}
```
### Response
```
{
  "success": true,
  "message": "Logged out successfully"
}
```
## 3. Candidate Profile

### Retrieve or update candidate profile.

### Endpoint
```
GET /api/candidate/profile/
PUT /api/candidate/profile/
PATCH /api/candidate/profile/
```
### Headers
```Authorization: Bearer <access_token>```
### Response Example
```
{
  "id": 1,
  "user": 1,
  "phone": "9876543210",
  "skills": "Python, Django",
  "total_experience": 2,
  "location": "Kerala",
  "is_active": true
}

```

## 4. Candidate Account Soft Delete

### Deactivates the candidate profile and user account.

### Endpoint
```DELETE /api/candidate/delete/```

### Headers
```Authorization: Bearer <access_token>```
### Response
```
{
  "success": true,
  "message": "Account deleted successfully"
}
```
## 5. Employer Profile

### Retrieve or update employer profile.

### Endpoint
```
GET /api/employer/profile/
PUT /api/employer/profile/
PATCH /api/employer/profile/
```
### Headers
```Authorization: Bearer <access_token>```
### Response Example
```
{
  "company_name": "Tech Solutions",
  "industry": "Software",
  "company_location": "Bangalore",
  "company_size": "11-50",
  "is_verified": false
}
```

## 6. Employer Profile Soft Delete

### Deactivates employer profile.

Endpoint
```
DELETE /api/employer/delete/
```
Headers

```Authorization: Bearer <access_token>```

Response
```
{
  "success": true,
  "message": "Employer profile deleted successfully"
}
```
## 7. Resume Upload

### Uploads candidate resume.

Endpoint

```PUT /api/candidate/upload-resume/```

Headers

```Authorization: Bearer <access_token>```

```Content-Type: multipart/form-data```

## Request Body
```
resume: file
Allowed File Types

PDF
DOC
DOCX

Max File Size
2 MB
```
Response
```
{
  "message": "Resume uploaded successfully"
}
```