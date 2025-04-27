
## Third-party modules: ##
from unittest import TestCase

## Local modules: ##
from core.api_v1.sign_up.schemas import UserRegistrationModel

user_models: dict[str, str] = [
    {'login': 'LOGINASDADA USER SSLLL', 'password': 'Pass%^&*()word123'},
    {'login': 'uasdasaaddAAxcxadsSDDDS', 'password': 'Secure$%^&*Pass456'},
    {'login': 'KRUISER LOL_BOY', 'password': 'MySecret789#'},
    {'login': 'PETROYAL', 'password': 'StrongPass!234'},
    {'login': 'ФЫВ1lLa', 'password': 'LetMeIn!567'},
    {'login': 'SEXY💖BOSSINTHISGY', 'password': 'Open%^&*()Sesame890'},
    {'login': 'YOoo', 'password': 'Welcome123$'},
    {'login': 'userasdasd', 'password': 'TrustNo1!'},
    {'login': 'WERTYUIDFGHJK%^&*()', 'password': 'Hi$%^&*()ddenGem!456'},
    {'login': '2345.67aSAS89CGHJK', 'password': 'SafeAn$%^&*()dSound789asdADADADA'},
    {'login': '456789DFGHJK s', 'password': 'Pa💖ssword!2023'},
    {'login': 'FIST', 'password': 'SecretKey!321'},
    {'login': 'INGSa A S S S ', 'password': 'AccessGranted!654'},
    {'login': 'ASSLSOSOSOSOSOOSOSO', 'password': 'User  Pass!987'},
    {'login': 'KRACK', 'password': 'TopSec$%^&*(ret123'},
    {'login': 'SLP:P:P', 'password': 'LetMeInasdasdadAgain!456'},
    {'login': 'Nikita', 'password': 'Password!2024'},
    {'login': 'HELLOW', 'password': 'SecureLogin!789'},
    {'login': 'BYYQ💖', 'password': 'HiddenPassw💖ord!321'},
    {'login': 'LOLILOP', 'password': 'StrongPassword!6asdasdasadadasdsdadad54'},

]


class TestSignUpModel(TestCase):
    """Test case for User regisration pydantic schema.

    Args:
        TestCase.
    """
    def test_registation_model(self) -> None:
        for user_model in user_models:
            user: UserRegistrationModel = UserRegistrationModel(**user_model)
            self.assertIsInstance(user, UserRegistrationModel)