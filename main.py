import pandas as pd
from matplotlib import pyplot as plt

from mplsoccer import PyPizza, add_image, FontManager

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))


df = pd.read_csv('moneyball.csv')
plt.style.use('dark_background')
print(df.tail())
df['npGoals/90'] = (df['Gls'] - df['Pens S']) / (df['Mins'].str.replace(',','').astype('int') / 90)
df['Asts/90'] = df['Asts/90'].str.replace('-', '0').astype(float)
df['Ch C/90'] = df['Ch C/90'].str.replace('-', '0').astype(float)
df['K Ps/90'] = df['K Ps/90'].str.replace('-', '0').astype(float)

positons_map = {}
for position in df['Position'].unique():
    if position.startswith('G'):
        positons_map[position] = 'Goalkeeper'
    elif position.startswith('DM') or position.startswith('M'):
        positons_map[position] = 'Midfielder'
    elif position.startswith('D') or position.startswith('W'):
        positons_map[position] = 'Defender'
    elif position.startswith('A') or position.startswith('S'):
        positons_map[position] = 'Forward'


df['Position Category'] = df['Position'].map(positons_map)

def create_scattergram(names, x, y, title):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.scatter(x, y)

    ax.set_xlabel(x.name, fontsize=14)
    ax.set_ylabel(y.name, fontsize=14)
    ax.set_title(title, fontsize=18)

    for i, txt in enumerate(names):
        ax.annotate(txt, (x[i], y[i]), xytext=(12,12), textcoords='offset points')
        plt.scatter(x, y)

    plt.plot([x.min(), x.max()], [y.mean(), y.mean()], ':')
    plt.plot([x.mean(), x.mean()], [y.min(), y.max()], ':')

    plt.savefig(f'{title.replace("/","_")}.png')


def defence_pizza(df, player):
    df = df[['Name', 'Club', 'Tackles Won per 90', 'Int/90', 'Defensive Actions per 90', 'Asts/90', 'K Ps/90', 'Ps C/90', 'Drb/90']]
    df.fillna(0, inplace=True)
    df.set_index('Name', inplace=True)
    club = df.loc[player]['Club']
    df['Int/90'] = df['Int/90'].str.replace('-','0').astype(float)
    df['Drb/90'] = df['Drb/90'].str.replace('-','0').astype(float)
    df_ranked = df.rank(numeric_only=True, pct=True)
    df_ranked = df_ranked.multiply(100)
    df_ranked = df_ranked.round(0)
    params = df_ranked.columns.values.tolist()
    player_row = df_ranked.loc[player]
    values = player_row.values.tolist()
    baker = PyPizza(
        params=params,
        straight_line_color="#000000",
        straight_line_lw=1,
        last_circle_lw=1,
        other_circle_lw=1,
        other_circle_ls="-."
    )

    fig, ax = baker.make_pizza(
        values,              # list of values
        figsize=(8, 8),      # adjust figsize according to your need
        param_location=110,  # where the parameters will be added
        kwargs_slices=dict(
            facecolor="cornflowerblue", edgecolor="#000000",
            zorder=2, linewidth=1
        ),                   # values to be used when plotting slices
        kwargs_params=dict(
            color="#FFFFFF", fontsize=12,
            fontproperties=font_normal.prop, va="center"
        ),                   # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=12,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                    # values to be used when adding parameter-values
    )

    # add title
    fig.text(
        0.515, 0.97, f"{player} - {club}", size=18,
        ha="center", fontproperties=font_bold.prop, color="#FFFFFF"
    )

    # add subtitle
    fig.text(
        0.515, 0.942,
        "Percentile Rank",
        size=15,
        ha="center", fontproperties=font_bold.prop, color="#FFFFFF"
    )

    # add credits
    CREDIT_1 = "data: Football Manager 2022 and Zealand Moneyball Spreadsheet"
    CREDIT_2 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"

    fig.text(
        0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}", size=9,
        fontproperties=font_italic.prop, color="#FFFFFF",
        ha="right"
    )
    plt.savefig(f'{player}_pizza.png')


forwards = df.loc[df['Position Category'] == 'Forward']
midandfor = df.loc[(df['Position Category'] == 'Forward') | (df['Position Category'] == 'Midfield')]
midandfor.reset_index(inplace=True)
forwards.reset_index(inplace=True)

create_scattergram(forwards['Name'], forwards['npxG per 90'], forwards['npGoals/90'], 'npxG/90 v npGoals/90')
create_scattergram(forwards['Name'], forwards['npGoals/90'], forwards['Asts/90'], 'Asts/90 v npGoals/90')
create_scattergram(midandfor['Name'], midandfor['Ch C/90'], midandfor['Asts/90'], 'Asts/90 v Chances Created/90')
create_scattergram(midandfor['Name'], midandfor['K Ps/90'], midandfor['Asts/90'], 'Key Passes/90 v Assists/90')
defence_pizza(df, 'Jordan Lotomba')