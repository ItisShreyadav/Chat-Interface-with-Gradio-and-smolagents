# Chat-Interface-with-Gradio-and-smolagents
Create a beautiful chat interface using gradio and smolagents.Must follow the smolagent boilerplate.
Reference - https://deepwiki.com/huggingface/smolagents/7.2-gradio-web-ui

@sneha Here is the takeaway : 

# Gradio Web UI and smolagents :

Gradio is the tool that helps us  build a chat interface right in our browser. Using smolagents together with Gradio means we  can chat with AI agents, upload files, and get real-time responses just like having a conversation.

## The Two Big Pieces /Components 

The Gradio Web UI is made up of two main parts:

1. The `GradioUI` class : It is like  the blueprint for our chat window.
2. The `stream_to_gradio()` function : This translates what the agent is thinking and doing into messages you see on screen.

Together, these parts handle the agent’s thinking process and send updates in real-time.

## What the GradioUI Class Does

This class connects AI agent to the Gradio web app. It lets us  see the conversation, upload files, and even reset the agent’s memory if we want  a fresh start.

When we  create a `GradioUI`, We can understand :

- Which agent to use (`agent`)
- Where to save uploaded files (`file_upload_folder`)
- If the agent should forget previous chats after each message (`reset_agent_memory`)

## Building the Chat Interface

The `create_app()` method puts together the Gradio chat window using these parts:

| What You See       | What It Does               | Gradio Component  |
|--------------------|----------------------------|-------------------|
| Sidebar            | Where you type and upload files | `gr.Sidebar`     |
| Text Input Box     | Where you enter your message | `gr.Textbox`      |
| Submit Button      | Click to send your message  | `gr.Button`       |
| File Upload Button | Upload PDFs, images, etc.   | `gr.File`         |
| Chat Window        | Where the conversation happens | `gr.Chatbot`    |

## Real-Time Thinking: Message Streaming - Thought Process 

Instead of waiting until the agent finishes thinking, we can  see the agent’s thoughts as they happen in the back:

- The agent breaks down the task into steps:
  1. Planning `_process_planning_step` : figuring out what to do
  2. Action `_process_action_step` : doing the work
  3. Final answer`_process_final_answer_step` : wrapping it all up

- The chat UI shows these steps as bubble messages one by one.
- It avoids duplicates and shows progress from “pending” to “done.”

## Uploading Files Safely - `upload_file()`

We can upload files like PDFs or images during the chat. The system:

- Cleans file names so nothing harmful gets through.
- Saves files securely so your agent can read them.
- Lets the agent check files to answer your questions better.

All this happens behind the scenes in the `upload_file()` method.

## How It All Works Together

Gradio handles the chat window, while the agent does the thinking and responding:

- The  messages and uploads go straight to the agent.
- The agent sends back updates step by step, so you see answers as they form.
- This happens in real time if streaming is enabled.

## Keeping Chats Unique with Sessions

Each user gets their own chat session with:

- A separate agent instance, so you don’t get mixed up with anyone else.
- Your own conversation history to keep answers relevant.
- Your uploaded files tracked for your session only.

This makes every interaction smooth and private.


# Integration with Agents
The Gradio UI works like a friendly chat window that talks with an AI agent doing several steps behind the scenes to help answer questions or complete tasks. It can show you the agent’s progress live as it thinks (streaming mode) or wait until everything is done and then show the final answer all at once (non-streaming mode), making it easy for anyone to follow what's happening.

 ## Streaming Behavior

When `stream_outputs=True`, the system sends updates live as the agent processes your request. Instead of waiting for a full answer, you get small bits of the response as they’re ready.

Finished steps are gathered using `pull_messages_from_step()`, and the message status changes from "pending" to "done" once completed.

To avoid showing the same information twice, model outputs are skipped during streaming.

This makes it easy to follow what’s happening while the agent works.


## Example Code Setup
``` from smolagents import CodeAgent, GradioUI, InferenceClientModel

model = InferenceClientModel(model_id="meta-llama/Meta-Llama-3.1-8B-Instruct")
agent = CodeAgent(tools=[], model=model)
gradio_ui = GradioUI(agent, reset_agent_memory=False)
gradio_ui.launch()
```
# How to achieve the goal : Of integrating Gradio with smolagents :
```Integrating SmolAgents with Gradio lets us  create a friendly chat window powered by smart AI helpers. 
firstly set up SmolAgents to take care of different tasks behind the scenes. 
Then,  build a simple Gradio interface where people can ask questions and get answers.
 When someone types in a question, it’s sent to SmolAgents, which figures out the best response.
 Finally, Gradio shows this answer clearly, making the whole experience smooth and easy for users.
```
