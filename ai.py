import openai


def process_with_ai(raw: str) -> str:
    req = f"""
You are a bot for helping code review.
Standard csv report was generated from diff analysis tool.

Here is a csv report below for a specific commit.
Evaluate it and indicate the most important parts which reviewers should care.
Empty report means that there are no dangerous changes.

--- report start ---

{raw}

--- report end ---
"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": req}]
    )
    return completion.choices[0].message.content
