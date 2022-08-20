import discord
import asyncio
from discord.ext import commands
class Paginator:
    def __init__(self,title="",entries=[],author="",prefix="",suffix="",color=discord.Colour.blue()):
        self.title=title
        self.entries=entries
        self.author=author
        self.prefix=prefix
        self.suffix=suffix
        self.color=color
        self.pages=[]
        self.current=0
    async def start(self,ctx):
        current=self.current
        class PageButton(discord.ui.View):
            def __init__(self,title,entries,author,
                  prefix="",
                  suffix="",
                  color=discord.Colour.blue(),
                  disableds=[True,True,False,False,False],
                  styles=[discord.ButtonStyle.blurple,discord.ButtonStyle.blurple,discord.ButtonStyle.danger,discord.ButtonStyle.blurple,discord.ButtonStyle.blurple],
                  args=["⏪","◀️","⏹","▶️","⏩"],
                  ids=["first","back","stop","next","end"]):
                super().__init__()
                if len(entries)>1:
                    for disable,style,txt,id in zip(disableds,styles,args,ids):
                        self.add_item(PaginateButton(title,entries,author,prefix,suffix,color,txt,disable,style,id))
                if len(entries)==1:
                    self.add_item(PaginateButton(title,entries,author,prefix,suffix,color,args[2],disableds[2],styles[2],ids[2]))
        class PaginateButton(discord.ui.Button):
            def __init__(self,title,entries,author,prefix,suffix,color,txt,disable,style,id):
                self.title=title
                self.entries=entries
                self.author=author
                self.prefix=prefix
                self.suffix=suffix
                self.color=color
                super().__init__(label=txt,style=style,custom_id=id,disabled=disable)
            async def callback(self,interaction:discord.Interaction):
                nonlocal current
                if self.author==interaction.user:
                    if self.custom_id=="next":
                        current+=1
                        if current<len(self.entries)-1:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=self.prefix+self.entries[current]+self.suffix,color=self.color),
                    view=PageButton(self.title,self.entries,self.author,disableds=[False,False,False,False,False]))
                        if current==len(self.entries)-1:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=self.prefix+self.entries[current]+self.suffix,color=self.color))
                            await interaction.message.edit(
                    view=PageButton(self.title,self.entries,self.author,disableds=[False,False,False,True,True]))
                    if self.custom_id=="back":
                        current-=1
                        if current>0:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=self.prefix+self.entries[current]+self.suffix,color=self.color),
                    view=PageButton(self.title,self.entries,self.author,disableds=[False,False,False,False,False])
                            )
                        if current==0:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=self.prefix+self.entries[current]+self.suffix,color=self.color))
                            await interaction.message.edit(
                    view=PageButton(self.title,self.entries,self.author,disableds=[True,True,False,False,False]))
                    if self.custom_id=="first":
                        current=0
                        await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=self.prefix+self.entries[current]+self.suffix,color=self.color),
                    view=PageButton(self.title,self.entries,self.author,disableds=[True,True,False,False,False]))
                    if self.custom_id=="end":
                        current=len(self.entries)-1
                        await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=self.prefix+self.entries[current]+self.suffix,color=self.color),
                    view=PageButton(self.title,self.entries,self.author,disableds=[False,False,False,True,True]))
                    if self.custom_id=="stop":
                        await interaction.response.edit_message(
                    view=None)
        embed=discord.Embed(title=self.title,description=self.prefix+self.entries[0]+self.suffix)
        if isinstance(ctx,commands.Context):
            await ctx.send(embed=embed,view=PageButton(self.title,self.entries,self.author,self.prefix,self.suffix,self.color))
        if isinstance(ctx,discord.Interaction):
            await ctx.response.send_message(embed=embed,view=PageButton(self.title,self.entries,self.author,self.prefix,self.suffix,self.color))
