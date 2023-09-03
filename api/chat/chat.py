import json
from api.chat.setup import generate_chat_response, add_message
from api.chat.data import chat
from sqlalchemy.orm import Session

from api.common.models import Home
from api.crud.home import generate_business_project_summary, generate_home_project_summary, get_home_summary


def initialize_messages():
    """Initialize the chat messages with system and user messages."""
    return [
        {"role": "system", "content": "You're a kind helpful assistant, only respond with knowledge you know for sure, don't hallucinate information."},
        {"role": "user", "content": chat['initial']}
    ]
    
    
    
async def generate_chat_response(db: Session, chat, home_id=str):
    """Generate a response for the chat."""
    db_home = await db.query(Home).filter(Home.id == home_id).first()
    if db_home.chat is None:
        message = initialize_messages()
        summary = ""
        if db_home.home_type == "residential":
            summary = get_home_summary(db_home.toJSON())
        else:
            summary = generate_business_project_summary(db_home.toJSON())
        add_message(message, "user", summary)
        chat_response = generate_chat_response(message)
        if chat_response is None:
            return None
        db_home.chat = json.dumps(message)
        db.commit()
        return chat_response
    else:
        messages = json.loads(db_home.chat)
        add_message(messages, "user", chat['prompt'])
        chat_response = generate_chat_response(messages)
        if chat_response is None:
            return None
        db_home.chat = json.dumps(messages)
        db.commit()
        return chat_response
    