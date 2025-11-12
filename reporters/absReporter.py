from abc import ABC, abstractmethod


class Reporter(ABC):
    
    @abstractmethod
    def send_message(self, *args, **kwargs):
        pass