from starlette.datastructures import FormData
from starlette.requests import Request

from fcg.viewmodels import parse
from fcg.viewmodels.base_viewmodel import BaseViewModel


class FormBaseViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.proposal_code = ""
        self.principal_investigator = ""
        self.target = ""

    def load_common_data(self, form: FormData) -> None:
        # proposal code
        self.proposal_code = parse.parse_proposal_code(form, self.errors) or ""

        # Principal Investigator
        self.principal_investigator = (
            parse.parse_principal_investigator(form, self.errors) or ""
        )

        # target
        self.target = parse.parse_target(form, self.errors) or ""
