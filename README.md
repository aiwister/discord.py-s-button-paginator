# discord.py-s-button-paginator
## how to use
button.Page(list)

If you are using discord.ext.commands,
```py
from button import Page
@bot.command()
async def pagetest(ctx):
  page=Page([i for i in range(20)])
  await page.start(ctx)
```
If using discord.app_commands,
```py
from button import Page
@tree.command()
async def pagetest(interaction:discord.Interaction):
  page=Page([i for i in range(20)])
  await page.start(interaction)
```
