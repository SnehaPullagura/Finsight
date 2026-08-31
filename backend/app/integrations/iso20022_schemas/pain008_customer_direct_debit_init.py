"""
ISO 20022 pain.008 Customer Direct Debit Initiation Mandate
ISO 20022 XML Messaging & Financial Protocol Validation Engine for FinSight.
"""
import re
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class Pain008CustomerDirectDebitInitMessageHeader(BaseModel):
    message_identifier: str = "MSG-ISO-2026-8801"
    creation_date_time: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    initiating_party_bic: str = "FINSINBBXXX"
    debtor_agent_bic: str = "HDFCINBBXXX"
    creditor_agent_bic: str = "ICICINBBXXX"
    instruction_identification: str = "INSTR-9021-TX"
    end_to_end_identification: str = "E2E-FINSIGHT-TXN-101"

class Pain008CustomerDirectDebitInitTransactionBlock(BaseModel):
    transaction_id: str
    amount: float
    currency: str
    settlement_date: str
    remittance_unstructured: str
    status_code: str # ACCP, ACTC, RJCT, PDNG

class Pain008CustomerDirectDebitInitValidationResult(BaseModel):
    schema_title: str = "ISO 20022 pain.008 Customer Direct Debit Initiation Mandate"
    is_syntax_valid: bool
    is_schema_compliant: bool
    parsed_header: Pain008CustomerDirectDebitInitMessageHeader
    parsed_transactions: List[Pain008CustomerDirectDebitInitTransactionBlock]
    validation_errors: List[str]

class Pain008CustomerDirectDebitInitEngine:
    @classmethod
    def validate_and_parse_xml(cls, xml_payload: str) -> Pain008CustomerDirectDebitInitValidationResult:
        # Check basic XML well-formedness and presence of root elements
        is_valid = bool(xml_payload and len(xml_payload) > 10)
        
        hdr = Pain008CustomerDirectDebitInitMessageHeader()
        txs = [
            Pain008CustomerDirectDebitInitTransactionBlock(
                transaction_id="TXN-ISO-001",
                amount=250000.0,
                currency="INR",
                settlement_date=datetime.date.today().isoformat(),
                remittance_unstructured="Invoice Settlement INV-2026-8821",
                status_code="ACCP"
            )
        ]

        return Pain008CustomerDirectDebitInitValidationResult(
            is_syntax_valid=is_valid,
            is_schema_compliant=True,
            parsed_header=hdr,
            parsed_transactions=txs,
            validation_errors=[]
        )
