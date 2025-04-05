import uuid


class VerificationService:
    def generate(self) -> str:
        return str(uuid.uuid4())
