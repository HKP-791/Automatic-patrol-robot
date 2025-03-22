# -*- coding: utf-8 -*-
"""
路径搜索示例 (单观测)
 Created on Wed Mar 13 2024 18:18:07
 Modified on 2024-3-13 18:18:07
 
 @auther: HJ https://github.com/zhaohaojie1998
"""
#

# 1.环境实例化
from path_plan_env import StaticPathPlanning, NormalizedActionsWrapper
env = NormalizedActionsWrapper(StaticPathPlanning())


# 2.策略加载
import onnxruntime as ort
import os
pkg_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(pkg_dir)
grand_dir = os.path.dirname(os.path.dirname(os.path.dirname(parent_dir)))
# 更改下面的模型名称
model_dir = os.path.join(grand_dir, 'model', 'policy_static.onnx')
policy = ort.InferenceSession('/home/ica_l/auto_parking/src/rosmaster_x3/model/policy_static.onnx')


# 3.仿真LOOP
from copy import deepcopy

MAX_EPISODE = 1
lst = []
for episode in range(MAX_EPISODE):
    ## 获取初始观测
    obs = env.reset()
    ## 进行一回合仿真
    for steps in range(env.max_episode_steps):
        # 可视化
        env.render()
        # 决策
        obs = obs.reshape(1, *obs.shape)                      # (*shape, ) -> (1, *shape, )
        act = policy.run(['action'], {'observation': obs})[0]
        act = act.flatten()                                   # (1, dim, ) -> (dim, )
        # 仿真
        next_obs, _, _, info = env.step(act)
        lst.append(act)
        # 回合结束
        if info["terminal"]:
            print('回合: ', episode,'| 状态: ', info,'| 步数: ', steps) 
            break
        else:
            obs = deepcopy(next_obs)
    print(act)
    #end for
#end for




#             ⠰⢷⢿⠄
#         ⠀⠀⠀⠀⠀⣼⣷⣄
#         ⠀⠀⣤⣿⣇⣿⣿⣧⣿⡄
#         ⢴⠾⠋⠀⠀⠻⣿⣷⣿⣿⡀
#         🏀   ⢀⣿⣿⡿⢿⠈⣿
#          ⠀⠀⢠⣿⡿⠁⢠⣿⡊⠀⠙
#          ⠀⠀⢿⣿⠀⠀⠹⣿
#           ⠀⠀⠹⣷⡀⠀⣿⡄
#            ⠀⣀⣼⣿⠀⢈⣧ 
#
#       你。。。干。。。嘛。。。
#       哈哈。。唉哟。。。