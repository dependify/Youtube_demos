import autogen

config_list = [
    {
        #'model': 'gpt-4-1106-preview',
        'model': 'gpt-3.5-turbo-1106',
        'api_key': 'sk-',
    }
    ]

llm_config = {"config_list": config_list, "seed": 32}

user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   system_message="A human admin.",
   is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
   code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
   human_input_mode="TERMINATE"
)

weather_reporter = autogen.AssistantAgent(
    name="Weather_reporter",
    system_message="""You are a weather reporter who provides weather 
    overall status based on the dates and location user provided.
    Using historical data is OK.
    Make your response short.""",
    llm_config=llm_config,
    description="""This agent is reponsible for providing weather 
    overall status based on the dates and location user provided.
    """
)
activity_agent = autogen.AssistantAgent(
    name="activity_agent",
    system_message="""You are an activity agent who recommends 
    activities considering the weather situation from weather_reporter.
    Don't ask questions. Make your response short.""",
    llm_config=llm_config,
    description="""This agent is responsible for actitivies 
    recommendation considering the weather situation from weather_reporter.
    """,
)
insure_agent = autogen.AssistantAgent(
    name="Insure_agent",
    system_message="""You are an Insure agent who gives 
    the short insurance items based on the travel plan. 
    Don't ask questions. Make your response short.""",
    llm_config=llm_config,
    description="""This agent is responsible for giving the short 
    insurance items based on the travel plan.
    """,
)
travel_advisor = autogen.AssistantAgent(
    name="Travel_advisor",
    system_message="""After activities recommendation generated 
    by activity_agent, You generate a concise travel plan 
    by consolidating the activities.
    """,
    llm_config=llm_config,
    description="""After activities recommendation generated by activity_agent,
    this agent is responsible for making travel plan by consolidating 
    the activities.
    """,
)
groupchat = autogen.GroupChat(agents=[user_proxy,  travel_advisor, activity_agent, weather_reporter,insure_agent], messages=[], max_round=8)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


user_proxy.initiate_chat(manager, message="Give me a travel plan to Bohol Island in Sept.")

# type exit to terminate the chat