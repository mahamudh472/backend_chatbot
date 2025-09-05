# AI Chatbot Backend with RAG Pipeline

A comprehensive Django REST Framework-based backend service for an AI chatbot that implements Retrieval-Augmented Generation (RAG) pipeline, JWT-based user authentication, persistent chat history storage, and automated background task scheduling.

## � Table of Contents

- [🚀 Features](#-features)
- [🛠 Technologies Used](#-technologies-used)
- [📁 Project Structure](#-project-structure)
- [🔧 Setup Instructions](#-setup-instructions)
- [📚 API Documentation](#-api-documentation)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Chat Endpoints](#chat-endpoints)
  - [System Information Endpoints](#system-information-endpoints)
- [🔍 Advanced RAG Pipeline Implementation](#-advanced-rag-pipeline-implementation)
- [🗄️ Database Schema and Model Structure](#️-database-schema-and-model-structure)
- [🔐 JWT Authentication Implementation](#-jwt-authentication-implementation)
- [🤖 AI Response Generation Process](#-ai-response-generation-process)
- [⏰ Background Task Implementation](#-background-task-implementation)
- [🧪 Testing Strategy](#-testing-strategy)
- [🔌 External Service Integration](#-external-service-integration)
- [🚀 Future Scalability and Advanced Features](#-future-scalability-and-advanced-features)
- [🛠️ Management Commands](#️-management-commands)
- [🔒 Security Implementation](#-security-implementation)
- [⚠️ Current Limitations & Production Notes](#️-current-limitations--production-notes)
- [🔮 Technology Upgrade Path](#-technology-upgrade-path)
- [📞 Support & Documentation](#-support--documentation)

## �🚀 Features

- **User Authentication**: Complete JWT-based authentication system with signup, login, and token refresh
- **Advanced RAG Pipeline**: Intelligent document chunking with FAISS vector search and context-aware AI responses
- **Chat History Management**: Persistent storage and retrieval of user conversations with automatic cleanup
- **Background Task Scheduling**: APScheduler-powered automated maintenance tasks
- **Smart Document Processing**: Configurable text chunking with overlap strategies for optimal context retrieval
- **Multi-Provider AI Support**: Priority-based AI provider system (Google Gemini primary, OpenAI fallback)
- **Management Commands**: Built-in Django commands for vector store rebuilding and system maintenance
- **Email Integration**: User verification email system (configurable)


## 🛠 Technologies Used

### Backend Framework
- **Django 5.2.6**: Web framework with robust ORM and admin interface
- **Django REST Framework 3.16.1**: Powerful API development toolkit

### Database
- **SQLite**: Default database for development (easily configurable for PostgreSQL/MySQL in production)

### Authentication & Security
- **djangorestframework-simplejwt 5.5.1**: JWT token-based authentication
- **Django User Model**: Built-in user management with username, email, and password hashing

### AI & Machine Learning
- **Google Generative AI 0.8.5**: 
  - **Primary Chat Model**: `gemini-1.5-flash` - Fast, efficient responses
  - **Embedding Model**: `embedding-001` - High-quality text embeddings
- **OpenAI 1.105.0**: Fallback AI provider via OpenRouter API
  - **Chat Model**: `gpt-4o-mini` - Cost-effective backup option
  - **Embedding Model**: `text-embedding-3-small` - Alternative embeddings
- **FAISS CPU 1.12.0**: Fast vector similarity search and clustering
- **NumPy 2.3.2**: Efficient numerical operations for embeddings

### Background Processing
- **APScheduler 3.11.0**: Advanced Python scheduler for background tasks
- **django-apscheduler 0.7.0**: Django integration for persistent job storage

### Development & Utilities
- **python-dotenv 1.1.1**: Environment variable management
- **httpx 0.28.1**: Modern async HTTP client
- **requests 2.32.5**: HTTP library for external API calls
- **tqdm 4.67.1**: Progress bars for long-running operations
## 📁 Project Structure

```
backend_chatbot/
├── backend_chatbot/          # Main Django project configuration
│   ├── settings.py          # Django settings and configuration
│   ├── urls.py             # Root URL routing and API endpoints
│   ├── wsgi.py             # WSGI configuration for deployment
│   └── asgi.py             # ASGI configuration for async support
├── chat/                   # Core chat application
│   ├── models.py          # ChatMessage model for database schema
│   ├── views.py           # API views (chat, history, vector stats)
│   ├── serializers.py     # DRF serializers for data validation
│   ├── ai_client.py       # Unified AI client with provider priority
│   ├── vectorstore.py     # FAISS vector search with document chunking
│   ├── gemini_client.py   # Google Gemini API integration
│   ├── openai_client.py   # OpenAI API integration (fallback)
│   ├── scheduler.py       # Background task definitions
│   ├── signals.py         # Django signals for auto-scheduler startup
│   └── management/        # Django management commands
│       └── commands/
│           ├── rebuild_vectorstore.py  # Vector store rebuild utility
│           └── check_ai_status.py      # AI provider status checker
├── users/                 # User authentication system
│   ├── views.py          # Signup, login, and JWT token views
│   └── models.py         # User-related models (Django's built-in)
├── documents/            # Knowledge base document storage
│   ├── api_docs_001.txt         # API documentation
│   ├── company_history_001.txt  # Company background
│   ├── hr_policy_001.txt        # HR policies
│   ├── product_spec_001.txt     # Product specifications
│   ├── support_ticket_001.txt   # Support examples
│   └── [8 more .txt files]     # Additional knowledge base files
├── env/                  # Python virtual environment
├── db.sqlite3           # SQLite database file
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies list
├── test_ai_client.py    # AI client testing script
└── .env                # Environment variables (create manually)
```

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend_chatbot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root with your API keys:
   ```env
   # Primary AI Provider (Google Gemini)
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Fallback AI Provider (OpenAI via OpenRouter)
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   
   # Email Configuration (optional, for user verification)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

   **API Key Priority**: The system uses Google Gemini as the primary provider and automatically falls back to OpenAI if Gemini is unavailable.

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Build Vector Store**
   Load and process the knowledge base documents:
   ```bash
   python manage.py rebuild_vectorstore --show-stats
   ```

7. **Test AI Client Configuration**
   Verify your AI provider setup:
   ```bash
   python test_ai_client.py
   ```

8. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/
```

### Authentication Endpoints

#### User Signup
Creates a new user account and sends verification email.

- **URL**: `POST /signup/`
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123"
  }
  ```
- **Success Response** (201):
  ```json
  {
    "success": true,
    "message": "User signed up successfully",
    "user": {
      "username": "john_doe",
      "email": "john@example.com"
    }
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Username or email already exists
  - `400 Bad Request`: Invalid or missing required fields

#### User Login
Authenticates user and returns JWT tokens.

- **URL**: `POST /login/`
- **Request Body** (supports both username and email):
  ```json
  {
    "username": "john_doe",  // or "email": "john@example.com"
    "password": "secure_password123"
  }
  ```
- **Success Response** (200):
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Error Response** (401):
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

#### JWT Token Refresh
Refreshes the access token using a valid refresh token.

- **URL**: `POST /token/refresh/`
- **Request Body**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Success Response** (200):
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

### Chat Endpoints

#### Get Chat History
Retrieves all chat messages for the authenticated user.

- **URL**: `GET /chat-history/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Success Response** (200):
  ```json
  [
    {
      "id": 1,
      "user": "john_doe",
      "message": "What is the company's mission?",
      "response": "Our company's mission is to provide...",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
  ```

#### Send Chat Message
Sends a message to the AI chatbot and receives a response using RAG pipeline.

- **URL**: `POST /chat/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "message": "What are the company's remote work policies?"
  }
  ```
- **Success Response** (200):
  ```json
  {
    "response": "Based on our HR policy documents, the company supports flexible remote work arrangements...",
    "provider": "Google Gemini"
  }
  ```
- **Error Response** (400):
  ```json
  {
    "error": "Message content is required"
  }
  ```

### System Information Endpoints

#### Vector Store Statistics
Returns information about the loaded knowledge base.

- **URL**: `GET /vectorstore/stats/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Success Response** (200):
  ```json
  {
    "total_chunks": 21,
    "total_files": 10,
    "files": [
      "api_docs_001.txt",
      "hr_policy_001.txt",
      "company_history_001.txt"
    ]
  }
  ```

#### AI Provider Status
Shows the status and configuration of available AI providers.

- **URL**: `GET /ai/status/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Success Response** (200):
  ```json
  {
    "active_provider": "Google Gemini",
    "google_available": true,
    "openai_available": false,
    "providers": {
      "google": {
        "chat_model": "gemini-1.5-flash",
        "embedding_model": "embedding-001"
      },
      "openai": {
        "chat_model": "gpt-4o-mini",
        "embedding_model": "text-embedding-3-small"
      }
    }
  }
  ```

## 🔍 Advanced RAG Pipeline Implementation

### How RAG Pipeline Integration Works

The RAG (Retrieval-Augmented Generation) pipeline in this project combines document retrieval with AI generation to provide contextually accurate responses:

1. **Document Processing**: All text documents in the `documents/` folder are automatically processed and split into intelligent chunks
2. **Vector Embedding**: Each chunk is converted to vector embeddings using Google's `embedding-001` model
3. **Vector Storage**: FAISS IndexFlatL2 stores embeddings for fast similarity search
4. **Query Processing**: User queries are embedded and matched against document chunks
5. **Context Assembly**: Top-k relevant chunks are retrieved and combined with metadata
6. **AI Generation**: The assembled context is fed to the AI model (Gemini-1.5-flash) for response generation

### Document Retrieval's Role in Response Generation

Document retrieval plays a crucial role in ensuring accurate, contextually relevant responses:

- **Precision**: Instead of using entire documents, the system retrieves only the most relevant chunks
- **Context Quality**: Multiple focused chunks provide comprehensive context without overwhelming the AI model
- **Source Attribution**: Responses include metadata about which documents and chunks were used
- **Fallback Handling**: If no relevant documents are found, the AI provides a general response indicating limited context

### Document Chunking Strategy

The system uses intelligent document chunking for optimal retrieval:

```python
# Configurable chunking parameters
chunk_size = 500        # characters per chunk
chunk_overlap = 50      # characters of overlap between chunks
```

**Benefits of Chunking**:
- **Better Precision**: Retrieve specific sections rather than entire documents
- **Improved Context**: Multiple relevant chunks provide comprehensive answers
- **Sentence Boundary Preservation**: Chunks split at natural sentence boundaries
- **Metadata Tracking**: Each chunk includes filename, position, and relevance scores

### Vector Store Management
```bash
# Rebuild vector store with default settings (500 char chunks, 50 char overlap)
python manage.py rebuild_vectorstore --show-stats

# Custom chunk sizes for different use cases
python manage.py rebuild_vectorstore --chunk-size=300 --chunk-overlap=30

# Larger chunks for more context
python manage.py rebuild_vectorstore --chunk-size=800 --chunk-overlap=100
```

### Benefits of Chunking
- **Better Precision**: Retrieve only relevant sections instead of entire documents
- **Improved Context Quality**: Multiple focused chunks provide comprehensive answers
- **Enhanced Performance**: Faster embedding generation and search
- **Configurable Strategy**: Adjustable chunk sizes for different document types
- **Overlap Prevention**: Smart overlap ensures no information loss at boundaries

## 🗄️ Database Schema and Model Structure

### Database Choice and Reasoning

**SQLite** is used for development with easy migration path to PostgreSQL/MySQL for production:

**Why SQLite for Development:**
- **Zero Configuration**: No additional setup required
- **Lightweight**: Perfect for development and testing
- **File-based**: Easy backup and sharing
- **Django ORM Compatibility**: Seamless integration with Django

**Production Considerations**: The schema is designed to easily migrate to PostgreSQL or MySQL by simply changing the database configuration in `settings.py`.

### ChatMessage Model Structure

```python
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to Django User
    message = models.TextField()                              # User's input message
    response = models.TextField()                             # AI-generated response
    created_at = models.DateTimeField(auto_now_add=True)      # Automatic timestamp
```

**Model Design Decisions:**
- **Foreign Key to User**: Ensures messages are tied to specific users with cascade deletion
- **TextField for Messages**: Handles variable-length content without size limitations
- **Auto Timestamp**: Automatic creation time tracking for history and cleanup
- **Simple Structure**: Optimized for performance and easy querying

### User Authentication Model

Uses Django's built-in User model with:
- **username**: Unique identifier for login
- **email**: Alternative login method and communication
- **password**: Hashed using Django's PBKDF2 algorithm
- **Additional fields**: first_name, last_name, is_active, date_joined

## 🔐 JWT Authentication Implementation

### JWT Security Approach

The authentication system uses **djangorestframework-simplejwt** with the following security measures:

```python
# JWT Configuration in settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

### Security Measures Implemented

1. **Password Security**:
   - Django's built-in PBKDF2 password hashing
   - Automatic salt generation
   - Configurable hash iterations for security scaling

2. **JWT Token Security**:
   - Short-lived access tokens (5 minutes) minimize exposure risk
   - Rotating refresh tokens prevent token reuse
   - Stateless authentication reduces server-side session vulnerabilities

3. **API Endpoint Protection**:
   - All chat endpoints require valid JWT authentication
   - Token validation on every request
   - Automatic token expiration handling

4. **Input Validation**:
   - Django REST Framework serializers validate all input data
   - SQL injection protection through Django ORM
   - XSS protection through proper data serialization

### Authentication Flow

1. **Signup**: User creates account with username, email, password
2. **Login**: Returns access token (5 min) and refresh token (1 day)
3. **API Access**: Access token required in Authorization header
4. **Token Refresh**: Use refresh token to get new access token
5. **Auto-expiry**: Tokens automatically expire for security

## 🤖 AI Response Generation Process

### Multi-Provider AI Architecture

The system implements a priority-based AI provider system:

**Priority Order: Google Gemini > OpenAI**

```python
# AI Client Priority Logic
if google_available:
    use_gemini_for_response()
elif openai_available:
    fallback_to_openai()
else:
    raise_no_provider_error()
```

### Response Generation with Retrieved Context

1. **Context Preparation**: Retrieved document chunks are formatted with metadata:
   ```
   (from hr_policy_001.txt, part 2/5):
   Remote work is supported with manager approval...
   
   ---
   
   (from company_history_001.txt, part 1/3):
   Our company was founded in 2020...
   ```

2. **AI Model Processing**: The formatted context + user query is sent to:
   - **Primary**: Google Gemini-1.5-flash (fast, efficient)
   - **Fallback**: OpenAI GPT-4o-mini via OpenRouter (cost-effective)

3. **Response Integration**: AI generates responses that:
   - Reference specific document sections
   - Maintain conversational tone
   - Provide accurate, contextual information
   - Include source attribution when relevant

### Model Selection Reasoning

- **Google Gemini-1.5-flash**: Primary choice for fast, high-quality responses
- **OpenAI GPT-4o-mini**: Cost-effective fallback with good performance
- **Automatic Fallback**: Ensures system reliability even if primary provider fails

## ⏰ Background Task Implementation

### APScheduler Integration

Background tasks are managed using **APScheduler** with Django integration:

```python
# Task Scheduler Configuration
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
```

### Implemented Background Tasks

1. **Chat History Cleanup**:
   ```python
   scheduler.add_job(
       cleanup_old_messages,
       'interval',
       days=1,  # Runs daily
       id='cleanup_old_messages',
       replace_existing=True
   )
   ```
   - **Purpose**: Automatically deletes chat messages older than 30 days
   - **Frequency**: Daily at application startup + 24-hour intervals
   - **Implementation**: Queries database for messages beyond threshold date

2. **Email Verification Task**:
   ```python
   def send_verification_emails():
       # Placeholder for email verification functionality
       print("Sending verification emails...")
   ```
   - **Status**: Framework implemented, functionality placeholder
   - **Purpose**: Send verification emails to new users
   - **Integration**: Triggered after user signup

### Task Persistence and Management

- **Database Storage**: Jobs stored in Django database via `django-apscheduler`
- **Auto-restart**: Scheduler automatically starts with Django application
- **Signal Integration**: Django signals ensure scheduler starts on app ready
- **Error Handling**: Jobs continue running even if individual tasks fail

### Task Monitoring

```bash
# Check scheduler status
python manage.py check_ai_status

# View scheduled jobs in Django admin
python manage.py runserver
# Navigate to /admin/ -> Django APScheduler -> Scheduled Jobs
```

## 🧪 Testing Strategy

### Testing Approaches Implemented

1. **API Endpoint Testing**:
   - Manual testing with tools like Postman or curl
   - Authentication flow verification (signup → login → API access)
   - Error handling validation for invalid inputs

2. **AI Provider Testing**:
   ```bash
   # Dedicated test script for AI functionality
   python test_ai_client.py
   ```
   - Tests both Google Gemini and OpenAI providers
   - Validates embedding generation
   - Verifies chat response generation
   - Checks provider fallback mechanism

3. **RAG Pipeline Testing**:
   - **Document Chunking**: Vector store rebuild with different parameters
   - **Retrieval Quality**: Query testing against known document content
   - **Context Assembly**: Multi-chunk retrieval verification
   - **Response Accuracy**: AI response quality with retrieved context

4. **Background Task Testing**:
   - Scheduler startup verification
   - Job execution monitoring
   - Database cleanup task validation

### Test Cases Covered

1. **Authentication Tests**:
   - Valid signup with unique username/email
   - Duplicate username/email rejection
   - Successful login with username or email
   - Invalid credential handling
   - JWT token refresh functionality

2. **Chat Functionality Tests**:
   - Query with matching documents → relevant context + AI response
   - Query with no matching documents → general AI response
   - Empty message handling
   - Unauthorized access prevention

3. **RAG Pipeline Tests**:
   - Vector store statistics endpoint
   - Document chunking with different sizes
   - Embedding generation for various text types
   - Search functionality with relevance scoring

## 🔌 External Service Integration

### AI Service APIs

1. **Google Generative AI**:
   ```python
   # Configuration
   GOOGLE_API_KEY = "your_api_key"
   
   # Models Used
   - Chat: "gemini-1.5-flash"
   - Embeddings: "embedding-001"
   ```
   - **Setup**: Requires Google AI Studio API key
   - **Usage**: Primary provider for chat and embeddings
   - **Rate Limits**: Handled with appropriate retry logic

2. **OpenAI via OpenRouter**:
   ```python
   # Configuration
   OPENROUTER_API_KEY = "your_api_key"
   
   # Models Used
   - Chat: "gpt-4o-mini" 
   - Embeddings: "text-embedding-3-small"
   ```
   - **Setup**: Requires OpenRouter account and API key
   - **Usage**: Fallback provider when Google is unavailable
   - **Cost**: More cost-effective through OpenRouter

### Email Service Integration

```python
# Email Configuration (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

- **Purpose**: User verification emails after signup
- **Status**: Framework implemented, full functionality pending
- **Configuration**: Supports Gmail, custom SMTP, or other providers

### Vector Search Integration

- **FAISS Library**: Fast, efficient vector similarity search
- **Configuration**: No external service required (local processing)
- **Storage**: In-memory vector index with disk serialization capability

## 🚀 Future Scalability and Advanced Features

### Planned Advanced Features

1. **Real-time Knowledge Base Updates**:
   - **File Watcher**: Monitor documents folder for changes
   - **Incremental Updates**: Add/update vectors without full rebuild
   - **API Endpoints**: Allow programmatic document management
   - **Version Control**: Track document changes and version history

2. **Multi-user Chat Sessions**:
   - **Session Management**: Multiple conversation threads per user
   - **Session Persistence**: Long-term conversation context
   - **Shared Sessions**: Collaborative chat capabilities
   - **Session Analytics**: Usage patterns and metrics

3. **Enhanced RAG Capabilities**:
   - **Semantic Chunking**: Structure-aware document splitting
   - **Query Rewriting**: Improve search query effectiveness
   - **Multi-modal Support**: Image and document processing
   - **Context Ranking**: Advanced relevance scoring algorithms

### Scalability Improvements

1. **Database Scaling**:
   ```python
   # Production Database Configuration
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'chatbot_prod',
           'HOST': 'db-cluster.amazonaws.com',
           # ... connection pooling, read replicas
       }
   }
   ```

2. **Vector Database Migration**:
   - **Pinecone**: Cloud-native vector database for large-scale search
   - **Weaviate**: Open-source vector database with GraphQL API
   - **Qdrant**: High-performance vector search engine

3. **Microservices Architecture**:
   ```
   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │  Auth Service   │    │  Chat Service   │    │  RAG Service    │
   │  (User Mgmt)    │    │  (Conversations)│    │  (Doc Search)   │
   └─────────────────┘    └─────────────────┘    └─────────────────┘
            │                       │                       │
   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │  API Gateway    │    │  Message Queue  │    │  Vector Store   │
   │  (Load Balance) │    │  (Redis/RabbitMQ)│   │  (Pinecone)     │
   └─────────────────┘    └─────────────────┘    └─────────────────┘
   ```

4. **Performance Optimizations**:
   - **Redis Caching**: Cache frequent queries and responses
   - **Connection Pooling**: Database connection optimization
   - **CDN Integration**: Static asset delivery
   - **Response Compression**: API response optimization

### Development Roadmap

**Phase 1** (Current): Core functionality with SQLite and basic RAG
**Phase 2**: PostgreSQL migration, enhanced chunking, session management
**Phase 3**: Microservices architecture, cloud vector database
**Phase 4**: Real-time features, multi-modal support, advanced analytics

## ⏰ Background Tasks

### Scheduled Jobs
- **Cleanup Task**: Automatically deletes chat messages older than 30 days
- **Testing Job**: Demonstration job that runs every minute
- **Email Verification**: Placeholder for sending verification emails (not implemented)

### Task Management
- **APScheduler**: Handles job scheduling and execution
- **Django Integration**: Jobs are stored in Django's database via django-apscheduler
- **Auto-start**: Scheduler automatically starts with the Django application

## 🛠️ Management Commands

## 🛠️ Management Commands

### Vector Store Management

#### Rebuild Vector Store
Completely rebuilds the vector store with configurable chunking parameters:

```bash
# Basic rebuild with default settings (500 char chunks, 50 char overlap)
python manage.py rebuild_vectorstore

# Show detailed statistics after rebuild
python manage.py rebuild_vectorstore --show-stats

# Custom chunk configuration for different use cases
python manage.py rebuild_vectorstore --chunk-size=300 --chunk-overlap=30 --show-stats

# Larger chunks for documents requiring more context
python manage.py rebuild_vectorstore --chunk-size=800 --chunk-overlap=100
```

**Command Parameters:**
- `--chunk-size`: Size of each chunk in characters (default: 500)
- `--chunk-overlap`: Overlap between chunks in characters (default: 50)  
- `--show-stats`: Display detailed vector store statistics after rebuilding

**Example Output:**
```
Building vector store with chunk_size=500, chunk_overlap=50
Loading and chunking documents...
✓ Loaded and chunked: api_docs_001.txt (3 chunks)
✓ Loaded and chunked: hr_policy_001.txt (2 chunks)
✓ Loaded and chunked: company_history_001.txt (4 chunks)
...

Vector Store Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Total chunks: 21
📁 Total files: 10
📋 Files processed: api_docs_001.txt, hr_policy_001.txt, ...

✅ Vector store rebuilt successfully!

🔍 Testing search functionality...
Top 3 results for "company mission":
  1. company_history_001.txt (chunk 0, distance: 0.6874)
  2. company_history_001.txt (chunk 1, distance: 0.7404)
  3. hr_policy_001.txt (chunk 2, distance: 0.8156)
```

#### Check AI Status
Verifies AI provider configuration and connectivity:

```bash
python manage.py check_ai_status
```

**Output Example:**
```
=== AI Client Test ===
🤖 Active Provider: Google Gemini

Provider Status:
  ✅ google_available: True
  ❌ openai_available: False

=== Testing Embeddings ===
✅ Embedding generated successfully
   📏 Embedding dimensions: 768
   🔢 First 5 values: [0.1234, -0.5678, 0.9012, ...]

=== Testing Chat ===
✅ Chat response generated successfully
   💬 Response: Based on the provided context, our company's mission is to...
```

## 🔒 Security Implementation

### Authentication Security
- **JWT Tokens**: Stateless authentication with configurable token lifetimes
  - Access tokens: 5 minutes (minimal exposure window)
  - Refresh tokens: 1 day (balanced security and usability)
- **Password Security**: Django's PBKDF2 hashing with automatic salt generation
- **Token Rotation**: Refresh tokens are rotated on each use to prevent replay attacks
- **Input Validation**: DRF serializers validate all API inputs

### API Security
- **Authentication Required**: All chat and user-specific endpoints require valid JWT tokens
- **Error Handling**: Sanitized error responses that don't expose sensitive information
- **SQL Injection Protection**: Django ORM provides automatic query parameterization
- **XSS Protection**: Proper data serialization prevents cross-site scripting

### Production Security Considerations
```python
# Recommended production settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

## ⚠️ Current Limitations & Production Notes

### Development vs Production
This is a **development-ready** implementation that requires additional configuration for production:

1. **Database**: Currently uses SQLite; migrate to PostgreSQL for production
2. **Environment Variables**: Secure API key management needed
3. **CORS**: Cross-origin resource sharing not configured
4. **Rate Limiting**: API request rate limiting not implemented
5. **Logging**: Comprehensive logging system needed for production monitoring
6. **Error Handling**: Enhanced error handling and user feedback

### Known Technical Debt
- **Email Verification**: Framework exists but full implementation pending
- **Chat Persistence**: All messages are saved (comment suggests some issues were previously present)
- **API Documentation**: Consider adding OpenAPI/Swagger documentation
- **Unit Tests**: Comprehensive test suite needed for CI/CD

### Performance Considerations
- **Vector Store**: Currently in-memory; consider persistent storage for large datasets
- **Concurrent Users**: No connection pooling or caching implemented
- **File Upload**: No API for dynamic document management
- **Search Optimization**: No query caching or optimization

## 🔮 Technology Upgrade Path

### Immediate Improvements (Week 1-2)
- [ ] Add comprehensive unit and integration tests
- [ ] Implement API rate limiting with Django-ratelimit
- [ ] Add OpenAPI documentation with drf-spectacular
- [ ] Configure CORS for frontend integration
- [ ] Enhanced error logging and monitoring

### Short-term Enhancements (Month 1)
- [ ] PostgreSQL migration for production
- [ ] Redis caching for frequent queries
- [ ] Advanced vector store with Pinecone/Weaviate
- [ ] Real-time WebSocket support for chat
- [ ] Admin interface for document management

### Long-term Vision (Quarter 1)
- [ ] Microservices architecture
- [ ] Multi-session chat support
- [ ] Advanced RAG with semantic chunking
- [ ] Real-time knowledge base updates
- [ ] Analytics and monitoring dashboard

## 📞 Support & Documentation

### Getting Help
- **Project Documentation**: All implementation details in this README
- **API Testing**: Use the provided test script `python test_ai_client.py`
- **Management Commands**: Built-in help with `python manage.py help <command>`
- **Django Admin**: Access at `/admin/` for user and data management

### Additional Resources
- **Django Documentation**: https://docs.djangoproject.com/
- **DRF Documentation**: https://www.django-rest-framework.org/
- **Google AI Documentation**: https://ai.google.dev/docs
- **FAISS Documentation**: https://faiss.ai/
- **APScheduler Documentation**: https://apscheduler.readthedocs.io/

### Configuration Files
- **Environment**: `.env` file for API keys and settings
- **Dependencies**: `requirements.txt` for Python packages
- **Database**: `db.sqlite3` (created automatically)
- **Knowledge Base**: `documents/` folder with .txt files

---

**🎯 Project Status**: Development Ready
**🔧 Production Ready**: Requires additional security and performance configuration  
**📝 Last Updated**: Based on current implementation analysis

This backend provides a solid foundation for an AI chatbot with RAG capabilities and can be extended for production use with the recommended enhancements above.
