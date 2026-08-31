from fastapi import APIRouter, Depends, status
from backend.app.cpq.schemas import (
    CurrencyConvertRequest,
    CurrencyConvertResponse,
    PriceCalculationItem,
    CPQCalculationResponse
)
from backend.app.cpq.engine import CurrencyConversionService, CPQPricingEngine

router = APIRouter()

@router.post("/convert-currency", response_model=CurrencyConvertResponse)
async def convert_currency(req: CurrencyConvertRequest):
    converted = CurrencyConversionService.convert(req.amount, req.from_currency, req.to_currency)
    rate = round(converted / req.amount, 4) if req.amount > 0 else 1.0
    return CurrencyConvertResponse(
        original_amount=req.amount,
        from_currency=req.from_currency.upper(),
        converted_amount=converted,
        to_currency=req.to_currency.upper(),
        rate=rate
    )

@router.post("/calculate-pricing", response_model=CPQCalculationResponse)
async def calculate_quote_pricing(items: list[PriceCalculationItem], currency: str = "USD"):
    subtotal = 0.0
    total_disc = 0.0
    net = 0.0
    tax = 0.0
    grand_total = 0.0
    breakdowns = []

    for item in items:
        res = CPQPricingEngine.calculate_line_item(
            unit_price=item.unit_price,
            quantity=item.quantity,
            discount_percentage=item.discount_percentage or 0.0,
            flat_discount=item.flat_discount or 0.0,
            tax_rate_pct=item.tax_rate_pct or 0.0
        )
        subtotal += res["subtotal"]
        total_disc += res["discount_amount"]
        net += res["net_amount"]
        tax += res["tax_amount"]
        grand_total += res["total_amount"]
        breakdowns.append(res)

    return CPQCalculationResponse(
        subtotal=round(subtotal, 2),
        total_discount=round(total_disc, 2),
        net_amount=round(net, 2),
        tax_amount=round(tax, 2),
        total_amount=round(grand_total, 2),
        currency=currency.upper(),
        line_breakdowns=breakdowns
    )
