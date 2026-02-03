from dataclasses import dataclass


@dataclass
class JobApplicationDocument:
    """
    Represents a job application document with relevant details.

    Attributes:
        filename: The name of the document.
        content: The content of the document.
        mime_type: The MIME type of the document.
    """

    filename: str
    content: bytes
    mime_type: str = "application/pdf"

    @classmethod
    def create(
        cls, filename: str, content: bytes, mime_type: str = "application/pdf"
    ) -> "JobApplicationDocument":
        return cls(filename=filename, content=content, mime_type=mime_type)
