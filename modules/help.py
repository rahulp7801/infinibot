from discord.ext import commands
import discord
import asyncio

class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    async def send_cog_help(self, cog):
        embed = discord.Embed()
        embed.set_author(icon_url=f"{cog.icon if hasattr(cog, 'icon') else ''}", name=cog.qualified_name)
        embed.colour = discord.Color.red()
        embed.description = cog.description if cog.description else ""
        embed.set_footer(text=f'Use {self.clean_prefix} [category] to get more information on a specific module!',)
        for i in cog.get_commands():
            embed.add_field(name=i.name, value = "Placeholder", inline = False)
        await self.get_destination().send(embed=embed)

    async def send_bot_help(self, mapping):
        ctx = self.context
        try:
            embed = discord.Embed(title = "InfiniBot Help", color = discord.Color.red())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            for cog, commands in sorted(mapping.items(), key=lambda x: len(x[1]), reverse=True):
                if cog is None or cog.qualified_name in ['Developers', 'No Category']:
                    continue
                name = f"{cog.icon if hasattr(cog, 'icon') else ''} {cog.qualified_name}"
                filtered = await self.filter_commands(commands, sort=True)
                if filtered:
                    embed.add_field(name=name, value = (cog.description or'...') + f"\n`{ctx.prefix}help {cog.qualified_name}`")
                embed.set_footer(text=f'Use {self.clean_prefix}help [category] to learn more about a category.')
            embed.add_field(name="About Us!",
                            value=f"[Invite Link](https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands) - [Support Server](https://discord.gg/4VnUA8ZXyH)\nSend the devs feedback by using `{ctx.prefix}feedback`!",
                            inline=False)
            await self.get_destination().send(embed=embed)
        except Exception as e:
            print(e)

