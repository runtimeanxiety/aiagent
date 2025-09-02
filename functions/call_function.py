from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .write_file import write_file
from google.genai import types

WORKING_DIRECTORY = "./calculator"


def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call_part.name
    print(
        f"{'Calling' if verbose else ' - Calling'} function: {function_name}({function_call_part.args})"
    )

    if function_call_part.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_args = dict(function_call_part.args)
    function_args["working_directory"] = WORKING_DIRECTORY
    try:
        function_result = function_map[function_name](**function_args)
        response = {"result": function_result}
    except Exception as e:
        response = {"error": str(e)}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
