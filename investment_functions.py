import sympy as sp


# 変数の定義
e = sp.E
T, t, r = sp.symbols('T t r')
M_1, M_2 = sp.symbols('M_1 M_2')


# S1(t)の定義
def create_S1(M_1=M_1, t=t, r=r):
    return M_1/r * (e**(r*t) - 1)

# S2(t)の定義
def create_S2(M_2=M_2, T=T, t=t, r=r):
    S_0 = M_2/r * (e**(-r*T) - 1)
    return M_2/r * (e**(r*t) - 1) + S_0 * e**(r*t)

# 接続点の時間t'を導出する関数の定義
def create_t(M_1=M_1, M_2=M_2, T=T, r=r):
    return sp.log((M_1 - M_2)*e**(r*T)/(M_1*e**(r*T) - M_2))/r

# S1とS2をもとに、接続点の時間t'を導出(使わないかも...)
def deri_t(S_1=create_S1(), S_2=create_S2()):
    equation = sp.Eq(S_1, S_2)
    solution = sp.solve(equation, t)[0]
    return solution
    
# 区分的関数S(t)の定義
def create_S(S_1=create_S1(), S_2=create_S2(), conn_t=create_t()):
    S = sp.Piecewise((S_1, t <= conn_t), (S_2, t > conn_t))
    return S

# 区分的関数の接続点x, yを取得
def get_conn_point(piecewise_func):
    conditions = piecewise_func.args[0][1]
    t_value = conditions.rhs
    S_value = piecewise_func.subs(t, t_value)
    return t_value, S_value


###以下、チューニング済み###
# 入力を調整した関数S(t)
def create_S_by_subs(accumulation, withdrawal, start, end, yeild_y):
    S = create_S()
    S = S.subs([
        (M_1, accumulation), (M_2, withdrawal),
        (T, end-start), (t, t-start), (r, yeild_y),
    ])
    return S

# 調整した関数をnumpy用に変換
def convert_f_to_np(f):
    f_numpy = sp.lambdify(t, f, 'numpy')
    return f_numpy