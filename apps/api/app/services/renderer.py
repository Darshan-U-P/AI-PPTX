from abc import ABC, abstractmethod

from app.schemas.presentation import PresentationIR


class Renderer(ABC):
    """Renderer boundary: renderers consume validated IR and contain no AI logic."""

    @abstractmethod
    def render(self, presentation: PresentationIR) -> bytes:
        raise NotImplementedError
