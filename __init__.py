# from datetime import datetime, timedelta
# from typing import Any, Dict

# from jose import jwt

# from src.configuration.environments import Environments
# from src.infrastructure.at.jwt.ports import (
#     AccessAndRefreshJWTRepositoryPort
# )


# class AccessAndRefreshJWTRepositoryAdapter(
#     AccessAndRefreshJWTRepositoryPort
# ):
#     async def encode_token(self, token_type: str, data: Dict[str, Any]) -> str:
#         encoded_data = data.copy()

#         expire_at = None
#         if token_type == "access":
#             expire_at = datetime.now() + timedelta(
#                 seconds=int(Environments().JWT_ACCESS_TOKEN_EXPIRE_SECONDS)
#             )
#         elif token_type == "refresh":
#             expire_at = datetime.now() + timedelta(
#                 seconds=int(Environments().JWT_REFRESH_TOKEN_EXPIRE_SECONDS)
#             )

#         encoded_data.update(
#             {
#                 "exp": expire_at,
#                 "type": token_type
#             }
#         )

#         encoded_jwt = jwt.encode(
#             encoded_data,
#             key=Environments().JWT_SECRET_KEY,
#             algorithm=Environments().JWT_ALGORITHM
#         )

#         return encoded_jwt

#     async def decode_token(self, token: str) -> Dict[str, Any]:
#         decoded_jwt = jwt.decode(
#             token,
#             key=Environments().JWT_SECRET_KEY,
#             algorithms=[Environments().JWT_ALGORITHM]
#         )

#         return decoded_jwt