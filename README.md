# blog-python
# Blog API - Django REST Framework

A simple yet powerful blog API built with Django REST Framework, featuring JWT authentication and full CRUD operations.

## Features

- 🔐 JWT Authentication (Access & Refresh tokens)
- 👤 User Registration & Login (Email-based)
- 📝 Full CRUD operations for blog posts
- 🔍 Search, filter, and sort blog posts
- 📄 Pagination support
- 🏷️ Tag system for blog posts
- 🔒 Author-only edit/delete permissions
- 📊 Published/Draft post status

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd blog-python
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| GET/PUT | `/api/auth/profile/` | User profile |
| POST | `/api/auth/token/refresh/` | Refresh access token |

### Blog Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/blog/posts/` | List all published posts |
| POST | `/api/blog/posts/` | Create new post (auth required) |
| GET | `/api/blog/posts/{id}/` | Get specific post |
| PUT/PATCH | `/api/blog/posts/{id}/` | Update post (author only) |
| DELETE | `/api/blog/posts/{id}/` | Delete post (author only) |
| GET | `/api/blog/my-posts/` | List user's posts (auth required) |

## Example API Usage

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### 2. User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create Blog Post
```bash
curl -X POST http://localhost:8000/api/blog/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post...",
    "is_published": true,
    "tags": "django, python, api"
  }'
```

### 4. Search Posts
```bash
curl "http://localhost:8000/api/blog/posts/?search=django&ordering=-created_at"
```

## Query Parameters

### Blog Posts List
- `search` - Search in title, content, and tags
- `author` - Filter by author ID
- `is_published` - Filter by publication status
- `ordering` - Sort by: `created_at`, `updated_at`, `title` (prefix with `-` for descending)

## Response Examples

### Successful Login Response
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2025-01-15T10:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### Blog Post Response
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content...",
  "author": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "is_published": true,
  "tags": "django, python, api",
  "tag_list": ["django", "python", "api"]
}
```

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to manage users and blog posts through a web interface.

## Project Structure

```
blog-python/
├── accounts/           # User authentication app
├── blog/              # Blog functionality app
├── blog_project/      # Main project settings
├── manage.py
├── requirements.txt
└── README.md
```

## Technologies Used

- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - API framework
- **SimpleJWT 5.3.0** - JWT authentication
- **django-cors-headers** - CORS handling
- **django-filter** - Advanced filtering
- **python-decouple** - Environment variables

## License

This project is open source and available under the [MIT License](LICENSE).