from abc import ABC, abstractmethod


class TTSProvider(ABC):
    @abstractmethod
    def synth(self, text: str, out_path: str) -> str:
        raise NotImplementedError
