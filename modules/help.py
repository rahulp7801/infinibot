from discord.ext import commands
import discord
import asyncio

class Help(commands.HelpCommand):
    '''
    Inherit from the base Help Command and create a help command for the bot
    '''

    def get_command_signature(self, command):
        '''
        :param command: The command we want to get the use for
        Example command: "afk"
        :return:
        The expected input from the user:
        ".afk Sleeping"
        '''
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    def get_subcommand(self, command):
        '''
        :param command: The command we need to check for subcommands
        :return:
        None if there are no subcommands, or a list of tuples with the subcommand's signature and name (short description)
        '''
        arr =[]
        if hasattr(command, "commands"):
            for i in command.commands:
                arr.append(((i.name, self.get_command_signature(i)), i.short_doc))
        return None if not arr else arr

    def get_aliases(self, mapping):
        '''
        :param mapping: The command name's mapping to the actual command itself
        :return:
        A string of aliases or None if there aren't any
        '''
        if mapping.aliases:
            return ", ".join(mapping.aliases)

    async def send_cog_help(self, cog):
        '''
        :param cog: The cog that was requested for help
        :return:
        An embed with a list of commands and their respective signatures
        '''
        ctx = self.context
        try:
            commands = await self.filter_commands(cog.get_commands(), sort=True)
            embed = discord.Embed(title=((cog.icon + " ") if hasattr(cog, 'icon') else ' ') + cog.qualified_name)
            embed.colour = discord.Color.red()
            embed.description = cog.description if cog.description else "..."
            embed.set_footer(text=f'Use {self.clean_prefix}help [command] to get more information on a specific command!',)
            for i in commands:
                z = f"{i.short_doc}\t\n" if i.short_doc != '' else f"{'Placeholder'}\t\n"
                embed.add_field(name=f"""`{self.get_command_signature(i)}`""", value=f"{z}", inline=False)
                x = self.get_subcommand(i)
                if x:
                    for k in x:
                        embed.add_field(name=f"`{k[0][1]}`", value = f"{k[1] if k[1] != '' else '...'}", inline = False)
            await self.get_destination().send(embed=embed)
        except Exception as e:
            print(e)

    async def send_bot_help(self, mapping):
        '''
        :param mapping: The mapping of cog names to cogs (a dictionary)
        :return:
        The help menu as an embed
        '''
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

    async def send_command_help(self, command):
        '''
        :param command: The command that needs help
        :return:
        An embed with the aliases, usage, and help for a command
        '''
        try:
            embed = discord.Embed(color = discord.Color.green())
            embed.title = f"{self.get_command_signature(command)}"
            embed.set_footer(text=f"{('Aliases: ' + self.get_aliases(command)) if self.get_aliases(command) is not None else ''}")
            if command.help:
                embed.description = command.help
            else:
                embed.description = 'No help for this command'
            await self.get_destination().send(embed=embed)
        except Exception as e:
            print(e)



