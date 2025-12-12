from google import genai

api_key= "AIzaSyDdOTwPHERq2o5MMyJniGqWULeNbOeHez"

client = genai.GenaiClient(api_key=api_key)

messages = [{"role":"user"}]

while true:
    user_input = input("YOU:")
    if user_input.lower == "exit":
        print("Goodbye")
        break
    messages.append({"role":"user"})
     response = client.models.generate_content_stream(
     model="gemini-2.5-flash"
     contents=user_input
)
    print("AI:",end="")
    full_replay = ""
    for chunk in response:
        full_reply += chunk.text
        print(full_reply, end="")

    messages.append({"role":"user","parts"})