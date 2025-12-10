**Importing all the libraries & the gradio framework**
import gradio as gr
from smolagents import tool, ToolCallingAgent, CodeAgent
from smolagents.models import InferenceClientModel
from smolagents.models import OpenAIServerModel 

#Defining the LLM
model = OpenAIServerModel(
    model_id="meta-llama/llama-3.1-70b-instruct",
    api_key="API-KEY", 
    api_base="https://openrouter.ai/api/v1/"
)


#For accomplishing task now assigning tools 

@tool
def track_order(order_id: str) -> str:
    """
    Track the status of an order.
    Args:
        order_id (str): The ID of the order to track.
    Returns:
        str: A message indicating the current status of the order.
    """
    # In a real app, this would query a database or an API.
    print(f"Tool called: track_order with ID {order_id}")
    return f"🔍 Order {order_id} is in transit and will be delivered in 2 days."

@tool
def check_product_availability(product_name: str) -> str:
    """
    Check if a product is currently available.
    Args:
        product_name (str): The name of the product to check.
    Returns:
        str: A message indicating whether the product is in stock.
    """
    print(f"Tool called: check_product_availability for {product_name}")
    return f"✅ {product_name} is currently in stock."

@tool
def get_product_info(product_name: str) -> str:
    """
    Get information about a product.
    Args:
        product_name (str): The name of the product to get information about.
    Returns:
        str: A message containing details about the product.
    """
    print(f"Tool called: get_product_info for {product_name}")
    return f"📦 {product_name} is made of recycled aluminum and ships with a 1-year warranty."

#Assigning tool calling Agents


order_agent = ToolCallingAgent(
    name="OrderTrackingAgent",
    model=model,
    tools=[track_order],
    description="Handles queries related to tracking the status of customer orders."
)

product_agent = ToolCallingAgent(
    name="ProductAgent",
    model=model,
    tools=[check_product_availability, get_product_info],
    description="Manages queries about product availability and product information."
)

#The Manager Agents - Who handles the whole program :

manager_agent = CodeAgent(
    name="CustomerServiceManager",
    model=model,
    managed_agents=[
        order_agent,
        product_agent
    ],
    tools=[],  # No global tools for the manager in this case
    verbosity_level=2,
    max_steps=8
)

#Defining custom Prompts :
custom_system_prompt = (
    "You are a customer service manager assistant.\n"
    "Your job is to understand customer issues, determine which support agent to call, and handle the query end-to-end.\n"
    "Follow this format:\n"
    "Thought: Analyze the customer's input.\n"
    "Action: Call a tool or agent with arguments.\n"
    "Observation: Record the response.\n"
    "Repeat Thought/Action/Observation as needed until the issue is resolved."
)

manager_agent.prompt_templates["system_prompt"] += custom_system_prompt

#Defining function to handle the query of gradio

def handle_query(query: str) -> str:
    """
    Takes a user query, processes it with the manager agent, and returns the final response.
    """
    print(f"\n--- New Query Received ---\nQuery: {query}")
    if not query:
        return "Please enter a query."
    
    # The manager agent will coordinate the right specialist agent to solve the query.
    final_response = manager_agent.run(query)
    print("\nFINAL RESPONSE:\n", final_response)
    return final_response


# **CREATE AND LAUNCH GRADIO**
_The main func that includes suggesting pre available queries to customers ,Also specifing the interface & fianlly launching the WEB UI_

if __name__ == "__main__":
    
    example_queries = [
        "Hi, I ordered a phone case last week and still haven’t received it. Can you check order ID 789123?",
        "I'd like to know more about the 'Eco-Friendly Water Bottle'. Also, can you check if it's in stock?",
        "What is the status of my order #555-4321?",
        "Tell me about the 'Smart Notebook'.",
    ]
    
    #Create the Gradio interface
    demo = gr.Interface(
        fn=handle_query,
        inputs=gr.Textbox(lines=3, placeholder="Enter your customer service query here..."),
        outputs=gr.Textbox(label="Agent Response", lines=5),
        title="🤖 Customer Service Multi-Agent System",
        description="Ask about order tracking or product information. The manager agent will delegate your query to the correct specialist agent.",
        examples=example_queries,
        allow_flagging="never", # Disables the "Flag" button
    )
    
    # Launch the web UI
    print("Gradio UI is starting. Open the URL in your browser.")
    demo.launch()
