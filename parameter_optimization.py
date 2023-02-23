import os
import optuna
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image

import warnings
warnings.simplefilter('ignore')

import function as f

def exe_opt():

    # 最適化の条件設定, 変数を与える関数
    study = optuna.multi_objective.create_study(
        directions=["maximize", "maximize"],
        sampler=optuna.multi_objective.samplers.NSGAIIMultiObjectiveSampler(seed = 1)
    )
    # 最適化の実行
    study.optimize(f.objective, n_trials=200)

    return study

def analyze(study):

    # 最適化過程で得た履歴データの取得。get_trials()メソッドを使用
    trials = {str(trial.values): trial for trial in study.get_trials()} # target values gotten y1 and y2
    trials = list(trials.values())

    # グラフにプロットするため、目的変数をリストに格納する
    trial_df = pd.DataFrame({})
    y1_all_list = []
    y2_all_list = []
    for i, trial in enumerate(trials, start=1):
        y1_all_list.append(trial.values[0])
        y2_all_list.append(trial.values[1])
        trial_result = {"trial":i,
                        "y1":trial.values[0],
                        "y2":trial.values[1],
                        }
        # each parameter
        for key, value in trial.params.items():
            # each params
            trial_result[key] = value
         # append to df
        trial_df = trial_df.append(trial_result, ignore_index=True)
    # save trial df
    trial_df.to_csv("plots/trial_result.csv", index=False)

    # パレート解の取得。get_pareto_front_trials()メソッドを使用
    trials = {str(trial.values): trial for trial in study.get_pareto_front_trials()}
    trials = list(trials.values())
    trials.sort(key=lambda t: t.values)

    # グラフプロット用にリストで取得。またパレート解の目的変数と説明変数をcsvに保存する
    trial_parato_df = pd.DataFrame({})
    y1_list = []
    y2_list = []
    with open('pareto_data_real.csv', 'w') as f:
        for i, trial in enumerate(trials, start=1):
            if i == 1:
                columns_name_str = 'trial_no,y1,y2'
            data_list = []
            data_list.append(trial.number)

            # y value
            y1_value = trial.values[0]
            y2_value = trial.values[1]
            y1_list.append(y1_value)
            y2_list.append(y2_value)
            data_list.append(y1_value)
            data_list.append(y2_value)
            trial_parato_result = {"trial":i,
                            "y1":trial.values[0],
                            "y2":trial.values[1],
                            }

            for key, value in trial.params.items():
                data_list.append(value)
                if i == 1:
                    columns_name_str += ',' + key
                # each params
                trial_parato_result[key] = value
            if i == 1:
                f.write(columns_name_str + '\n')
            data_list = list(map(str, data_list))
            data_list_str = ','.join(data_list)
            f.write(data_list_str + '\n')

            # append to df
            trial_parato_df = trial_parato_df.append(trial_parato_result, ignore_index=True)
    # save trial df
    trial_parato_df.to_csv("plots/trial_parato_front_result.csv", index=False)

    # --------------------------------------
    # パレート解を図示
    # --------------------------------------
    # setting of graph
    # plot
    plot_fig_list = list()
    os.makedirs("plots", exist_ok=True)
    for i in range(len(y1_all_list)):
        plt.figure(figsize=(10,6))
        plt.scatter(y1_all_list[:i], y2_all_list[:i], c='blue', label='all trials', s=20)
        plt.title("multiobjective optimization")
        plt.xlabel("Y1")
        plt.ylabel("Y2")
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plot_fig_list.append("plots/pareto_graph_real_{}.png".format(i))
        plt.savefig("plots/pareto_graph_real_{}.png".format(i))
    # make gif image
    # create gif file
    images = list(map(lambda file : Image.open(file), plot_fig_list))
    images[0].save("plots/optimization_step.gif", save_all=True, append_images=images[1:], duration=400, loop=0)

    # last result
    plt.figure(figsize=(10,6))
    plt.scatter(y1_all_list, y2_all_list, c='blue', label='all trials', s=20)
    plt.scatter(y1_list, y2_list, c='red', label='pareto front', s=20)
    plt.title("multiobjective optimization")
    plt.xlabel("Y1")
    plt.ylabel("Y2")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig("plots/pareto_graph_real.png")
    plt.close()

if __name__ == "__main__":

    # exe optimization
    print("-"*20)
    print("Exe optimization")
    study = exe_opt()
    print("-"*20)

    # analyze
    print("Exe analysis")
    analyze(study)
    print("-"*20)