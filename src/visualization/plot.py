import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from scipy import interpolate
default_evloc_file_path = "./tmp/json/ev_loc/ev_loc0.json"

def create_smooth_3d_plot(df, save_path = "./tmp/img/plot.html", smooth_points=100):
    fig = go.Figure()
    
    df_sorted = df.sort_values('t')
    
    # 样条插值创建平滑曲线
    if len(df_sorted) >= 4:
        try:
            # 3D 样条插值
            tck, u = interpolate.splprep([
                df_sorted['x'].values,
                df_sorted['y'].values, 
                df_sorted['t'].values
            ], s=0)  # s=0 表示插值通过所有点
            
            u_new = np.linspace(0, 1, smooth_points)
            x_smooth, y_smooth, t_smooth = interpolate.splev(u_new, tck)
            
            # 添加平滑轨迹线
            fig.add_trace(go.Scatter3d(
                x=x_smooth,
                y=y_smooth,
                z=t_smooth,
                mode='lines',
                line=dict(
                    color=t_smooth,
                    colorscale='rainbow',
                    width=8,
                    showscale=True,
                    cmin=df_sorted['t'].min(),
                    cmax=df_sorted['t'].max(),
                    colorbar=dict(title='时间戳', x=0.85)
                ),
                name='平滑轨迹',
                hovertemplate=(
                    "X: %{x:.2f}<br>"
                    "Y: %{y:.2f}<br>"
                    "时间: %{z:.2f}<extra></extra>"
                )
            ))
            
        except Exception as e:
            print(f"样条插值失败: {e}")
            # 备用：使用直线连接
            add_straight_lines(fig, df_sorted)
    else:
        # 数据点太少，使用直线连接
        add_straight_lines(fig, df_sorted)
    
    # 添加标记点
    fig.add_trace(go.Scatter3d(
        x=df_sorted['x'],
        y=df_sorted['y'],
        z=df_sorted['t'],
        mode='markers',
        marker=dict(
            size=6,
            color=df_sorted['t'],
            colorscale='rainbow',
            cmin=df_sorted['t'].min(),
            cmax=df_sorted['t'].max(),
            line=dict(width=1, color='white')
        ),
        name='事件点',
        hovertemplate=(
            "X: %{x:.2f}<br>"
            "Y: %{y:.2f}<br>"
            "时间: %{z:.2f}<extra></extra>"
        )
    ))
    
    # 更新布局
    fig.update_layout(
        title='3D 平滑事件轨迹可视化',
        scene=dict(
            xaxis_title='X坐标',
            yaxis_title='Y坐标',
            zaxis_title='时间戳',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=1000,
        height=800
    )
    
    fig.write_html(save_path)
    print(f"✅ 平滑 3D 图已保存: {save_path}")

def add_straight_lines(fig, df_sorted):
    """添加直线连接（备用方案）"""
    for i in range(len(df_sorted) - 1):
        fig.add_trace(go.Scatter3d(
            x=df_sorted['x'].iloc[i:i+2],
            y=df_sorted['y'].iloc[i:i+2],
            z=df_sorted['t'].iloc[i:i+2],
            mode='lines',
            line=dict(
                color=df_sorted['t'].iloc[i],
                colorscale='rainbow',
                width=6
            ),
            showlegend=False
        ))
    
    


with open(default_evloc_file_path,"r",encoding="utf-8") as f:
    s = json.load(f)
    df = pd.DataFrame(s)
    df_sampled = df.iloc[::10].reset_index(drop=True)
    ############### info ###########################
    print("数据概览:")
    print(df.head())
    print(f"\n数据形状: {df.shape}")
    print(f"时间范围: {df['t'].min()} - {df['t'].max()}")
    print(f"坐标范围: x({df['x'].min()}-{df['x'].max()}), y({df['y'].min()}-{df['y'].max()})")
    ################# about ############################
    create_smooth_3d_plot(df_sampled)
    