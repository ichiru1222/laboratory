import numpy as np

class Environment:
    def __init__ (self, nS1, nS2, action_range=4):
        self.action_range = action_range
        self.actions = self.make_actions(action_range)
        self.nS1 = nS1
        self.nS2 = nS2
        self.nS = nS1 * nS2
        self.nA = len(self.actions)
        self.P = self.make_P()
    

    def make_actions(self,action_range):
        actions = []
        for i in range(-action_range, action_range+1):
            for j in range(-action_range, action_range+1):
                action = np.zeros(2)
                action[0] = i
                action[1] = j
                actions.append(action)
        return actions

    def is_possible_action(self, s1, s2, action):
        """行動が可能か判定
        """
        to_s1 = s1
        to_s2 = s2

        to_s1 += action[0]
        to_s2 += action[1]

        if self.nS1 <= to_s1 or 0 > to_s1:
            return False
        if self.nS2 <= to_s2 or 0 > to_s2:
            return False
        return True

    def to_scalar(self, s1, s2):
        # 二次元ベクトルの状態をスカラー値に
        s = self.nS1 * s2 + s1
        s = int(s)
        return s
    def to_vector(self, s):
        # スカラーをベクトルに
        s1 = s % self.nS1
        s2 = s // self.nS1
        return s1, s2

    
    
    def make_P(self):
        """状態遷移確率行列の作成
        """
        #Pの初期化
        P = np.zeros((self.nS, self.nA, self.nS))

        for s_idx in range(self.nS):
            for a_idx in range(self.nA):
                action = self.actions[a_idx]
                s1, s2 = self.to_vector(s_idx)
                if self.is_possible_action(s1, s2, action):
                    next_s1 = s1 + action[0]
                    next_s2 = s2 + action[1]
                    next_s = self.to_scalar(next_s1, next_s2)
                    P[s_idx][a_idx][next_s] += 1

        return P




        



if __name__ == "__main__":
    import numpy
    
    env = Environment(11, 11, 4)
    numpy.set_printoptions(threshold=numpy.inf)
    print(env.actions)

    print(env.P)

