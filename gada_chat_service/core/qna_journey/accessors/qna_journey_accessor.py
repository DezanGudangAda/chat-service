from abc import ABC, abstractmethod


class IQnaJourneyAccessor(ABC):
    @abstractmethod
    def create(self):
        raise NotImplementedError

