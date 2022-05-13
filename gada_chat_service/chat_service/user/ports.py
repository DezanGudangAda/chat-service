from abc import ABC, abstractmethod
from typing import Optional


class IUserServiceProvider(ABC):
    @abstractmethod
    def get_buyer_name(self, username: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_seller_name(self, id: str) -> Optional[str]:
        raise NotImplementedError
