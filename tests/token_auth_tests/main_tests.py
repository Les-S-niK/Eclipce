
## Built-in modules: ##

## Third-party modules: ##
from unittest import TestCase

## Local modules: ##
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth import (
    create_token, decode_token, authenticate_user,
    BcryptActions,
)
from core.api_v1.token_auth.schemas import DecodedTokenModel, TokenModel
from config import ACCESS_TOKEN_EXPIRE_TIME, TOKEN_TYPE
from tests.sign_up_tests.main_tests import user_models


encoded_tokens: list[str] = ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJMT0dJTkFTREFEQSBVU0VSIFNTTExMIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.hXwruVA_njjfvXLsejntuoWzXFNVbnC_g22DZGU-_Ec', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1YXNkYXNhYWRkQUF4Y3hhZHNTREREUyIsImV4cCI6MTc0NDM5NzcxOX0.nxhwQQwbyFVhgHVShXawZJAQ2PdQC7SLyaMycmZCV2Y', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJLUlVJU0VSIExPTF9CT1kiLCJleHAiOjE3NDQzOTc3MTl9.UhOYGKknHcWmEjtYz-UJVDA8kPyN_x22FG8orIP29ts', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJQRVRST1lBTCIsImV4cCI6MTc0NDM5NzcxOX0.TDE7c6KE83ygvTCvubY0nKurcgmXSv2r0pPjRis28zY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJcdTA0MjRcdTA0MmJcdTA0MTIxbExhIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.a4xZRP5PFufkpuT6KI8ISxRtYX8waXacqSBRscTYBWM', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTRVhZXHVkODNkXHVkYzk2Qk9TU0lOVEhJU0dZIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.q-mAt9KjvOSSChM2x6MxcerAS6axnSMNs992TyQTbsU', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZT29vIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.HFI_BAkXgCneunNGJjxb2QOL5jkxXDXSwAEtQqYyEKE', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyYXNkYXNkIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.XyM354xzL3i_MG2yD71Dg-3HCh16Kztx5KBvRr8X6dI', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJXRVJUWVVJREZHSEpLJV4mKigpIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.RmJ9PYFXAGYhhY1JH9neDcuTZ0Gqs_oV58jCcf7I3fs', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMzQ1LjY3YVNBUzg5Q0dISksiLCJleHAiOjE3NDQzOTc3MTl9.5rprKWjeuZD01UsL6NhQSjiqMIIFcAp7scN52c3RRTU', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0NTY3ODlERkdISksgcyIsImV4cCI6MTc0NDM5NzcxOX0.6XX4-htZ1m5HS1sZEe57g7c4ywnk-27qQe5FSSFhOio', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJGSVNUIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.2VdknsouLu-JJRQvnwV73gCDmRDA9nU9j974yZiebIw', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJJTkdTYSBBIFMgUyBTICIsImV4cCI6MTc0NDM5NzcxOX0.wgUPN3hKumJf1BzDpjjZRVunTmt7Y0rvTn19h1lR5Qg', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBU1NMU09TT1NPU09TT09TT1NPIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.F42GWqkCDPeF2kP6QpG8sNC0v8xFOPsULCJueiswgPI', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJLUkFDSyIsImV4cCI6MTc0NDM5NzcxOX0.k8KLPsHZPj0YFZ1w9s1QiJBwdRyhjAg775sSgPjCTbk', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTTFA6UDpQIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.j6C2y0ZHF58QYdsayBszrBr7XlFlBGko9Qn5CXhk0n4', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJOaWtpdGEiLCJleHAiOjE3NDQzOTc3MTl9.B5gXS6ftKmRnsLGCbdCyvno3StgonhGmZE6Bq7QQ3Zg', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJIRUxMT1ciLCJleHAiOjE3NDQzOTc3MTl9.Ctx2-a1Qreqbh1eU5mAXh6Z3HIEAxYNdGL4y5NA_MVU', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCWVlRXHVkODNkXHVkYzk2IiwiZXhwIjoxNzQ0Mzk3NzE5fQ.A8YiIwz49P9bFmRVm4S6aIDfoermGVHiDZM0x30cet8', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJMT0xJTE9QIiwiZXhwIjoxNzQ0Mzk3NzE5fQ.IdPnGY4tEDWxXMArXH0dlRvLg2S8cXINz5gIM4pb2fM']

class TestTokenAuth(TestCase):
    """Class for testing the /api_v1/token_auth/ endpoint.

    Args:
        TestCase.
    """
    def test_create_access_token(self) -> None:
        for user in user_models:
            user_data: dict[str, str] = {
                "sub": user.get("sub")
            }
            token: str = create_token(data_to_encode=user_data, expires_delta=ACCESS_TOKEN_EXPIRE_TIME)
            self.assertIsNotNone(token)
    
    def test_decode_acces_token(self) -> None:
        for token in encoded_tokens:
            token_model: TokenModel = TokenModel(access_token=token, token_type=TOKEN_TYPE)
            decoded_token: DecodedTokenModel = decode_token(encoded_token=token_model)
            self.assertIsInstance(decoded_token, DecodedTokenModel)
    
    async def test_authenticate_user(self) -> None:
        for user in user_models:
            user_model: UserRegistrationModel = UserRegistrationModel(**user)
            response: UserRegistrationModel | bool = await authenticate_user(user_login=user_model.login, user_password=user_model.password)
            assert self.assertIsInstance(response, bool | UserRegistrationModel)
    
    def test_bcrypt_actions(self) -> None:
        for user in user_models:
            user_model: UserRegistrationModel = UserRegistrationModel(**user)
            bcrypt_actions: BcryptActions = BcryptActions(user_model.password)
            hashed_password: str = bcrypt_actions.hash_password()
            compare_result: bool = bcrypt_actions.compare_password(hashed_password=str(hashed_password))
            assert self.assertTrue(compare_result)
            