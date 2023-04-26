import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import (ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory, ConversationKGMemory)

llm = OpenAI(
    temperature=0, 
    openai_api_key=os.environ.get("OPENAI_API_TOKEN"),
    model_name='text-davinci-003'  # can be used with llms like 'gpt-3.5-turbo' 'text-davinci-003'
)

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
#from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import (ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory, ConversationKGMemory)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

#Langchain implementation
template = """Assistant is a large language model trained by OpenAI.
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    {history}
    Human: {human_input}
    Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "human_input"], 
    template=template
)


#llm = OpenAI(temperature=0)
conversation_with_summary = ConversationChain(
    llm=llm, 
    memory=ConversationSummaryMemory(llm=llm),
    verbose=True
)


#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)
    
    output = conversation_with_summary.predict(input = message['text'])   
    say(output)

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
@app.event("app_mention")
def handle_app_mention_events(body, logger,say):
    #test1
    AI_prompt = str(body['event']['blocks'][0]['elements'][0]['elements'][1]['text'])
    output = conversation_with_summary.predict(input = AI_prompt)
    say(output)
    logger.info(body)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()