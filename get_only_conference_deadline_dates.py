import os
from os.path import join as pjoin
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from pdb import set_trace
from datetime import datetime
from copy import deepcopy
import re
from pathlib import Path
import getpass
import os
from pdb import set_trace
import shutil
import pandas as pd
from pprint import pprint
import getpass
import os
from datetime import datetime
from copy import deepcopy

from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from myutils import CSVFileBuilderFromData


def main():    
    year = 2025
    conference_deadline_file_name = f"Conference_deadlines_{year}_according_to_AI_agent.csv"
    conference_deadline_date_only_file_name = f"Conference_deadlines_{year}_date_only_according_to_AI_agent.csv"

    df = pd.read_csv(conference_deadline_file_name)
    conference_list = df["conference_name"].to_list()

    llm = OpenAIModel(
        # model_name='qwen2.5:32b',
        model_name='gemma3',
        provider=OpenAIProvider(base_url='http://localhost:11434/v1')
    )
    agent = Agent(
        llm, 
        # tools=[duckduckgo_search_tool()],        
        # system_prompt='Search DuckDuckGo for the given query and return the results.',
        tools=[],
        system_prompt="Answer the question."
    )

    file_builder = CSVFileBuilderFromData(conference_deadline_date_only_file_name)

    for index, row in df.iterrows():
        conference_name = row["conference_name"]
        ai_answer = row["ai_answer"]

        # Remove <think> </think>
        ai_answer = re.sub(r"<think>.*?</think>\n?", "", ai_answer, flags=re.DOTALL)
        summarize_question = f"""
        Given an answer, find the full paper submission deadline. No pre-amble. No explanation. Only return the full paper submission deadline date and nothing else.
        Answer: {ai_answer}
        """
        agent_answer = agent.run_sync(
            summarize_question
        )
        agent_answer = agent_answer.data
        print(f"Conference name: {conference_name}")
        print("LLM answer:")
        print(agent_answer)
        file_builder.add_data(conference_name=conference_name, date=agent_answer)

        # set_trace()
    # Save the results to file
    file_builder.build_file()


if __name__ == "__main__":
    main()