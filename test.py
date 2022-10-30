
import pickle
import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, precision_score,
                             confusion_matrix, classification_report,roc_auc_score)

from res.values import constan
from res.values import path as dir
from res.values.constan import screen as scr
from src import dataset as dst

WIDTH, HEIGHT = 1100, 600

def abc(root):
    newWindow = tk.Toplevel(root, bg='white')
    newWindow.title("New Window")
    newWindow.geometry(f'{WIDTH}x{HEIGHT}')
    newWindow.resizable(False, False)
    #newWindow.eval('tk::PlaceWindow . center')

    content(newWindow)

def content(newWindow):
    labels = [f'{x} Tahun' for x in dst.classLabel()]
    
    with open(f'{dir.PICKLE_FOLDER}{constan.YTRUE_YPRED}.pickle','rb') as f:
            y_trues, y_preds = pickle.load(f)    
    
    result = confusion_matrix(y_trues, y_preds)

    result = pd.DataFrame(result, index = labels,columns = labels)
    figure = Figure(figsize=(6, 6))
    

    ax = figure.subplots() 
    heatmap = sns.heatmap(result, annot=True ,square=True, cbar=False, ax=ax, fmt=".0f", linewidth=.5)
    # heatmap.set_title('Confusion Matrix', fontdict={'fontsize':12}, pad=16)
   
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Actual Values   ')
    ax.tick_params(length=0, labeltop=True, labelbottom=False)
    ax.xaxis.set_label_position('top')
    
    FrameA = tk.Frame(newWindow, width= scr.width_70p, height= HEIGHT, bg='white')
    FrameA.grid(row=0, column=0, sticky='nsew')
    FrameA.grid_propagate(False)
    canvas = FigureCanvasTkAgg(figure, FrameA)             
    canvas.get_tk_widget().pack() 

    FrameB = tk.Frame(newWindow, width= scr.width_70p, height= HEIGHT, bg='white')
    FrameB.grid(row=0, column=1, sticky='nsew',pady=(20,1))
    FrameB.grid_propagate(False)
    cnf_matrix = confusion_matrix(np.array(y_trues), np.array(y_preds))
    FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix)  
    FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
    TP = np.diag(cnf_matrix)
    TN = cnf_matrix.sum() - (FP + FN + TP)

    FP = FP.astype(float)
    FN = FN.astype(float)
    TP = TP.astype(float)
    TN = TN.astype(float)
    # Sensitivity, hit rate, recall, or true positive rate
    TPR = TP/(TP+FN)
    # Specificity or true negative rate
    TNR = TN/(TN+FP) 
    # Precision or positive predictive value
    PPV = TP/(TP+FP)
    # Negative predictive value
    NPV = TN/(TN+FN)
    # Fall out or false positive rate
    FPR = FP/(FP+TN)
    # False negative rate
    FNR = FN/(TP+FN)
    # False discovery rate
    FDR = FP/(TP+FP)
    # Overall accuracy
    ACC = (np.sum(TP))/(TP+FP+FN+TN)
    print(ACC)
    
    a = accuracy_score(y_trues, y_preds)
    b = precision_score(y_trues, y_preds, average='micro')
    c = precision_score(y_trues, y_preds, average='macro')
    d = precision_score(y_trues, y_preds, average='weighted')
    e = classification_report(y_trues, y_preds, target_names=labels)
    print(e)
    lbl_accuracy = Label(FrameB, text=f'Acuraccy : {a}', bg='white')
    lbl_accuracy.grid(row=0, column=0, sticky=W, padx=1,pady=(20,1))

    lbl_time_execution= Label(FrameB, text=f'Micro Precision :{b}', bg='white')
    lbl_time_execution.grid(row=1, column=0, sticky=W, padx=1,pady=1)
    lbl_time_executions= Label(FrameB, text=f'Macro Precision :{c}', bg='white')
    lbl_time_executions.grid(row=2, column=0, sticky=W, padx=1,pady=1)
    lbl_time_executiond= Label(FrameB, text=f'Weighted Precision :{d}', bg='white')
    lbl_time_executiond.grid(row=3, column=0, sticky=W, padx=1,pady=1)

    lbl_deviation = Label(FrameB, text=f'ROC_AUC ', bg='white')
    lbl_deviation.grid(row=4, column=0, sticky=W, padx=1,pady=1)
    lbl_deviations = Label(FrameB, text=f'{e}', bg='white')
    lbl_deviations.grid(row=5, column=0, sticky=W, padx=1,pady=1)

    print(result)

def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)): 
        if y_actual[i]==y_hat[i]==1:
           TP += 1
        if y_hat[i]==1 and y_actual[i]!=y_hat[i]:
           FP += 1
        if y_actual[i]==y_hat[i]==0:
           TN += 1
        if y_hat[i]==0 and y_actual[i]!=y_hat[i]:
           FN += 1

    return(TP, FP, TN, FN)