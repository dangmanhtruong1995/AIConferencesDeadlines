import os
from os.path import join as pjoin
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from pdb import set_trace
from copy import deepcopy
import re
from pdb import set_trace
import pandas as pd
from pprint import pprint
from copy import deepcopy

from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from myutils import CSVFileBuilderFromData


def main():
    conference_list = [
        "NeurIPS",
        "CVPR",
        "ICML",
        "ICLR",
        "AAAI",
        "IJCAI",
        "ECCV",
        "ICCV",
        "ACL",
        "EMNLP",
        "UAI",
        "AISTATS",
        "ICASSP",
        "KDD (1st cycle)",
        "KDD (2nd cycle)",
        "MICCAI",
    ]
    year = 2025
    output_file_name = f"Conference_deadlines_{year}_according_to_AI_agent.csv"

    llm = OpenAIModel(
        # model_name='qwen2.5:32b',
        model_name='qwq',
        provider=OpenAIProvider(base_url='http://localhost:11434/v1')
    )
    agent = Agent(
        llm, 
        tools=[duckduckgo_search_tool()],
        system_prompt='Search DuckDuckGo for the given query and return the results.',
    )
    file_builder = CSVFileBuilderFromData(output_file_name)

    for conference_name in conference_list:
        try:
            agent_answer = agent.run_sync(                
                f"Search for the full paper submission deadline of the conference named {conference_name} in {year}.",
            )
            agent_answer = agent_answer.data
            print(f"Conference name: {conference_name}")
            print("LLM answer:")
            print(agent_answer)
        except RuntimeError as err:
            print(err)
            print(f"Conference name: {conference_name}. No search result found.")
            agent_answer = "No search result found."
        
        file_builder.add_data(conference_name=conference_name,ai_answer=agent_answer)

    # Save the results to file
    file_builder.build_file()


if __name__ == "__main__":
    main()