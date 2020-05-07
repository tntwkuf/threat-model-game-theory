import numpy as np
import copy
def liner(n):                                      #функция вывода линий для таблицы
    number=(32+18*(n-1))
    print()
    for i in range(number):
        print('-',end='')
    print()
def header_table(number):                         #функция вывода шапки для таблицы
    print ('{0:16}|  {1:13} |'.format('Защитник', 'Нарушитель 1'),end='')
    for s in range(2,number+1):
            print('  {0:14} |'.format('Нарушитель %d',)%s,end='')
def calculate_length(path,matrix):     #вычисление длины пути нарушителя
    length=1                               
    n=len(path)                       
    for i in range(n-1):
        length=length*matrix[path[i]][path[i+1]]
    return length
def get_best_path(paths,matrix):    #поиск наилучшего пути нарушителя
    curr_length=0
    best_length=0
    best_path=[]
    for path in paths:
        path=list(path)
        curr_length=calculate_length(path,matrix)
        if (curr_length>best_length):
            best_length=curr_length
            best_path=copy.copy(path)
    return best_length,best_path
def search_all_paths(graph,start,path=[]):  #поиск всех доступных путей в графе
    finish=len(graph)-1                     #определение конечной точки графа
    fill=0                                  #флаг, является ли точка тупиковой
    if not path:                            #если путь пустой, начинаем с стартовой точки
        path.append(0)
    if (start==finish):                     #если достигли конечной точки, выводим пройденный путь
        allpaths.append(tuple(path))
        path.pop()                          #и возвращаемся на шаг назад
    for i in range(len(graph)):             #проходя всю строку матрицы графа
        if ((graph[start][i]>0) and (graph[i][i]!=1)):             #если есть ребро
            fill=1                          #меняем флаг, добавляем точку к пути
            path.append(i)
            search_all_paths(graph,i,path)  #запускаем функцию рекурсивно из точки
        else:
            fill=0                          #если из точки больше путей нет, меняем флаг
    if fill==0:
        start=path.pop()                    # и возвращаемся на шаг назад
    return allpaths
def nullifier(x,intr,matrix):        #обнуляет заданную строку и столбец
    for i in range(len(matrix)):
        if i not in intr:
            for j in range(len(matrix)):
                if j not in intr:
                    matrix[i][j]=0
    for i in range(len(x)):
        k=x[i]
        if (k>=len(matrix)):
            break
        else:
            for j in range(len(matrix)):
                matrix[k][j]=0
                matrix[j][k]=0
            matrix[k][k]=1
    
def take_paths(matrix):     #возвращает поиск наилучшего пути из всех
    allpaths=[]
    allpaths=search_all_paths(matrix,0)
    best_length,best_path=get_best_path(allpaths,matrix)
    allpaths.clear()
    return best_length,best_path
def get_sum(def_strat,vuln_cost):    #подсчет стоимости реализации стратегии защитника
    sum=0
    for i in def_strat:
        sum=sum+vuln_cost[i-1]
    return sum
    
def game_func(matrix,inf_cost,vuln_cost,intruder_type):
    intruder=len(intruder_type)
    n=len(matrix)-2
    header_table(intruder)                                          #шапка таблицы
    liner(intruder)          
    vuln_list=[i+1 for i in range(n)]   #перечень уязвимостей
    def_strat=[]*n
    mmax=0
    mmin=10*inf_cost
    d_path=[]
    i_path=[]
    d_strat=[]
    i_strat=[]
    min_strat=[]
    max_strat=[]
    d_t=0
    i_t=0
    max_t=0
    min_t=0
    for i in range(2**n):
        maxi=0
        mini=10*inf_cost
        def_strat.clear()
        curr_matrix=matrix.copy()
        for j in range (n):
            if (i&(1<<j)):
                def_strat.append(vuln_list[j])
        proxy_sum=get_sum(def_strat,vuln_cost)
        print ('%s' % (str(def_strat).ljust(15)),end=' ')
        print('|', end='')
        for t in range(intruder):
            mark=0
            intr_matrix=curr_matrix.copy()
            nullifier(def_strat, intruder_type[t],intr_matrix)
            curr_length,curr_path=take_paths(intr_matrix)
            mark=proxy_sum+curr_length*inf_cost
            print('%15.2f |' % (mark),end='')
            if mark>maxi:
                maxi=mark
                d_strat=def_strat
                d_t=t+1
            if mark<mini:
                mini=mark
                i_strat=def_strat
                i_t=t+1
        if maxi<mmin:
            mmin=maxi
            max_strat=d_strat.copy()
            max_t=d_t
        if mini>mmax:
            mmax=mini
            min_strat=i_strat.copy()
            min_t=i_t
        print()
    liner(intruder)          
    print("Нижняя цена игры:",mmin)
    print("Верхяя цена игры:",mmax)
    print("Оптимальная стратегия защитника: ликвидация уязвимостей",str(max_strat),".\nПри этом потенциальные потери:",str(mmin),"\nТип нарушителя:",max_t)
    print("Оптимальная стратегия нарушителя: ликвидация уязвимостей",str(min_strat),".\nПри этом потенциальные потери:",str(mmax),"\nТип нарушителя:",min_t)

inf_cost=20000
vuln_cost=[4500,3500,5500,1000,3500]
intruder_type=[[1,4],[2,4],[1,2,3,4,5]]
matrix=np.array([[0,0.31,0.17,0.52,0,0,0],
        [0,0,0,0,0.19,0,0],
        [0,0,0,0,0.81,0,0],
        [0,0,0,0,0,1,0],
        [0,0,0,0,0,0,1],
        [0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0]])



allpaths=[]      
game_func(matrix,inf_cost,vuln_cost,intruder_type)
