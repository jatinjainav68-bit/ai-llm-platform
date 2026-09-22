# AI/LLM Platform API

A production-style AI/LLM backend API built with FastAPI. The project provides JWT authentication, LLM-powered chat, Redis caching, PostgreSQL database persistence, token/latency tracking, Docker configuration, error handling with retries, and automated tests.

---

## Features

- FastAPI REST API
- JWT authentication
- Protected `/chat` endpoint
- OpenAI LLM integration
- Redis caching
- PostgreSQL database integration
- Chat history persistence
- Input/output/total token tracking
- LLM response latency tracking
- Error handling and retry mechanism
- Docker and Docker Compose configuration
- Health check endpoint
- Metrics endpoint
- Automated tests with pytest
- Interactive Swagger API documentation

---

## Architecture

```text
                         Client
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |     API     |
                    +-------------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
      JWT Authentication            /chat Endpoint
                                         |
                                         v
                                  +-------------+
                                  | Redis Cache |
                                  +-------------+
                                         |
                              Cache HIT    |    Cache MISS
                                  |        |
                                  |        v
                                  |   +------------+
                                  |   | OpenAI LLM |
                                  |   +------------+
                                  |        |
                                  +--------+
                                         |
                                         v
                                  PostgreSQL DB
                                         |
                                         v
                                  Chat Metrics
                              - Input tokens
                              - Output tokens
                              - Total tokens
                              - Latency