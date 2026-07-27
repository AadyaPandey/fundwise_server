from pydantic import BaseModel

class GrantApplication(BaseModel):
    organization: str
    requested_amount: int
    registration_valid: bool
    timeline: str
    beneficiaries: int