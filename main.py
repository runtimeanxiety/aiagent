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

MAX_ITERATION = 20

for iteration in range(MAX_ITERATION):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
    except Exception as e:
        print(f"Error during generate_content (iteration {iteration+1}): {e}")

    for candidate in response.candidates:
        messages.append(candidate.content)

    if response.function_calls:
        for fc in response.function_calls:
            try:
                fc_result = call_function(fc, verbose)
            except Exception as e:
                print(f"Error during function call (iteration {iteration+1}): {e}")
                continue

            if not fc_result.parts or not fc_result.parts[0].function_response:
                print("empty function call result")
                continue

            if verbose:
                print(f"-> {fc_result.parts[0].function_response.response}")

            messages.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=fc_result.parts[0].function_response.name,
                            response=fc_result.parts[0].function_response.response,
                        )
                    ],
                )
            )
    elif hasattr(response, "text") and response.text:
        print(response.text)
        break
else:
    print("Max iterations reached without a final response.")
