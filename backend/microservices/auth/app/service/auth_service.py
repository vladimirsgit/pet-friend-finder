from app.schema.signup_request import SignUpRequest

import httpx
import os

class AuthService:
    async def register(self, signup_request: SignUpRequest):
        headers = {"x-api-key": os.getenv("USERS_INTERNAL_SERVICE_API_KEY")}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://users-microservice:8001/api/v1/internal/register",
                json=signup_request.model_dump(),
                headers=headers
            )

        return response.json()