from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="The name of the category")
    description: str = Field(..., min_length=5, max_length=255, description="A brief description of the category")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int = Field(..., description="The unique identifier of the category")

    class Config:
        form_attributes = True
        orm_mode = True
