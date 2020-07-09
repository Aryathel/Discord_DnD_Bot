import discord
from discord.ext import commands
import datetime
import re
import random

"""Cog | Roll

This is a template put in place to be used
when creating a new Cog file.

NOTE: All commands are restricted to server use only by default,
remove the `@commands.guild_only()` line before any command that
should also be able to be used in a DM.
"""
class Roll(commands.Cog, name = "Roll"):
    """
    Command used for rolling numbers. See `!help roll` for more specifics.
    """
    def __init__(self, bot):
        self.bot = bot
        print(f"{bot.OK} {bot.TIMELOG()} Loaded Roll Cog.")

    @commands.guild_only()
    @commands.command(name = "roll", aliases = ['r'], help = "Just a placeholder.", brief = "If parameters then examples here")
    async def sample(self, ctx, *, arg):
        """Command | Roll

        Roll dice according to argument input.

        Functionality
        ----------------
        <num_die>d<num_sides>[kh<num>|kl<num>][+num]

        num_die - The number of die being rolled
        num_sides - the number of sides on the die being rolled
        kh<num> - keep the highest <num> rolls out of the results
        kl<num> - keep the lowesr <num> rolls out of the results
        +num - add a static number (usually a stat) to your roll.
        """
        p = re.compile("(?P<num_die>\d+)d(?P<num_sides>\d+)(?:\s?kh\s?(?P<kh>\d+)|\s?kl\s?(?P<kl>\d+))?(?:\s?\+\s?(?P<add>\d+)|\s?\-\s?(?P<sub>\d+))?", re.IGNORECASE)
        match = p.match(arg)
        if match:
            num_die = int(match.group('num_die'))
            num_sides = int(match.group('num_sides'))

            kh = match.group('kh')
            kl = match.group('kl')

            add = match.group('add')
            sub = match.group('sub')

            li = [num_die, num_sides, kh, kl, add, sub]

            rolls = sorted([random.randint(1, num_sides) for i in range(num_die)])

            fields = []
            rolls_trimmed = None

            if kh:
                kh = int(kh)
                if kh <= len(rolls):
                    rolls_trimmed = rolls[-kh:]
                    fields.append({
                        "name": f"{kh} Highest Roll(s)",
                        "value": ', '.join(f"`{roll}`" for roll in rolls_trimmed),
                        "inline": False
                    })
                else:
                    raise BadArgument(f"You cannot keep the {kh} highest rolls of {num_die} rolls.")
            elif kl:
                kl = int(kl)
                if kl <= len(rolls):
                    rolls_trimmed = rolls[:kl]
                    fields.append({
                        "name": f"{kl} Lowest Roll(s)",
                        "value": ', '.join(f"`{roll}`" for roll in rolls_trimmed),
                        "inline": False
                    })
                else:
                    raise BadArgument(f"You cannot keep the {kl} lowest rolls of {num_die} rolls.")

            for i in range(len(rolls)):
                fields.append({
                    "name": f"Roll #{i+1}",
                    "value": f"`{rolls[i]}`",
                    "inline": True
                })

            if rolls_trimmed:
                res_str = " + ".join(str(i) for i in rolls_trimmed)
                sub_total = sum(rolls_trimmed)
            else:
                res_str = " + ".join(str(i) for i in rolls)
                sub_total = sum(rolls)

            if add:
                add = int(add)
                fields.insert(0, {
                    "name": "Subtotal",
                    "value": f"{res_str} = `{sub_total}`",
                    "inline": False
                })
                res_str = res_str + f" + {add}"
                total = sub_total + add

            elif sub:
                sub = int(sub)
                fields.insert(0, {
                    "name": "Subtotal",
                    "value": f"{res_str} = `{sub_total}`",
                    "inline": False
                })
                res_str = res_str + f" - {sub}"
                total = sub_total - sub
            else:
                total = sub_total

            fields.insert(0, {
                "name": "Result",
                "value": f"{res_str} = `{total}`",
                "inline": False
            })

            embed = self.bot.embed_util.get_embed(
                title = f"{num_die}d{num_sides} Roll",
                author = ctx.author,
                fields = fields
            )
            await ctx.send(embed = embed)

        else:
            embed = self.bot.embed_util.get_embed(
                title = "Improper Roll",
                desc = "Here are some example rolls:\n`!r 2d20 + 1` - roll 2 d20 and add 1\n`!r 2d10kh1 3 3` - roll 2 d10, keep the highest 1, and subtract 3\n`!r 1d100` - roll 1 100-sided dice",
                author = ctx.author
            )
            await ctx.send(embed = embed)

def setup(bot):
    """Setup

    The function called by Discord.py when adding another file in a multi-file project.
    """
    bot.add_cog(Roll(bot))
