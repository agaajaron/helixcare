import json
from pathlib import Path

def load_demo_request():
    return json.loads(Path("examples/a2a_prior_auth_request.json").read_text())

def main():
    msg = load_demo_request()
    print("HelixCare demo A2A message")
    print(json.dumps(msg, indent=2))
    print("\nNext implementation step: wire this envelope to a NATS/Kafka/gRPC agent bus.")

if __name__ == "__main__":
    main()
