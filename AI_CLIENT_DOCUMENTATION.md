# AI Client System Documentation

## Overview

The AI client system implements a prioritized approach for handling AI requests with automatic fallback support between Google Gemini and OpenAI providers.

## Priority System

**Priority Order: Google Gemini > OpenAI**

The system will always attempt to use Google Gemini first, and only fall back to OpenAI if:
1. Google API key is not configured
2. Google API request fails

## Configuration

### Environment Variables

Set these in your `.env` file:

```bash
# Google Gemini API Key (Primary)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI API Key (Fallback)
OPENAI_API_KEY=your_openai_api_key_here
```

### Supported Models

#### Google Gemini
- **Chat Model**: `gemini-1.5-flash`
- **Embedding Model**: `embedding-001`

#### OpenAI
- **Chat Model**: `gpt-4o-mini` (Latest cost-effective model)
- **Embedding Model**: `text-embedding-3-small`

## Usage

### Basic Usage

```python
from chat.ai_client import ai_client

# Generate embeddings
embedding = ai_client.embed_text("Your text here")

# Generate chat response with context
response = ai_client.chat_with_context(prompt, context)

# Check active provider
provider = ai_client.get_active_provider()
```

### Provider Status

```python
# Get detailed status information
status = ai_client.get_provider_status()
print(status)
# Output:
# {
#     "google_available": True,
#     "openai_available": False,
#     "active_provider": "Google Gemini",
#     "google_api_key_set": True,
#     "openai_api_key_set": False
# }
```

## API Endpoints

### Check AI Provider Status
```
GET /ai/status/
```

Returns information about available AI providers and which one is currently active.

### Chat with AI
```
POST /chat/
```

The response now includes which provider was used:
```json
{
    "response": "AI generated response",
    "provider": "Google Gemini"
}
```

## File Structure

```
chat/
├── ai_client.py          # Unified AI client with priority system
├── gemini_client.py      # Google Gemini implementation
├── openai_client.py      # OpenAI implementation
├── vectorstore.py        # Updated to use unified client
└── views.py              # Updated API endpoints
```

## Error Handling

The system includes comprehensive error handling:

1. **Provider Availability Check**: Validates API keys on initialization
2. **Graceful Fallback**: Automatically switches to backup provider on failure
3. **Detailed Logging**: Logs provider switches and errors
4. **User Feedback**: API responses include which provider was used

## Testing

Run the test script to verify the system:

```bash
python test_ai_client.py
```

This will test:
- Provider detection and priority
- Embedding generation
- Chat response generation
- Error handling

## Monitoring

Monitor which provider is being used through:

1. **API Response**: Each chat response includes the provider name
2. **Status Endpoint**: `/ai/status/` provides real-time status
3. **Logs**: Check application logs for provider switches and errors

## Best Practices

1. **Always set both API keys** for maximum reliability
2. **Monitor provider usage** to ensure optimal performance
3. **Check logs regularly** for any API issues or failures
4. **Test both providers** in your development environment

## Troubleshooting

### Common Issues

1. **No API keys configured**
   - Error: "No AI API keys configured"
   - Solution: Set at least one API key in environment variables

2. **Provider fails repeatedly**
   - Check API key validity
   - Verify network connectivity
   - Check API rate limits

3. **Unexpected provider switching**
   - Check logs for error messages
   - Verify primary provider (Google) API key is working

### Debug Commands

```python
# Check provider status
from chat.ai_client import ai_client
print(ai_client.get_provider_status())

# Test specific provider
try:
    response = ai_client.chat_with_context("test", "test context")
    print(f"Success with {ai_client.get_active_provider()}")
except Exception as e:
    print(f"Error: {e}")
```
