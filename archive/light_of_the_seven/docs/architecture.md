# Grid Architecture Documentation

## Overview

Grid is a unified development environment that combines a structured Python framework with software development templates. It follows a layered architecture pattern with clear separation of concerns, promoting maintainability, testability, and scalability.

## Architectural Layers

### 1. Core Layer (`src/core/`)

The foundation of the framework providing essential services:

- **Application Management**: Lifecycle management and startup/shutdown hooks
- **Configuration**: Type-safe configuration with environment variable support
- **Dependency Injection**: Service container for managing dependencies
- **Logging**: Structured logging with multiple output formats
- **Security**: Authentication, authorization, and cryptographic utilities
- **Exceptions**: Custom exception hierarchy for error handling

### 2. API Layer (`src/api/`)

Web interface layer built on FastAPI:

- **Server**: FastAPI application factory with middleware configuration
- **Routers**: API endpoint definitions organized by domain
- **Dependencies**: FastAPI dependency injection for request handling
- **Middleware**: Request logging, CORS, security headers

### 3. Database Layer (`src/database/`)

Data persistence layer using SQLAlchemy:

- **Models**: ORM models representing database entities
- **Sessions**: Database connection and transaction management
- **Migrations**: Schema versioning and migration system

### 4. CLI Layer (`src/cli/`)

Command-line interface for application management:

- **Commands**: Server management, testing, linting, database operations
- **Rich Output**: Formatted console output using Rich library

### 5. Service Layer (`src/services/`)

Business logic layer:

- **NER Service**: Named entity recognition and extraction
- **Pattern Engine**: Pattern recognition using Grid cognition patterns
- **Rules Engine**: Competitor detection and anomaly identification
- **Scenario Analyzer**: Context-based player detection
- **Relationship Analyzer**: Relationship judgment (friend/foe/neutral) analysis

### 6. Utility Layer (`src/utils/`)

Helper functions and utilities (placeholder for implementation):

- **Common Functions**: Reusable utility functions
- **Helpers**: Domain-specific helper classes

## Core Patterns

### Builder Pattern
The application uses the **Builder Pattern** (`src/core/builder.py`) for initialization. This decouples the construction of the `FastAPI` application from its configuration, allowing for flexible assembly of:
- Settings
- Routers
- Middleware
- Lifespan contexts

### Dependency Inversion
We follow **Clean Architecture** principles. High-level modules depend on abstractions (defined in `src/core/interfaces.py`), not concrete implementations.
- **Interfaces**: `IDatabase`, `IEmailService`, `ILogger`, `IVisionService`
- **Injection**: Dependencies are wired up during the Build phase.

## Design Patterns

### Dependency Injection

The framework uses a simple dependency injection container:

```python
# Service registration
container.register_singleton(DatabaseService, DatabaseService())
container.register_transient(UserService, UserService)

# Service resolution
db_service = container.get(DatabaseService)
user_service = container.get(UserService)
```

### Factory Pattern

FastAPI application factory for creating configured instances:

```python
def create_app() -> FastAPI:
    app = FastAPI(...)
    configure_middleware(app)
    include_routers(app)
    return app
```

### Repository Pattern

Database access through repository classes (to be implemented):

```python
class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
```

### Service Provider Pattern

Service providers for organizing service registration:

```python
class DatabaseServiceProvider(ServiceProvider):
    def register(self, container: Container) -> None:
        container.register_singleton(Session, create_db_session)
        container.register_transient(UserRepository, UserRepository)
```

## Data Flow

### Request Flow

1. **Request Reception**: FastAPI receives HTTP request
2. **Middleware Processing**: Logging, CORS, security headers
3. **Route Matching**: FastAPI matches request to route handler
4. **Dependency Resolution**: FastAPI resolves dependencies
5. **Business Logic**: Service layer processes request
6. **Database Operations**: Repository layer handles data access
7. **Response Generation**: Response created and sent through middleware

### NER System Pipeline

The NER system follows this processing pipeline:

```
Input Event → NER Service → Entity Extraction → Relationship Extraction →
Pattern Engine → Relationship Analyzer → Scenario Analyzer → Output
```

**Relationship Analyzer** computes relationship judgments by:
1. Extracting contextual features (history, emotions, triggers, risk, etc.)
2. Computing numeric polarity score (-1.0 to +1.0)
3. Classifying relationship label (supportive, cooperative, neutral, competitive, adversarial, manipulative, ambiguous)
4. Calculating confidence and generating explanations

See `relationship_analyzer_design.md` for detailed design.

### Application Startup Flow

1. **Configuration Loading**: Environment variables and settings loaded
2. **Container Setup**: Dependency injection container configured
3. **Database Initialization**: Connection established and migrations run
4. **Service Registration**: All services registered in container
5. **Server Start**: FastAPI server starts listening for requests

## Configuration Management

### Environment-Based Configuration

The framework supports multiple environments:

- **Development**: Debug mode enabled, verbose logging
- **Staging**: Production-like settings with debug features
- **Production**: Optimized for performance and security

### Configuration Hierarchy

1. Default values in code
2. Environment variables
3. `.env` file values
4. Runtime overrides (CLI arguments)

## Security Architecture

### Authentication Flow

1. **Login Request**: User provides credentials
2. **Credential Validation**: Password verified against hash
3. **Token Generation**: JWT access and refresh tokens created
4. **Token Storage**: Tokens stored securely on client
5. **Authenticated Requests**: Access token sent in Authorization header

### Authorization Model

- **Role-Based Access Control**: Users assigned roles/permissions
- **Resource-Based Authorization**: Permissions checked per resource
- **JWT Claims**: User identity and permissions encoded in token

## Error Handling Strategy

### Exception Hierarchy

```
FrameworkException
├── ConfigurationError
├── DatabaseError
├── ValidationError
├── AuthenticationError
├── AuthorizationError
├── NotFoundError
├── ConflictError
├── RateLimitError
└── ExternalServiceError
```

### Error Response Format

```json
{
  "error": "ValidationError",
  "message": "Invalid request data",
  "error_code": "VALIDATION_FAILED",
  "details": {
    "field": "email",
    "issue": "Invalid format"
  }
}
```

## Testing Strategy

### Test Types

- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **API Tests**: Endpoint testing with HTTP requests
- **Database Tests**: Repository and model testing

### Test Organization

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Slower, component tests
├── conftest.py     # Shared fixtures and configuration
└── fixtures/       # Test data and utilities
```

## Performance Considerations

### Database Optimization

- **Connection Pooling**: Reuse database connections
- **Query Optimization**: Efficient queries with proper indexing
- **Caching**: Redis integration for frequently accessed data

### API Performance

- **Async Processing**: Non-blocking request handling
- **Response Compression**: Gzip compression for large responses
- **Rate Limiting**: Prevent abuse and ensure fair usage

### Memory Management

- **Dependency Lifecycle**: Proper service lifecycle management
- **Resource Cleanup**: Automatic cleanup of database connections
- **Lazy Loading**: Load resources only when needed

## Scalability Patterns

### Horizontal Scaling

- **Stateless Design**: Services designed to be stateless
- **Load Balancing**: Multiple server instances behind load balancer
- **Database Sharding**: Partition data across multiple databases

### Vertical Scaling

- **Resource Optimization**: Efficient resource utilization
- **Caching Layers**: Multiple levels of caching
- **Background Processing**: Async task processing with Celery

## Monitoring and Observability

### Logging Strategy

- **Structured Logging**: JSON-formatted logs with context
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation**: Automatic log file rotation and retention

### Health Checks

- **Application Health**: Basic application status
- **Dependency Health**: Database and external service status
- **Resource Health**: Memory, CPU, and disk usage

### Metrics Collection

- **Request Metrics**: Response times, error rates
- **Business Metrics**: User activity, feature usage
- **System Metrics**: Resource utilization

## Deployment Architecture

### Container Strategy

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["python", "-m", "src.cli.main", "serve"]
```

### Environment Configuration

- **Development**: Local development with hot reload
- **Staging**: Pre-production testing environment
- **Production**: Optimized for security and performance

## Future Enhancements

### Planned Features

- **GraphQL Support**: GraphQL API endpoint
- **WebSocket Support**: Real-time communication
- **Event System**: Event-driven architecture
- **Plugin System**: Extensible plugin architecture
- **Multi-tenancy**: Support for multiple organizations

### Technology Roadmap

- **Message Queues**: RabbitMQ or Apache Kafka integration
- **Search Engine**: Elasticsearch integration
- **File Storage**: S3 or MinIO integration
- **Monitoring**: Prometheus and Grafana integration
