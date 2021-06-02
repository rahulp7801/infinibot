from discord.ext import commands
import discord
import asyncio

class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    def get_subcommand(self, command, lent = 1):
        arr =[]
        if hasattr(command, "commands"):
            for i in command.commands:
                arr.append(((i.name, self.get_command_signature(i)), i.short_doc))
        print(arr)
        return arr

    async def send_cog_help(self, cog):
        ctx = self.context
        try:
            commands = await self.filter_commands(cog.get_commands(), sort=True)
            embed = discord.Embed(title=((cog.icon + " ") if hasattr(cog, 'icon') else ' ') + cog.qualified_name)
            embed.colour = discord.Color.red()
            embed.description = cog.description if cog.description else "..."
            embed.set_footer(text=f'Use {self.clean_prefix}help [command] to get more information on a specific command!',)
            for i in commands:
                z = f"{i.short_doc}\t\n" if i.short_doc is not None else f"{'Placeholder'}\t\n"
                embed.add_field(name=f"""`{self.get_command_signature(i)}`""", value=f"{z}", inline=False)
                x = self.get_subcommand(i)
                if x:
                    for k in x:
                        embed.add_field(name=f"`{k[0][1]}`", value = f"{k[1] if k[1] != '' else '...'}", inline = False)
            await self.get_destination().send(embed=embed)
        except Exception as e:
            print(e)

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



