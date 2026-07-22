from groq import Groq

client = Groq(
    api_key="your api key"
)

def compare_ai(info1, info2, rsi1, rsi2):

    prompt = f"""
Compare these two stocks like a professional investment advisor.

Stock 1
Company: {info1.get('longName')}
Price: {info1.get('currentPrice')}
Market Cap: {info1.get('marketCap')}
PE Ratio: {info1.get('trailingPE')}
RSI: {rsi1:.2f}

Stock 2
Company: {info2.get('longName')}
Price: {info2.get('currentPrice')}
Market Cap: {info2.get('marketCap')}
PE Ratio: {info2.get('trailingPE')}
RSI: {rsi2:.2f}

Give:

1. Better Stock
2. Why?
3. Risk Comparison
4. Growth Potential
5. Which stock would you choose and why?

Keep answer short, professional and in bullet points.
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