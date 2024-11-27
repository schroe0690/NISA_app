import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from investment_functions import create_S_by_subs, get_conn_point, convert_f_to_np

# タイトル
st.title('積み立てNISAシミュレーション')
'''
元本も使い切ることを考慮した積立投資計算ツール\n
積み立て終了までは切り崩さず、積み立て終了後に切り崩しが始まります！\n
'''

# 入力欄
st.subheader('数値入力欄')
with st.form(key='profile_form'):
    col1, col2 = st.columns(2)
    
    # 左側
    with col1:
        accumulation = st.number_input('月間積み立て額 (万円)', min_value=1.0, max_value=10.0, value=5.0, step=0.1)
        withdrawal = st.number_input('月間切り崩し額 (万円)', min_value=1.0, value=30.0, step=0.1)
        yeild_y = st.number_input('年利 (%)', min_value=0.0, value=5.0, step=0.01)
    
    # 右側
    with col2:
        start_age = st.number_input('投資を始める年齢', min_value=0, value=20)
        end_age = st.number_input('資産を使い切る年齢', min_value=1, value=80)
        # ボタン
        submit_btm = st.form_submit_button('シミュレーション開始')
        
# ボタンを押したときの処理
if submit_btm:
    # 計算
    accumulation = 12 * accumulation
    withdrawal = -12 * withdrawal
    yeild_y = float(yeild_y) / 100
    S = create_S_by_subs(accumulation, withdrawal, start_age, end_age, yeild_y)
    t_max, S_max = get_conn_point(S)
    
    # グラフ用に変換
    S_numpy = convert_f_to_np(S)
    t = np.linspace(start_age, end_age, 1000)
    df = pd.DataFrame({'年齢': t, '資産（万円）': S_numpy(t)})
    
    # プロット
    st.subheader('資産の推移')
    fig, ax = plt.subplots()
    st.line_chart(df, x='年齢', y='資産（万円）')
    
    # 詳細表示
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric(label='総投資額', value=f'{round(accumulation * (t_max-start_age))}万円')
    with col4:
        st.metric(label='積み立て終了年齢', value=f'約{round(t_max)}歳')
    with col5:
        st.metric(label='積み立て終了時資産', value=f'{round(S_max)}万円')
            