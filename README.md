# discord.py-s-button-paginator
## how to use
button.Page(list)

If you are using discord.ext.commands,
```py
from button import Page
@bot.command()
async def pagetest(ctx):
  page=Page(embed=[i for i in range(20)],author=ctx.author)
  await page.start(ctx)
```
If using discord.app_commands,
```py
from button import Page
@tree.command()
async def pagetest(interaction:discord.Interaction):
  page=Page(embed=[i for i in range(20)],author=interaction.user)
  await page.start(interaction)
```
