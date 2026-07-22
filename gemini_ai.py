
from groq import Groq

client = Groq(
    api_key="enter_your api_key"
)

def analyze_stock(company, price, rsi, advice):


    prompt = f"""
Company: {company}
Current Price: {price}
RSI: {rsi}
Recommendation: {advice}

Give:
1. Buy/Hold/Sell
2. Reason
3. Risk
4. Future Outlook
5. Long term or Short term
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

def chat_with_ai(company, price, rsi, advice, question):

    prompt = f"""
You are an expert stock market AI assistant.

Company: {company}
Current Price: ₹{price}
RSI: {rsi}
Recommendation: {advice}

User Question:
{question}

Answer in simple language.
Keep the answer under 200 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
