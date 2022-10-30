import discord
import asyncio
from discord.ext import commands
class Paginator:
    def __init__(self,title="",entries=[],prefix="",suffix="",color=discord.Colour.blue(),timeout=180):
        self.title=title
        self.entries=entries
        self.prefix=prefix
        self.suffix=suffix
        self.color=color
        self.pages=[]
        self.current=0
        self.timeout=timeout
    async def start(self,ctx,msg=None):
        current=self.current
        class PageButton(discord.ui.View):
            def __init__(self,title,entries,
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
                        self.add_item(PaginateButton(title,entries,prefix,suffix,color,txt,disable,style,id))
                if len(entries)==1:
                    self.add_item(PaginateButton(title,entries,prefix,suffix,color,args[2],disableds[2],styles[2],ids[2]))
        class PaginateButton(discord.ui.Button):
            def __init__(self,title,entries,prefix,suffix,color,txt,disable,style,id):
                self.title=title
                self.entries=entries
                self.prefix=prefix
                self.suffix=suffix
                self.color=color
                super().__init__(label=txt,style=style,custom_id=id,disabled=disable)
            async def callback(self,interaction:discord.Interaction):
                nonlocal current,ctx,msg
                if isinstance(ctx,commands.Context):
                  author=ctx.author
                elif isinstance(ctx,discord.Interaction):
                  author=ctx.user
                if author==interaction.user:
                    if self.custom_id=="next":
                        current+=1
                        if current<len(self.entries)-1:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=f"{self.prefix}{self.entries[current]}{self.suffix}",color=self.color).set_footer(text=f"{current+1}/{len(self.entries)}"),
                    view=PageButton(self.title,self.entries, self.prefix,self.suffix,self.color,disableds=[False,False,False,False,False]))
                        if current==len(self.entries)-1:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=f"{self.prefix}{self.entries[current]}{self.suffix}",color=self.color).set_footer(text=f"{current+1}/{len(self.entries)}"))
                            await interaction.message.edit(
                    view=PageButton(self.title,self.entries, self.prefix,self.suffix,self.color,disableds=[False,False,False,True,True]))
                    if self.custom_id=="back":
                        current-=1
                        if current>0:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=f"{self.prefix}{self.entries[current]}{self.suffix}",color=self.color).set_footer(text=f"{current+1}/{len(self.entries)}"),
                    view=PageButton(self.title,self.entries, self.prefix,self.suffix,self.color,disableds=[False,False,False,False,False])
                            )
                        if current==0:
                            await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=f"{self.prefix}{self.entries[current]}{self.suffix}",color=self.color).set_footer(text=f"{current+1}/{len(self.entries)}"))
                            await interaction.message.edit(
                    view=PageButton(self.title,self.entries, self.prefix,self.suffix,self.color,disableds=[True,True,False,False,False]))
                    if self.custom_id=="first":
                        current=0
                        await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=f"{self.prefix}{self.entries[current]}{self.suffix}",color=self.color).set_footer(text=f"{current+1}/{len(self.entries)}"),
                    view=PageButton(self.title,self.entries, self.prefix,self.suffix,self.color,disableds=[True,True,False,False,False]))
                    if self.custom_id=="end":
                        current=len(self.entries)-1
                        await interaction.response.edit_message(
                    embed=discord.Embed(title=self.title,description=f"{self.prefix}{self.entries[current]}{self.suffix}",color=self.color).set_footer(text=f"{current+1}/{len(self.entries)}"),
                    view=PageButton(self.title,self.entries, self.prefix,self.suffix,self.color,disableds=[False,False,False,True,True]))
                    if self.custom_id=="stop":
                        await interaction.response.edit_message(
                    view=None)
        embed=discord.Embed(title=self.title,description=f"{self.prefix}{self.entries[0]}{self.suffix}",color=self.color).set_footer(text=f"{current+1}/{len(self.entries)}")

        if not msg:
          if isinstance(ctx,commands.Context):
            m=await ctx.send(embed=embed,view=PageButton(self.title,self.entries,self.prefix,self.suffix,self.color))
          elif isinstance(ctx,discord.Interaction):
            m=await ctx.response.send_message(embed=embed,view=PageButton(self.title,self.entries,self.prefix,self.suffix,self.color))
        elif isinstance(msg,discord.Message):
            m=await msg.edit(embed=embed,view=PageButton(self.title,self.entries,self.prefix,self.suffix,self.color))
        elif isinstance(msg,discord.Interaction):
            m=await msg.response.edit_message(embed=embed,view=PageButton(self.title,self.entries,self.prefix,self.suffix,self.color))
        await asyncio.sleep(self.timeout)
        try:
          await m.edit(view=None)
        except:
          pass
