import sympy as sp

# 変数の定義
e = sp.E
t, T, M, r = sp.symbols('t T M r')
M_1, M_2 = sp.symbols('M_1 M_2')


# f(t)の定義
def create_f(t=t, M_1=M_1, r=r):
    return M_1/r * (e**(r*t) - 1)

# g(t)の定義
def create_g(t=t, T=T, M_2=M_2, r=r):
    x = -M_2/r * (1 - sp.exp(-r*T))
    return x * sp.exp(r*t) + M_2/r * (sp.exp(r*t) - 1)

# fg(t)の定義 (区分的関数)
def create_fg(t=t, T=T, M_1=M_1, M_2=M_2, r=r):
    f, g  = create_f(), create_g()
    t_max = create_t_max()
    fg = sp.Piecewise((f, t <= t_max), (g, t > t_max))
    return fg

# t_maxの定義
def create_t_max():
    f, g  = create_f(), create_g()
    equation = sp.Eq(f, g)
    solution = sp.solve(equation, t)[0]
    return solution
    # return sp.log((M_1-M_2)*e**(r*T)/(M_1*e**(r*T)-M_2)) / r


# モデルに合わせ調整したfg
def adjusted_fg(accumulation, withdrawal, yeild_y, start_age, end_age):
    x_axis = t - start_age              # 開始位置調整
    life_exp = end_age - start_age      # 残り期間(資産を使い切るまでの)
    annual_accum = 12 * accumulation    # 年間積み立て額
    annual_withd = -12 * withdrawal     # 年間切り崩し額
    yeild_y = yeild_y / 100             # 年利の数値調整
    fg_args = [(t, x_axis), (T, life_exp), (M_1, annual_accum), (M_2, annual_withd), (r, yeild_y)]
    fg = create_fg().subs(fg_args)
    return fg

def calc_amount(fg, age):
    amount = fg.subs(t, age)
    return amount

# t_maxを算出
def calc_t_max(accumulation, withdrawal, yeild_y, start_age, end_age):
    life_exp = end_age - start_age      # 残り期間(資産を使い切るまでの)
    annual_accum = 12 * accumulation    # 年間積み立て額
    annual_withd = -12 * withdrawal     # 年間切り崩し額
    yeild_y = yeild_y / 100             # 年利の数値調整
    t_max_args = [(T, life_exp), (M_1, annual_accum), (M_2, annual_withd), (r, yeild_y)]
    t_max = create_t_max().subs(t_max_args) + start_age
    return t_max

# 調整した関数をnumpy用に変換
def convert_fg_to_np(fg):
    fg_numpy = sp.lambdify(t, fg, 'numpy')
    return fg_numpy