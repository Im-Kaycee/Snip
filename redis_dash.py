import redis
import time

# --- Redis connection ---
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# --- List of keys to monitor (one per user or IP) ---
keys = [
    "token_bucket:user_1",
    "token_bucket:user_2",
    "token_bucket:user_3",
]

MAX_TOKENS = 10  # max tokens in bucket (for display purposes)

def display_buckets():
    output = []
    for key in keys:
        data = r.get(key)
        if data:
            try:
                tokens_left, last_refill = map(float, data.split(":"))
            except ValueError:
                tokens_left = 0
        else:
            tokens_left = 0
        bar = "█" * int(tokens_left) + "-" * (MAX_TOKENS - int(tokens_left))
        output.append(f"{key}: [{bar}] {tokens_left:.1f} tokens")
    print("\033[H\033[J", end="")  # clear screen
    print("\n".join(output))

if __name__ == "__main__":
    try:
        while True:
            display_buckets()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting dashboard...")