# AIConferencesDeadlines
Website: [GitHub Pages](https://dangmanhtruong1995.github.io/AIConferencesDeadlines/)

Automatically pulls the paper submission deadlines of some well-known AI conferences by using AI agents. 

This was done using a two-step process:

- Firstly I used a reasoning model (QwQ) to get the information about deadlines.

- Then I used a smaller non-reasoning model (Gemma3) to extract only the dates.

How to run:
1) Install Ollama by following the steps on their website. Then:

```shell
pip install -r requirements.txt
```		

2) Run :
```shell
python search_for_conference_deadlines.py
python get_only_conference_deadline_dates.py
python post_process.py
python draw_timeline.py
```