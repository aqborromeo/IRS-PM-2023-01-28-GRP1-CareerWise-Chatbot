from .chat import Chat
from .user import User
from .chat_session import ChatSession
from .question import Question
from .option import Option
from .weight import Weight
from .occupation import Occupation
from .result import Result
from .career_path import CareerPath
from .ssoc_job import SsocJob


target_metadata = [
    User.metadata,
    Chat.metadata,
    Question.metadata,
    ChatSession.metadata,
    Option.metadata,
    Weight.metadata,
    Occupation.metadata,
    Result.metadata,
    CareerPath.metadata,
    SsocJob.metadata
]
