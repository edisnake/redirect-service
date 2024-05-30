from pydantic import BaseModel, validator


class DomainSchema(BaseModel):
    domain: str
    weight: int

    @validator('domain')
    def validate_domain(cls, value: str):
        # Making sure the domain includes the protocol
        if not value.startswith('http'):
            raise ValueError('The domain must include the protocol')

        return value


class PoolSchema(BaseModel):
    name: str
    domains: list[DomainSchema]


class PoolOutputSchema(PoolSchema):
    id: int
