from openai import OpenAI

client = OpenAI()


def ask_ai(ai_prompt):
    return client.responses.create(
        model="gpt-4o-mini",
        input=ai_prompt,
        text={"format": {"type": "text"}},
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True,
    )


def create_ai_prompt(list_games: list[str], number_of_players: int):
    return f"given this list of games {list_games}, \
        can you suggest a game that is multiplayer \
        and able to play with {number_of_players} players"


def get_suggestion(list_games: list[str], number_of_players: int):
    ai_prompt = create_ai_prompt(list_games, number_of_players)
    return ask_ai(ai_prompt)
