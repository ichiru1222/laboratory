import numpy as np
from tqdm import tqdm
import math

"""Max Entroy IRL
"""

"""Φ(s)の計算
"""
def phi(state: int, nS: int):
    phi_s = np.zeros(nS)

    for i in range(nS):
        if i == state:
            phi_s[i] = 1
        else:
            phi_s[i] = 0

    return phi_s

def Mu(traj, nS: int):
    """軌跡一つの特徴量を計算
    """
    Mu_s = np.zeros(nS)
    for s in traj:
        Mu_s = Mu_s + phi(s, nS)
    return Mu_s

def MuE(trajectories, nS: int):
    """軌跡集合の特徴量期待値を計算
    """
    MuE_m = np.zeros(nS)
    for traj in trajectories:
        MuE_m = MuE_m + Mu(traj, nS)
    
    MuE_m = MuE_m / len(trajectories)

    return MuE_m

def MaxEntIRL(env, P, trajectories, n_iter: int, max_step, learning_rate: float):
    """MaxEntIRL 本体
    """
    # 状態遷移確率行列を環境から取得
    P = P

    global muE # 必要？

    muE = MuE(trajectories, env.nS)

    # 更新していく重みを定義
    theta = np.random.uniform(-0.5, 0.5, size=env.nS)
    # 特徴量ベクトルの初期化
    feature_matrix = np.eye(env.nS)
    # 報酬の初期化　重みと特徴量ベクトルの内積
    R = np.dot(theta, feature_matrix.T)
    print("initial reward")
    print(R)

    norm_grad = float("inf")

    for _ in tqdm(range(n_iter)):
        R = np.dot(theta, feature_matrix.T)

        """Backward pass"""
        policy = np.zeros([env.nS, env.nA])

        Z_a = np.zeros([env.nS, env.nA])
        Z_s = np.ones([env.nS])

        # Note:N回のイテレーションの”N”は，軌跡の長さ
        for n in range(max_step):
            # オーバーフロー対策
            R_max = np.max(R)
            Z_a = np.einsum("san, s, n -> sa", P, np.exp(R - R_max), Z_s) #nはnext_stateの意
            Z_s = np.sum(Z_a, axis = 1) #Z_sの初期化位置は"ここ"

        # NOTE ここはソフトマックス関数の形になっているためオーバーフローが起こる
        policy = np.einsum("sa, s -> sa", Z_a, 1/Z_s)#各状態における行動選択確率：：：これがsoft_Q_policy

        """Forward pass"""
        Dt = np.zeros([max_step, env.nS]) #論文アルゴリズム中の Dを指す
         
        #initialize mu[0] based on trajectories initial state
        for trajectory in trajectories:
            Dt[0][trajectory[0]] += 1
        Dt /= len(trajectories)
                
        for t in range(1, max_step):
            Dt[t] = np.einsum("s, sa, san -> n", Dt[t-1], policy, P) 
        Ds = Dt.sum(axis=0)#頻度

        grad = muE - feature_matrix.T.dot(Ds)
        norm_grad = np.linalg.norm(grad, ord=2)

        print("norm_grad")
        print(norm_grad)

        theta += learning_rate * grad #最大化問題なので勾配降下が勾配上昇（勾配を加える）になっていることに注意
        # print("theta")
        # print(theta)
        # print("############")
        # # print("R")
        # # print(R)
        # print("policy")
        # print(policy)
    
    print("MaxEntIRL ended.")
    return R, policy, theta, Z_s

if __name__ == "__main__":
    
    import sys
    sys.path.append("../env")
    from maxent_env import Environment
    print(sys.path)

    env = Environment(3, 3, 1)

    trajectories = np.array([[0, 2, 4], [1, 2, 4], [8, 2, 4]])

    R, policy, theta, Z_s = MaxEntIRL(env, trajectories, n_iter=50, max_step=len(trajectories[0]), learning_rate=0.01)
    print(R, Z_s)