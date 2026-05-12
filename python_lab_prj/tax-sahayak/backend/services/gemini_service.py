import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = (
    "You are 'Tax Sahayak', an intelligent financial assistant. "
    "Your expertise is in Indian Income Tax, Loans, EMI calculations, and general personal finance. "
    "Keep responses short, clear, and helpful. "
    "For complex tax matters, advise consulting a Chartered Accountant. "
    "Be polite and professional. Use simple language."
)

# Fallback responses when API is unavailable
FALLBACK_RESPONSES = {
    "emi": "EMI = (P × R × (1+R)^N) / ((1+R)^N - 1). Use the EMI Calculator on the right to compute it instantly!",
    "tax": "Your income tax depends on your slab. Use the Tax Calculator on the right — enter your income and tax rate to get your liability!",
    "loan": "For loans, the key factors are: Principal amount, Interest Rate, and Tenure. Try the EMI Calculator to plan your repayment!",
    "section 80c": "Section 80C allows up to ₹1.5 lakh deduction on PPF, ELSS, LIC, NSC, and home loan principal.",
    "hra": "HRA exemption = min of (actual HRA received, 50%/40% of basic salary, rent paid minus 10% of basic salary).",
    "itr": "To file ITR: collect Form 16, log in to incometax.gov.in, choose the correct ITR form, fill details and submit by July 31.",
    "hello": "Hello! I'm Tax Sahayak. Ask me about EMI, income tax, loans, or deductions!",
    "hi": "Hi there! How can I help with your finances today?",
}

def get_fallback(message: str) -> str:
    lower = message.lower()
    for key, response in FALLBACK_RESPONSES.items():
        if key in lower:
            return response
    return (
        "⚠️ AI service is temporarily unavailable. "
        "Meanwhile: For EMI queries, use the calculator on the right. "
        "For tax queries, visit incometax.gov.in or consult a CA."
    )

# Initialize Groq client
client = None
if GROQ_API_KEY and "your_groq_api_key" not in GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

# Groq models to try (all free tier)
MODELS_TO_TRY = [
    "llama-3.3-70b-versatile",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
]

async def generate_response(message: str) -> str:
    if not client:
        return "AI not configured. Please set GROQ_API_KEY in your backend .env file."

    for model_name in MODELS_TO_TRY:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                model=model_name,
                max_tokens=400,
                temperature=0.7,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str.lower():
                # Try next model
                continue
            elif "model" in error_str.lower() and "not found" in error_str.lower():
                continue
            else:
                return f"Error: {error_str}"

    # All models exhausted — return smart fallback
    return get_fallback(message)
