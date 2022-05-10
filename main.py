import discord

class PageButton(discord.ui.View):
    def __init__(self,emb,styles=[discord.ButtonStyle.blurple,discord.ButtonStyle.blurple,discord.ButtonStyle.danger,discord.ButtonStyle.blurple,discord.ButtonStyle.blurple],args=["⏪","◀️","⏹","▶️","⏩"],ids=["first","back","stop","next","end"],prefix=None,suffix=None):
        super().__init__()
        if len(emb)>1:
          for style,txt,id in zip(styles,args,ids):
            self.add_item(HugaButton(emb,txt,style,id,prefix,suffix))
        if len(emb)==1:
          self.add_item(HugaButton(emb,args[2],styles[2],ids[2],prefix,suffix))
        self.emb=emb
        self.args=args
        self.ids=ids

class Page:
  def __init__(self,embed,prefix=None,suffix=None):
    self.embed=embed
    self.prefix=prefix
    self.suffix=suffix
  async def start(self,interaction):
    if isinstance(interaction,discord.Interaction):
      await interaction.response.send_message(embed=discord.Embed(description=f"{self.prefix}{self.embed[0]}{self.suffix}"),view=PageButton(self.embed,prefix=self.prefix,suffix=self.suffix))
    if isinstance(interaction,discord.ext.commands.Context):
      await interaction.send(embed=discord.Embed(description=f"{self.prefix}{self.embed[0]}{self.suffix}"),view=PageButton(self.embed,prefix=self.prefix,suffix=self.suffix))
n=0
class HugaButton(discord.ui.Button):
    def __init__(self,emb,txt,style,id,prefix,suffix):
        self.emb=emb
        self.prefix=prefix
        self.suffix=suffix
      
        super().__init__(label=txt,style=style,custom_id=id)

    async def callback(self, interaction: discord.Interaction):
        global n
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
