import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List the directory contents
- Get a file's contents
- Write file contents (don't overwrite anything important, maybe create a new file)
- Execute the calculator app's tests (tests.py)

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

verbose = "--verbose" in sys.argv
args = []
for arg in sys.argv[1:]:
    if not arg.startswith("--"):
        args.append(arg)

if not args:
    print("Usage: python main.py '<your prompt here>' [--verbose]")
    sys.exit(1)

user_prompt = " ".join(args)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

print(f"User prompt: {user_prompt}")
if response.function_calls:
    for fc in response.function_calls:
        fc_result = call_function(fc, verbose)

        if not fc_result.parts or not fc_result.parts[0].function_response:
            raise Exception("empty function call result")

        if verbose:
            print(f"-> {fc_result.parts[0].function_response.response}")
else:
    print(response.text)
