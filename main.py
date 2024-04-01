import orjson
import ujson
import json
import timeit

def benchmark_json_encoders(data, num_iterations=10000):
    encoders = [
        ('orjson', lambda d: orjson.dumps(d, option=orjson.OPT_INDENT_2).decode()),
        ('ujson', lambda d: ujson.dumps(d, indent=2)),
        ('json', lambda d: json.dumps(d, indent=2)),
        ('orjson (non-pretty)', lambda d: orjson.dumps(d).decode()),
        ('ujson (non-pretty)', lambda d: ujson.dumps(d)),
        ('json (non-pretty)', lambda d: json.dumps(d))
    ]

    results = []
    for name, encoder in encoders:
        time = timeit.timeit(lambda: encoder(data), number=num_iterations)
        results.append((name, time))

    results.sort(key=lambda x: x[1])  # Sort by time
    for name, time in results:
        print(f"{name}: {time:.6f} seconds")
    return results[0][0]  # Return the name of the fastest encoder

# Test data
dummy_error = {
    "error": {
        "message": "You didn't provide an API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY). You can obtain an API key from https://platform.openai.com/account/api-keys.",
        "type": "invalid_request_error",
        "param": None,
        "code": None
    }
}

dummy_completion = {
    "id": "chatcmpl-KoshCsdIMDhX06fJeJCjpRurIGkPw",
    "object": "chat.completion",
    "created": 1711793678,
    "model": "gpt-4",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello! How can I assist you today?"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 9,
        "total_tokens": 19
    },
    "system_fingerprint": "fp_z5au7bncas"
}

# Benchmark
fastest_encoder_error = benchmark_json_encoders(dummy_error)
fastest_encoder_completion = benchmark_json_encoders(dummy_completion)

print(f"Fastest JSON encoder for dummy_error: {fastest_encoder_error}")
print(f"Fastest JSON encoder for dummy_completion: {fastest_encoder_completion}")
