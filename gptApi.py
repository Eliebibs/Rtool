from openai import OpenAI

client = OpenAI(api_key='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')

def summarize_html(html_content):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes web content."},
                {"role": "user", "content": f"Summarize the following content in about 2-3 sentences, please focus on relevant, insightful, and up to date information. Organize the summary into 3 sections, a title, a description, and a list of key points. Please organize the summary using fonts, proper text formatting, and bullet points:\n\n{html_content}"}
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error communicating with GPT API: {e}")
        return "Error summarizing content"