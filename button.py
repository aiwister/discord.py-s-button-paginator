import discord
import asyncio
class PageButton(discord.ui.View):
    def __init__(self,emb,author,styles=[discord.ButtonStyle.blurple,discord.ButtonStyle.blurple,discord.ButtonStyle.danger,discord.ButtonStyle.blurple,discord.ButtonStyle.blurple],args=["⏪","◀️","⏹","▶️","⏩"],ids=["first","back","stop","next","end"],prefix="",suffix="",timeout=180):
        super().__init__()
        if len(emb)>1:
          for style,txt,id in zip(styles,args,ids):
            self.add_item(HugaButton(emb,author,txt,style,id,prefix,suffix,timeout))
        if len(emb)==1:
          self.add_item(HugaButton(emb,author,args[2],styles[2],ids[2],prefix,suffix,timeout))
        self.emb=emb
        self.args=args
        self.ids=ids

class Pager:
  def __init__(self,embed,author,timeout,prefix="",suffix=""):
    self.embed=embed
    self.prefix=prefix
    self.suffix=suffix
    self.author=author
    self.timeout=timeout
    
  async def start(self,interaction):
    if isinstance(interaction,discord.Interaction):
      msg=await interaction.response.send_message(embed=discord.Embed(description=f"{self.prefix}{self.embed[0]}{self.suffix}"),view=PageButton(emb=self.embed,author=self.author,prefix=self.prefix,suffix=self.suffix,timeout=self.timeiut))
    if isinstance(interaction,discord.ext.commands.Context):
      msg=await interaction.send(embed=discord.Embed(description=f"{self.prefix}{self.embed[0]}{self.suffix}"),view=PageButton(emb=self.embed,author=self.author,prefix=self.prefix,suffix=self.suffix,timeout=self.timeout))
    if self.timeout:
      await asyncio.sleep(self.timeout)
      await msg.edit(view=None)
n=0
class HugaButton(discord.ui.Button):
    def __init__(self,emb,author,txt,style,id,prefix,suffix,timeout):
        self.emb=emb
        self.prefix=prefix
        self.suffix=suffix
        self.author=author
        self.timeout=timeout
        super().__init__(label=txt,style=style,custom_id=id)

    async def callback(self,interaction):
      global n
      if self.author==interaction.user:
        if self.custom_id=="next":
          if n<=len(self.emb):
            await interaction.response.edit_message(embed=discord.Embed(description=f"{self.prefix}{self.emb[n+1]}{self.suffix}"))
            n+=1
          else:
            pass
        if self.custom_id=="back":
          if n>0:
            n-=1
            await interaction.response.edit_message(embed=discord.Embed(description=f"{self.prefix}{self.emb[n]}{self.suffix}"))
            pass
          else:
            pass
        if self.custom_id=="first":
          n=0
          await interaction.response.edit_message(embed=discord.Embed(description=f"{self.prefix}{self.emb[0]}{self.suffix}"))
        if self.custom_id=="end":
          n=len(self.emb)-1
          await interaction.response.edit_message(embed=discord.Embed(description=f"{self.prefix}{self.emb[-1]}{self.suffix}"))
        if self.custom_id=="stop":
            await interaction.response.edit_message(view=None)
            n=0
        else:
          if self.timeout:
            await asyncio.sleep(self.timeout)
            n=0
