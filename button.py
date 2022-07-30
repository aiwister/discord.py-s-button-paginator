import discord
import asyncio
pager={}

class PageButton(discord.ui.View):
    def __init__(self,emb,author,disableds=[True,True,False,False,False],styles=[discord.ButtonStyle.blurple,discord.ButtonStyle.blurple,discord.ButtonStyle.danger,discord.ButtonStyle.blurple,discord.ButtonStyle.blurple],args=["⏪","◀️","⏹","▶️","⏩"],ids=["first","-1","stop","1","end"],prefix="",suffix=""):
        super().__init__()
        if len(emb)>1:
          for disable,style,txt,id in zip(disableds,styles,args,ids):
            self.add_item(HugaButton(emb,author,txt,disable,style,id,prefix,suffix))
        if len(emb)==1:
          self.add_item(HugaButton(emb,author,args[2],styles[2],ids[2],prefix,suffix))
        self.emb=emb
        self.args=args
        self.ids=ids

class Pag:
  def __init__(self,embed,author,prefix="",suffix=""):
    self.embed=embed
    self.prefix=prefix
    self.suffix=suffix
    self.author=author 
  async def start(self,interaction):
    global pager
    if isinstance(interaction,discord.Interaction):
      msg=await interaction.response.send_message(embed=discord.Embed(description=f"{self.prefix}{self.embed[0]}{self.suffix}"),view=PageButton(emb=self.embed,author=self.author,prefix=self.prefix,suffix=self.suffix))
    if isinstance(interaction,discord.ext.commands.Context):
      msg=await interaction.send(embed=discord.Embed(description=f"{self.prefix}{self.embed[0]}{self.suffix}"),view=PageButton(emb=self.embed,author=self.author,prefix=self.prefix,suffix=self.suffix))
    pager[str(msg.id)]=0
      
class HugaButton(discord.ui.Button):
    def __init__(self,emb,author,txt,disable,style,id,prefix,suffix):
        self.emb=emb
        self.prefix=prefix
        self.suffix=suffix
        self.author=author
        self.disable=disable
        super().__init__(label=txt,style=style,custom_id=id,disabled=disable)


    async def callback(self,interaction):
      global pager
      if self.author==interaction.user:
       if self.custom_id=="1" or self.custom_id=="-1":
        pager[str(interaction.message.id)]+=int(self.custom_id)
        if pager[str(interaction.message.id)]>0 and pager[str(interaction.message.id)]<len(self.emb)-1:
         await interaction.message.edit(view=PageButton(emb=self.emb,author=self.author,disableds=[False,False,False,False,False],prefix=self.prefix,suffix=self.suffix))
        if pager[str(interaction.message.id)]==0:
         await interaction.message.edit(view=PageButton(emb=self.emb,author=self.author,disableds=[True,True,False,False,False],prefix=self.prefix,suffix=self.suffix))
        if pager[str(interaction.message.id)]==len(self.emb)-1:
         await interaction.message.edit(view=PageButton(emb=self.emb,author=self.author,disableds=[False,False,False,True,True],prefix=self.prefix,suffix=self.suffix))
       if self.custom_id=="first":
        pager[str(interaction.message.id)]=0
        await interaction.message.edit(view=PageButton(emb=self.emb,author=self.author,disableds=[True,True,False,False,False],prefix=self.prefix,suffix=self.suffix))
       if self.custom_id=="end":
         pager[str(interaction.message.id)]=len(self.emb)-1
         await interaction.message.edit(view=PageButton(emb=self.emb,author=self.author,disableds=[False,False,False,True,True],prefix=self.prefix,suffix=self.suffix))
       await interaction.response.edit_message(embed=discord.Embed(description=f"{self.prefix}{self.emb[pager[str(interaction.message.id)]]}{self.suffix}"))
       if self.custom_id=="stop":
            await interaction.response.edit_message(view=None)
