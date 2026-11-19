from client import client
from config import MODEL

def setUp():
    print("Testing model:", MODEL)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Hello"}
        ],
        temperature=0.1
    )

    print("\nAI Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    setUp()

