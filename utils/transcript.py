import discord
import html
import io

EMOJI_TO_TYPE = {
    "🛠️": "General",
    "🚨": "Report",
    "💡": "Suggestion"
}

async def generate_transcript(channel: discord.TextChannel, owner: discord.Member):
    """
    Generate an HTML transcript and return a BytesIO object (no file saved to disk)
    """
    messages = []
    async for msg in channel.history(limit=None, oldest_first=True):
        messages.append(msg)

    emoji = channel.name.split("-")[0]
    ticket_type = EMOJI_TO_TYPE.get(emoji, "Unknown")

    html_content = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <title>Transcript – {ticket_type} – User: {owner.display_name}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

            body {{ font-family: 'Roboto', sans-serif; background: #1e1e2f; color: #e0e0e0; margin:0; padding:0; }}
            .container {{ max-width: 900px; margin: 20px auto; padding:20px; background: #2c2c3e; border-radius:12px; }}
            h1 {{ text-align:center; color:#ff79c6; margin-bottom:20px; }}
            .message {{ padding:15px 20px; margin:10px 0; border-radius:10px; background:#3b3b52; }}
            .author {{ font-weight:700; color:#8be9fd; }}
            .time {{ font-size:0.8em; color:#6272a4; float:right; }}
            .content {{ margin-top:8px; white-space:pre-wrap; line-height:1.5; }}
            .footer {{ text-align:center; margin-top:30px; font-size:0.85em; color:#6272a4; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Transcript – Ticket Type: {ticket_type} – User: {owner.display_name}</h1>
    """

    for msg in messages:
        timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        content = html.escape(msg.content)
        html_content += f"""
        <div class='message'>
            <div class='author'>{msg.author}<span class='time'>{timestamp}</span></div>
            <div class='content'>{content}</div>
        </div>
        """

    html_content += """
            <div class="footer">Developer : Nicotine | ACE team</div>
        </div>
    </body>
    </html>
    """

    bio = io.BytesIO()
    bio.write(html_content.encode('utf-8'))
    bio.seek(0)
    return bio
