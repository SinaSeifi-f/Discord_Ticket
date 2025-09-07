import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from utils.counter import get_ticket_number
from utils.transcript import generate_transcript
import utils.config as config

open_tickets = {}
closed_tickets = []

TICKET_EMOJIS = {
    "general": "🛠️",
    "report": "🚨",
    "suggestion": "💡"
}

embed_templates = {
    "general": {
        "title": "🛠️ تیکت پشتیبانی",
        "description": (
            "به تیکت پشتیبانی خوش آمدید!\n\n"
            "🔹 لطفاً سوال یا درخواست خودتون رو به صورت واضح و کامل مطرح کنید.\n"
            "🔹 تیم پشتیبانی در اسرع وقت پاسخ خواهد داد.\n\n"
            "**راهنما:**\n"
            "1️⃣ موضوع اصلی رو توضیح بدید.\n"
            "2️⃣ در صورت نیاز اسکرین‌شات یا فایل ضمیمه کنید.\n"
            "3️⃣ منتظر پاسخ بمونید، از منشن کردن بی‌دلیل خودداری کنید."
        ),
        "color": discord.Color.dark_gold()
    },
    "report": {
        "title": "🚨 تیکت گزارش مشکل",
        "description": (
            "شما وارد بخش گزارش مشکلات شدید.\n\n"
            "⚠️ لطفاً مشکل رو با جزئیات کامل توضیح بدید:\n"
            "🔹 چه اتفاقی افتاده؟\n"
            "🔹 کی و کجا رخ داده؟\n"
            "🔹 چه کارهایی برای رفع مشکل انجام دادید؟\n\n"
            "📌 اطلاعات بیشتر → رسیدگی سریع‌تر!"
        ),
        "color": discord.Color.red()
    },
    "suggestion": {
        "title": "💡 تیکت پیشنهادات",
        "description": (
            "از اینکه پیشنهادات ارزشمند خودتون رو با ما به اشتراک می‌گذارید ممنونیم 🙏\n\n"
            "🔹 ایده یا پیشنهادی دارید که به بهبود سرور کمک می‌کنه؟\n"
            "🔹 لطفاً پیشنهاد خودتون رو به صورت واضح توضیح بدید.\n"
            "🔹 در صورت امکان مثال یا توضیحات بیشتری ارائه کنید.\n\n"
            "✨ ما همه پیشنهادات رو بررسی می‌کنیم و بهترین‌ها رو پیاده‌سازی می‌کنیم."
        ),
        "color": discord.Color.yellow()
    }
}

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.update_status.is_running():
            self.update_status.start()

    @tasks.loop(seconds=15)
    async def update_status(self):
        if not self.bot or not self.bot.is_ready():
            return
        try:

            valid_closed = [ch for ch in closed_tickets if ch and self.bot.get_channel(ch.id)]
            
            await self.bot.change_presence(
                activity=discord.Game(
                    name=f"🎫 Open: {len(open_tickets)} | 🔒 Closed: {len(valid_closed)}"
                )
            )
        except Exception as e:
            print(f"Error updating status: {e}")




    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str):
        guild = interaction.guild
        user = interaction.user
        category = guild.get_channel(config.TICKET_CATEGORY_ID)
        support_role = guild.get_role(config.SUPPORT_ROLE_ID)


        print(f"Creating ticket for user {user.id}, type: {ticket_type}")
        print(f"Category ID: {config.TICKET_CATEGORY_ID}, Found: {category}")
        print(f"Support Role ID: {config.SUPPORT_ROLE_ID}, Found: {support_role}")

        if not category:
            await interaction.followup.send("❌ Ticket category not found.", ephemeral=True)
            return
        if not support_role:
            await interaction.followup.send("❌ Support role not found.", ephemeral=True)
            return
        if user.id in open_tickets:
            await interaction.followup.send(
                f"⚠️ You already have an open ticket: {open_tickets[user.id].mention}", ephemeral=True
            )
            return

        try:
            ticket_number = get_ticket_number()
        except Exception as e:
            await interaction.followup.send(f"❌ Cannot generate ticket number: {e}", ephemeral=True)
            return

        emoji = TICKET_EMOJIS.get(ticket_type, "🎫")
        channel_name = f"{emoji}•{ticket_number:04d}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        try:
            ticket_channel = await guild.create_text_channel(
                name=channel_name, category=category, overwrites=overwrites
            )
        except Exception as e:
            await interaction.followup.send(f"❌ Cannot create ticket channel: {e}", ephemeral=True)
            return

        open_tickets[user.id] = ticket_channel

        data = embed_templates.get(ticket_type, embed_templates["general"])
        embed = discord.Embed(title=data["title"], description=data["description"], color=data["color"])
        embed.set_footer(text=f"User: {user}")

        view = View(timeout=None)
        close_btn = Button(label="Close", style=discord.ButtonStyle.primary, emoji="🔒")
        delete_btn = Button(label="Delete", style=discord.ButtonStyle.danger, emoji="🗑️")
        transcript_btn = Button(label="HTML", style=discord.ButtonStyle.secondary, emoji="💾")

        async def close_callback(btn_inter: discord.Interaction):
            if btn_inter.user.id == user.id or config.SUPPORT_ROLE_ID in [r.id for r in btn_inter.user.roles]:
                await ticket_channel.set_permissions(user, read_messages=False, send_messages=False)
                open_tickets.pop(user.id, None)
                if ticket_channel not in closed_tickets:
                    closed_tickets.append(ticket_channel)
                await btn_inter.response.send_message("🔒 Ticket closed.", ephemeral=True)
            else:
                await btn_inter.response.send_message("❌ You do not have permission to close.", ephemeral=True)


        async def delete_callback(btn_inter: discord.Interaction):
            if btn_inter.user.id == user.id or config.SUPPORT_ROLE_ID in [r.id for r in btn_inter.user.roles]:
                open_tickets.pop(user.id, None)
                await ticket_channel.delete()
            else:
                await btn_inter.response.send_message("❌ You do not have permission to delete.", ephemeral=True)


        async def transcript_callback(btn_inter: discord.Interaction):
            try:
                bio = await generate_transcript(ticket_channel, user)
                await ticket_channel.send(
                    f"💾 Transcript for ticket #{ticket_number:04d}:",
                    file=discord.File(fp=bio, filename=f"ticket_{ticket_number:04d}.html")
                )
                await btn_inter.response.send_message("✅ Transcript created.", ephemeral=True)
                bio.close()
            except Exception as e:
                await btn_inter.response.send_message(f"❌ Error generating transcript: {e}", ephemeral=True)

        close_btn.callback = close_callback
        delete_btn.callback = delete_callback
        transcript_btn.callback = transcript_callback

        view.add_item(close_btn)
        view.add_item(delete_btn)
        view.add_item(transcript_btn)

        try:
            await ticket_channel.send(embed=embed, view=view)
            await interaction.followup.send(f"✅ Ticket created: {ticket_channel.mention}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error sending ticket message: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
