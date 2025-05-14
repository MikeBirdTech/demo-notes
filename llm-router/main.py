import json
import os
from dotenv import load_dotenv
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel


# --- Mock Functions ---
def define_mcp_tool(service_name: str, tool_ideas: str, **kwargs):
    """MOCK: Defines tool signatures for a given service based on natural language ideas."""
    output_message = f"SUCCESS: Function 'define_mcp_tool_signatures_for_service' called. Tool signature definition process started for {service_name}. Tool ideas: '{tool_ideas}'."
    print(f"\n{output_message}\n")
    return json.dumps(
        {
            "status": "success",
            "message": output_message,
            "service": service_name,
            "tool_ideas_received": tool_ideas,
        },
        indent=2,
    )


def setup_project_environment(programming_language: str, **kwargs):
    """MOCK: Sets up the project environment, installs SDKs, creates basic file structure."""
    output_message = f"SUCCESS: Function 'setup_mcp_server_project_environment' called. Project environment setup initiated for {programming_language}."
    print(f"\n{output_message}\n")
    return json.dumps(
        {
            "status": "success",
            "message": output_message,
            "language": programming_language,
        },
        indent=2,
    )


def implement_external_api(service_name: str, tool_name: str, **kwargs):
    """MOCK: Implements the logic to call an external API for a specific MCP tool."""
    output_message = f"SUCCESS: Function 'implement_external_api_interaction_logic' called. API interaction logic implementation for {tool_name} (service: {service_name}) started."
    print(f"\n{output_message}\n")
    return json.dumps(
        {
            "status": "success",
            "message": output_message,
            "service": service_name,
            "tool": tool_name,
        },
        indent=2,
    )


def configure_server_auth(service_name: str, **kwargs):
    """MOCK: Configures authentication and security for interacting with an external service."""
    output_message = f"SUCCESS: Function 'configure_server_authentication_and_security' called. Auth and security configuration for {service_name} initiated."
    print(f"\n{output_message}\n")
    return json.dumps(
        {"status": "success", "message": output_message, "service": service_name},
        indent=2,
    )


# --- LLM Function Declarations (Global Configuration) ---
available_functions = [
    {
        "name": "define_mcp_tool_signatures_for_service",
        "description": "This is the absolute first function to call when a user states they want to 'make', 'create', or 'start' a new MCP server for any specific external service. It defines the core tools and functionalities the server will have. The user must provide the service name and at least a general idea of desired functionalities.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "service_name": {
                    "type": "STRING",
                    "description": "The external service the MCP server will connect to (e.g., 'Twitter', 'GitHub').",
                },
                "tool_ideas": {
                    "type": "STRING",
                    "description": "A natural language description of desired functionalities or tool ideas for this service (e.g., 'post tweets and search for users', or if not specified by user, a general goal like 'general interaction').",
                },
            },
            "required": ["service_name", "tool_ideas"],
        },
    },
    {
        "name": "setup_mcp_server_project_environment",
        "description": "Once initial tool ideas for a service are defined, or if the user asks generally about project setup without mentioning a service yet, call this. It handles choosing a language, installing SDKs, project directories, and basic file structure.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "programming_language": {
                    "type": "STRING",
                    "description": "The primary programming language for the server (e.g., 'Python', 'TypeScript').",
                }
            },
            "required": ["programming_language"],
        },
    },
    {
        "name": "implement_external_api_interaction_logic",
        "description": "Writes the actual code that interacts with an external service API to fulfill the action of a pre-defined MCP tool. Assumes tool signatures are already designed.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "service_name": {
                    "type": "STRING",
                    "description": "The name of the external service API being called (e.g., 'Twitter', 'Stripe').",
                },
                "tool_name": {
                    "type": "STRING",
                    "description": "The specific MCP tool being implemented (e.g., 'searchTweets', 'createPaymentIntent').",
                },
            },
            "required": ["service_name", "tool_name"],
        },
    },
    {
        "name": "configure_server_authentication_and_security",
        "description": "Dedicated to securely handling credentials (API keys, access tokens) and managing access for the MCP server when it needs to interact with a protected external service API.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "service_name": {
                    "type": "STRING",
                    "description": "The external service for which authentication is being configured (e.g., 'Twitter', 'AWS').",
                }
            },
            "required": ["service_name"],
        },
    },
]

# --- Function Mapping (Global Configuration) ---
FUNCTION_MAP = {
    "define_mcp_tool_signatures_for_service": define_mcp_tool,
    "setup_mcp_server_project_environment": setup_project_environment,
    "implement_external_api_interaction_logic": implement_external_api,
    "configure_server_authentication_and_security": configure_server_auth,
}

chat = None


# --- LLM Interaction Function ---
def get_llm_decision(user_input):
    """
    Sends the user input to the LLM and gets the function call decision.
    Uses the global 'chat' object initialized in main().
    """
    global chat
    if not chat:
        print("Error: Chat model not initialized. Please run the main() function.")
        return None, None

    try:
        enhanced_prompt = f"User request: '{user_input}'. Based on the available functions, choose the single most appropriate function and its arguments to fulfill this request."
        response = chat.send_message(
            enhanced_prompt,
            tools=available_functions,
            generation_config={"temperature": 0},
        )

        if hasattr(response, "candidates") and response.candidates:
            for candidate in response.candidates:
                if (
                    hasattr(candidate, "content")
                    and hasattr(candidate.content, "parts")
                    and candidate.content.parts
                ):
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call") and part.function_call:
                            function_name = part.function_call.name
                            args = (
                                dict(part.function_call.args)
                                if hasattr(part.function_call, "args")
                                else {}
                            )
                            return function_name, args

        response_text_to_print = (
            "Could not understand the request well enough to take a specific action."
        )
        if hasattr(response, "text") and response.text is not None:
            response_text_to_print = response.text
        print(f"\nAssistant: {response_text_to_print}")
        return None, None

    except Exception as e:
        print(f"\nError during LLM API call or response processing: {e}")
        if hasattr(e, "args") and e.args:
            print(f"Error details: {e.args}")
        return None, None


# --- Main Application Logic ---
def main():
    """Runs the main MCP QuickStart Assistant application."""
    global chat

    # --- LLM Router using Google Generative AI ---
    load_dotenv()
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file.")
        configure(api_key=api_key)
        print("Google Generative AI API configured successfully")
    except ValueError as e:
        print(f"API Key Error: {e}")
        print(
            "Please add GOOGLE_API_KEY to your .env file in the project root directory."
        )
        return
    except Exception as e:
        print(f"An unexpected error occurred during API configuration: {e}")
        return

    try:
        model = GenerativeModel("gemini-1.5-flash-latest")
        chat = model.start_chat()
        print("Successfully initialized Gemini model and chat session")
    except Exception as e:
        print(f"Error initializing model: {e}")
        return

    print("\nMCP QuickStart Assistant")
    print("I can help you with various stages of creating an MCP server.")
    print("Type your request, or 'quit' to exit.")
    print("-" * 60)

    while True:
        user_input = input("> ")
        if user_input.lower() in ["quit", "exit"]:
            break

        print(f"\nProcessing: '{user_input}'")
        chosen_function_name, arguments = get_llm_decision(user_input)

        if chosen_function_name:
            if chosen_function_name in FUNCTION_MAP:
                selected_function = FUNCTION_MAP[chosen_function_name]
                print(f"\nAssistant: Executing action: '{chosen_function_name}'...")
                try:
                    selected_function(**arguments)
                    print("-" * 60)
                except TypeError as te:
                    print(
                        f"\nAssistant Error: Problem calling function '{chosen_function_name}'."
                    )
                    print(f"Details: {te}")
                    print(
                        "Please ensure your request provides the necessary details for this action."
                    )
                    print("-" * 60)
                except Exception as e:
                    print(
                        f"\nAssistant Error: An unexpected error occurred while executing '{chosen_function_name}': {e}"
                    )
                    print("-" * 60)
            else:
                print(
                    f"\nAssistant Error: The system tried to run an unrecognized action: '{chosen_function_name}'."
                )
                print("-" * 60)
        else:
            print("-" * 60)

    print("Exiting MCP QuickStart Assistant.")


# --- Script Execution Guard ---
if __name__ == "__main__":
    main()
