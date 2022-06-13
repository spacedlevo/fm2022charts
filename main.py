import pandas as pd
from matplotlib import pyplot as plt

from mplsoccer import PyPizza, add_image, FontManager

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))


df = pd.read_csv('moneyball.csv', na_values=['-'])
plt.style.use('dark_background')
# df['npGoals/90'] = (df['Gls'] - df['Pens S']) / (df['Mins'].str.replace(',','').astype('int') / 90)
# df['Asts/90'] = df['Asts/90'].str.replace('-', '0').astype(float)
# df['Ch C/90'] = df['Ch C/90'].str.replace('-', '0').astype(float)
# df['K Ps/90'] = df['K Ps/90'].str.replace('-', '0').astype(float)
# df['Hdrs W/90'] = df['Hdrs W/90'].str.replace('-','0').astype(float)
# df['Int/90'] = df['Int/90'].str.replace('-','0').astype(float)
# df['Drb/90'] = df['Drb/90'].str.replace('-','0').astype(float)

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
    slice_colors = ["#1A78CF"] * 4 + ["#FF9300"] * 3 + ["#D70232"]
    text_colors = ["#FFFFFF"] * 7 + ["#F2F2F2"]
    df = df[['Name', 'Club', 'Tackles Won per 90', 'Int/90','Hdrs W/90','Defensive Actions per 90', 'Asts/90', 'K Ps/90', 'Ps C/90', 'Drb/90']]
    df.fillna(0, inplace=True)
    df.set_index('Name', inplace=True)
    club = df.loc[player]['Club']
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
        color_blank_space="same",
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
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
        "Percentile Rank v Top 5 League Defenders",
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

    # add text
    fig.text(
        0.34, 0.925, "Defending        Passing       Possession", size=14,
        fontproperties=font_bold.prop, color="#FFFFFF"
    )

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.31, 0.9225), 0.025, 0.021, fill=True, color="#1a78cf",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.462, 0.9225), 0.025, 0.021, fill=True, color="#ff9300",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.632, 0.9225), 0.025, 0.021, fill=True, color="#d70232",
            transform=fig.transFigure, figure=fig
        ),
    ])
    plt.savefig(f'{player}_pizza.png')


def midfielder_pizza(df, player):
    slice_colors = ["#1A78CF"] * 4 + ["#FF9300"] * 4 + ["#D70232"] * 2
    text_colors = ["#FFFFFF"] * 8 + ["#F2F2F2"] * 2

    df = df[['Name', 'Club', 'Tackles Won per 90', 'Int/90','Hdrs W/90','Defensive Actions per 90', 'Asts/90', 'K Ps/90', 'Ps C/90','Ch C/90', 'Drb/90', 'Distance per 90']]
    df.fillna(0, inplace=True)
    df.set_index('Name', inplace=True)
    club = df.loc[player]['Club']
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
        color_blank_space="same",
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
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
        "Percentile Rank v Top 5 League Defenders",
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

    # add text
    fig.text(
        0.34, 0.925, "Defending        Passing       Possession", size=14,
        fontproperties=font_bold.prop, color="#FFFFFF"
    )

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.31, 0.9225), 0.025, 0.021, fill=True, color="#1a78cf",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.462, 0.9225), 0.025, 0.021, fill=True, color="#ff9300",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.632, 0.9225), 0.025, 0.021, fill=True, color="#d70232",
            transform=fig.transFigure, figure=fig
        ),
    ])
    plt.savefig(f'{player}_pizza.png')

defenders = df.loc[df['Position Category'] == 'Defender']
forwards = df.loc[df['Position Category'] == 'Forward']
mids = df.loc[df['Position Category'] == 'Midfielder']
mids.reset_index(inplace=True)
forwards.reset_index(inplace=True)
defenders.reset_index(inplace=True)

# create_scattergram(forwards['Name'], forwards['npxG per 90'], forwards['npGoals/90'], 'npxG/90 v npGoals/90')
# create_scattergram(forwards['Name'], forwards['npGoals/90'], forwards['Asts/90'], 'Asts/90 v npGoals/90')
# create_scattergram(mids['Name'], mids['Ch C/90'], mids['Asts/90'], 'Asts/90 v Chances Created/90')
# create_scattergram(mids['Name'], mids['K Ps/90'], mids['Asts/90'], 'Key Passes/90 v Assists/90')
# create_scattergram(defenders['Name'], defenders['Int/90'], defenders['Hdrs W/90'], 'Interceptions/90 v Headers Won/90')
midfielder_pizza(df, 'Michaël Cuisance')
midfielder_pizza(df, 'Christoph Baumgartner')