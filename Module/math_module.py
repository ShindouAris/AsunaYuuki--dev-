# bot_math.py

import ast
import operator as op
import disnake as discord
from disnake.ext import commands

# --- MODULE TÍNH TOÁN AN TOÀN ---
_OPERATORS: dict[type[ast.AST], op] = { # type: ignore
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def calculate(expr: str) -> float:
    node = ast.parse(expr, mode='eval').body
    return _eval(node)

def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError(f"Phép toán không hỗ trợ: {ast.dump(node)}")
# --- KẾT THÚC MODULE TÍNH TOÁN ---

# --- PHẦN DISCORD BOT ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'▶️ Bot đã sẵn sàng: {bot.user} (ID: {bot.user.id})')

@bot.command(name='calc', aliases=['math'])
async def _calc(ctx: commands.Context, *, expr: str):
    """
    Sử dụng: !calc 22*5
    """
    try:
        result = calculate(expr)
        await ctx.send(f'`{expr}` = **{result}**')
    except Exception as e:
        await ctx.send(f'❌ Lỗi: {e}')

@bot.command(name='help')
async def _help(ctx: commands.Context):
    msg = (
        "**Lệnh bot tính toán**\n"
        "`!calc <biểu_thức>` hoặc `!math <biểu_thức>`\n"
        "Hỗ trợ +, -, *, /, ** và ngoặc ().\n"
        "Ví dụ: `!calc (3+4)**2/7`"
    )
    await ctx.send(msg)
