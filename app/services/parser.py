import re
from datetime import datetime
from app.schemas.transaction import TransactionExtracted
import os
import openai
import logging
import json

logger = logging.getLogger(__name__)

AMOUNT_RE = re.compile(r"\$?(\d+[\.,]?\d*)")
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})\b")

CATEGORY_KEYWORDS = {
    "utilities": ["vodafone", "electricity", "water"],
    "food": ["restaurant", "cafe", "grocery"],
    "income": ["invoice", "payment", "client"],
}


def parse_text(text: str) -> TransactionExtracted:
    """
    Main parsing function that attempts to use an LLM first,
    then falls back to a regex-based method.
    """
    logger.info("Starting text parsing process.")
    try:
        logger.info("Attempting to parse with LLM.")
        return parse_with_llm(text)
    except Exception as e:
        # Log the specific error from the LLM attempt
        logger.warning(
            f"LLM parsing failed with error: {e}. Falling back to regex method."
        )
        return parse_with_fallback(text)


def parse_with_llm(text: str) -> TransactionExtracted:
    logger.debug("Executing parse_with_llm function.")

    # --- FIX 2: Use the modern OpenAI Client ---
    try:
        # Create a client instance. It automatically uses the OPENAI_API_KEY environment variable.
        client = openai.OpenAI()

        prompt = f"""
            You are an intelligent document parser. Extract the following fields from the unstructured receipt text below. Respond in a valid JSON object with the following keys and value types: "vendor" (string), "amount" (float), "amount_currency" (string), "date" (string, YYYY-MM-DD format), "category" (string).

            If a value is not present, use null for that key.

            ---
            {text}
            """

        logger.info("Sending request to OpenAI...")
        logger.debug(f"OpenAI Prompt:\n---PROMPT START---\n{prompt}\n---PROMPT END---")

        # Use the new client syntax and response_format for guaranteed JSON
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        logger.info("Received response from OpenAI.")
        logger.debug(f"OpenAI Raw JSON Response: {content}")

        # The response is now guaranteed to be a JSON string, so we can parse it directly.
        fields = json.loads(content)

        logger.debug(f"Parsed fields from LLM response: {fields}")

        extracted_data = TransactionExtracted(
            vendor=fields.get("vendor"),
            amount=float(fields.get("amount", 0))
            if fields.get("amount") is not None
            else None,
            amount_currency=fields.get("amount_currency") or None,
            date=datetime.fromisoformat(fields.get("date"))
            if fields.get("date")
            else None,
            category=fields.get("category"),
        )
        logger.info(f"Successfully extracted data with LLM: {extracted_data.dict()}")
        return extracted_data

    except Exception as e:
        logger.error(
            f"Error during OpenAI API call or response processing: {e}", exc_info=True
        )
        raise  # Re-raise to trigger the fallback


def parse_with_fallback(text: str) -> TransactionExtracted:
    """
    Parses receipt text using a simple regex and keyword-based approach.
    """
    logger.info("Executing parse_with_fallback function.")
    amount = _extract_amount(text)
    date = _extract_date(text)
    vendor = _extract_vendor(text)
    category = _categorize(text)

    fallback_data = TransactionExtracted(
        vendor=vendor, amount=amount, date=date, category=category
    )
    logger.info(f"Extracted data with fallback method: {fallback_data.dict()}")
    return fallback_data


def _extract_amount(text):
    match = AMOUNT_RE.search(text)
    amount = float(match.group(1).replace(",", "")) if match else None
    logger.debug(f"Fallback extracted amount: {amount}")
    return amount


def _extract_date(text):
    match = DATE_RE.search(text)
    if not match:
        logger.debug("Fallback could not find a date.")
        return None
    try:
        date = datetime.strptime(match.group(1), "%Y-%m-%d")
        logger.debug(f"Fallback extracted date: {date}")
        return date
    except ValueError:
        try:
            date = datetime.strptime(match.group(1), "%d/%m/%Y")
            logger.debug(f"Fallback extracted date: {date}")
            return date
        except ValueError:
            logger.debug("Fallback found a date-like string but could not parse it.")
            return None


def _extract_vendor(text):
    lines = text.splitlines()
    vendor = lines[0].strip() if lines else None
    logger.debug(f"Fallback extracted vendor: {vendor}")
    return vendor


def _categorize(text):
    text = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                logger.debug(
                    f"Fallback categorized as '{category}' based on keyword '{keyword}'."
                )
                return category
    logger.debug(
        "Fallback could not determine a category, defaulting to 'uncategorized'."
    )
    return "uncategorized"
