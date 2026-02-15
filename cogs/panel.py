import discord
from discord.ext import commands
from discord.ui import Select, View
from cogs.ticket import Ticket

class TicketPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    @commands.command(name="tc")
    @commands.has_permissions(administrator=True)
    async def ticket_panel(self, ctx):
        embed = discord.Embed(
            title="🎫 Ticket System",
            description="Please select the type of ticket you want to create:",
            color=discord.Color.blurple()
        )

        options = [
            discord.SelectOption(label="General", value="general", emoji="🛠️"),
            discord.SelectOption(label="Report", value="report", emoji="🚨"),
            discord.SelectOption(label="Suggestion", value="suggestion", emoji="💡")
        ]

        select = Select(placeholder="Choose a ticket type...", options=options)

        async def select_callback(interaction: discord.Interaction):
            try:
                print(f"Select interaction received: {interaction.data['values'][0]}")
                await interaction.response.defer(ephemeral=True)
                ticket_cog: Ticket = self.bot.get_cog("Ticket")
                if not ticket_cog:
                    print("Ticket cog not found")
                    await interaction.followup.send("⚠️ Ticket system is not loaded.", ephemeral=True)
                    return
                await ticket_cog.create_ticket(interaction, interaction.data["values"][0])
            except Exception as e:
                print(f"Error in select callback: {e}")
                await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)

        select.callback = select_callback
        view = View(timeout=None)
        view.add_item(select)

        try:
            await ctx.send(embed=embed, view=view)
            print("Ticket panel sent successfully")
        except Exception as e:
            print(f"Error sending ticket panel: {e}")
            await ctx.send(f"❌ Error sending ticket panel: {e}")

def setup(bot):
    bot.add_cog(TicketPanel(bot))
