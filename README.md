# API Data Collector

A Python automation project for collecting data from REST APIs, normalizing API responses, validating records, and generating structured CSV reports.

The application is designed to process large amounts of data reliably and can later be integrated with systems such as TeraFlowSDN and other REST API platforms.

## Project Goals

- Collect data from REST APIs
- Process large datasets through pagination
- Parse nested JSON safely
- Normalize different API response formats
- Validate required fields
- Generate CSV reports with fixed headers
- Generate a separate report for missing or invalid fields
- Retry requests after temporary API failures
- Support multiple API sources
- Run locally, in Docker, and as a Kubernetes CronJob


### API Collection

- REST API requests with `httpx` or `requests`
- Environment-based configuration
- Request timeouts
- Pagination
- Retry handling
- Exponential backoff
- Authentication support
- Structured logging
- Meaningful exit codes

### Data Processing

- Safe `.get()` parsing
- Nested JSON parsing
- Common data models
- Data normalization
- Required-field validation
- IP address validation
- Duplicate detection
- Streaming CSV export
- Missing-fields report

### Design Patterns

The following design patterns will be introduced where they solve a real problem:

- **Adapter Pattern** — normalize data from different API systems
- **Factory Pattern** — select the correct API adapter or exporter
- **Strategy Pattern** — support different export formats
- **Template Method** — define a common data collection workflow
- **Dependency Injection** — improve testability and separation of concerns
- **Observer Pattern** — connect logging, metrics, and notifications to collector events
