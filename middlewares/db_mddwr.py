from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject



class DbSessionMiddleware(BaseMiddleware):
   
    def __init__(self, async_sess) -> None:
        super().__init__()
        self.async_session = async_sess
    

    def __call__(
                self, 
                handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
                event: TelegramObject, 
                data: Dict[str, Any]) -> Coroutine[Any, Any, Any]:
        
        # we give session from constructor to our handlers by dict "data" with key "async_session"
        data["async_session"] = self.async_session
        
        return handler(event, data)
    

class RedisInstanceMiddleware(BaseMiddleware):
    def __init__(self, instance_redis) -> None:
        super().__init__()
        self.inst_red = instance_redis

    def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]) -> Coroutine[Any, Any, Any]:
        
        data["redis_instance"] = self.inst_red

        return handler(event, data)
