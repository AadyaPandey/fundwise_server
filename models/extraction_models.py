from typing import Dict, List
from pydantic import BaseModel, Field


class PDFExtraction(BaseModel):
    """
    Raw information extracted from a grant application PDF.
    """

    organization: str = Field(default="")
    registration_number: str = Field(default="")
    year_established: int = Field(default=0)
    years_operating: int = Field(default=0)

    contact_person: str = Field(default="")
    designation: str = Field(default="")

    email: str = Field(default="")
    phone: str = Field(default="")

    project_title: str = Field(default="")
    grant_category: str = Field(default="")

    requested_amount: int = Field(default=0)

    project_description: str = Field(default="")

    beneficiaries: int = Field(default=0)

    timeline: str = Field(default="")

    budget: Dict[str, int] = Field(default_factory=dict)

    documents: List[str] = Field(default_factory=list)

    declaration_signed: bool = Field(default=False)