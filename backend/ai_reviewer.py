import anthropic

client = anthropic.Anthropic()


def ai_review(code: str, issues: list) -> str:
    issue_text = "\n".join(
        f"- line {i['line']}: {i['message']}" for i in issues
    ) or "None found"

    prompt = (
        "You are a senior code reviewer. Review the code below.\n"
        "Automated checks already found:\n"
        f"{issue_text}\n\n"
        "Give a short review: bugs, readability, and 2-3 concrete "
        "improvements. Keep it under 200 words.\n\n"
        f"```\n{code}\n```"
    )

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text