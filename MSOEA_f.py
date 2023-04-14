import os, sys
sys.path.append("./")
import time
from tqdm import trange

from Parameter import Parameter
import Initialization as I
import convergence as cvg
import knee_trans_ar as kta
import Delete_Ar as da
import Off_generation as og
import environmental_sel as es
import record as r


'''MSOEA_f: knee-transferrable-pcos'''

'''
initial the population and ideal point update (in Initialization.py import as I)
calculate the convergence (in convergence.py import as cvg)

Solution Selection:
1. get knee solutions and thresholds
2. get the transfer solution and update the archive (in knee_trans_ar.py import as kta)

Solution Utilization:
3. crossover and mutation for offspring (in Off_generation.py import as og)
4. environmental selection (in environmental_sel.py import as es)
'''

'''main()'''
def main(test_function, test_number, path):

    param = Parameter(test_function)
    x_num = param.x_num
    x_min = param.MIN_BOUND
    x_max = param.MAX_BOUND   
    f_num = param.f_num
    scenario = param.scenarios
    keep_cnt = param.keep_cnt

    "parameter settings"
    max_gen = 3000
    N = 100
    NK = 5

    #SBX: pc, eta_c
    #PM: pm, eta_m
    cm_param = {
        "pc": 0.9,
        "eta_c": 1,
        "pm": 1 / x_num,
        "eta_m": 5,
        "x_num": x_num
    }

    #store function
    P = {}
    Ar = []
    ideal = {}
    nadir = {}
    min_idx = {}
    max_idx = {}
    ar_each = []

    Arp = {}

    start = time.time()

    Knee = {}
    for s in scenario:
        p = I.initial(s, N, x_min, x_max, param, test_function)
        min_idx[s], max_idx[s], ideal[s], nadir[s] = I.ideal_point(p, s, f_num[s])
        cvg.cal_con(p, s, ideal[s], nadir[s], f_num[s])
        P[s] = p

        Knee[s] = kta.get_Knee(p, s, NK)
    
    clock = start
    iterator = trange(max_gen)
    for gen in iterator:
        Trans = {}
        O = {}

        '''1. calculate the threshold'''
        k_s = []
        for s1 in scenario:
            k_s.extend(Knee[s1])


        for s1 in scenario:
            ideal[s1], min_idx[s1] = I.update(k_s + Ar, s1, ideal[s1], min_idx[s1], f_num[s1])
            cvg.cal_con(k_s, s1, ideal[s1], nadir[s1], f_num[s1])
            cvg.cal_con(Ar, s1, ideal[s1], nadir[s1], f_num[s1])

        '''calculate the worst of each population
        (after ideal point update, cause no influence to the worst performance)
        selet knees to be added to other scenarios'''
        for s1 in scenario:
            # get extreme point
            extreme = kta.get_ex(Knee[s1], s1)
            l_min, l_max, o_min, o_max = kta.get_param(k_s, Knee[s1], s1)
            Trans[s1] = kta.get_trans(k_s, Ar, s1, l_min, l_max, o_min, o_max, extreme, ideal[s1], test_function, test_number)

        new_pcos = []        
        for k in k_s: 
            if k.nr == len(scenario):
                new_pcos.append(k)
        
        if new_pcos:
            for s1 in scenario:
                extreme = kta.get_ex(Knee[s1], s1)
                l_min, l_max, o_min, o_max = kta.get_param(k_s, Knee[s1], s1)
                Ar = kta.update_pcos_ar(Ar, s1, l_min, l_max, o_min, extreme, ideal[s1], test_number)
                
            Ar.extend(new_pcos)
            ar_each.append(len(new_pcos))
            '''N 为超参'''
            if len(Ar) > N:
                Ar = da.del_update(Ar, N, scenario)
 
        '''3. crossover and mutation
           4. do environmental selection'''
        for s1 in scenario:
            p1 = P[s1]
            trans1 = Trans[s1]
            off1, sga = og.get_off(p1, trans1 + Ar, s1, Arp, N, test_function, cm_param, param)
            O[s1] = off1

            temp1 = p1 + off1
            min_idx[s1], max_idx[s1], ideal[s1], nadir[s1] = I.ideal_point(temp1, s1, f_num[s1])
            cvg.cal_con(temp1, s1, ideal[s1], nadir[s1], f_num[s1])

            next1, keep = es.env_select(temp1, s1, N)


            P[s1] = next1
            if not keep:
                keep = 1
            keep_cnt[s1].append(keep)

            arp = keep / sga if sga else 1
            Arp[s1] = arp

            Knee[s1] = kta.get_Knee(next1, s1, NK)

            
        

        if gen % 10 == 0:
            remain = []
            probability = []
            for s in scenario:
                remain.append(keep_cnt[s][-1])
                probability.append(format(Arp[s], '.2f'))
            desc = 'gen:{}, size of Ar: {}, survive: {}, arp: {}, time: {:.2f}'.format(gen, len(Ar), remain, probability, time.time() - clock)
            iterator.set_description(desc)
            clock = time.time()

    pcos = Ar
    if len(pcos) > NK:
        for s in scenario:
            min_idx[s], max_idx[s], ideal[s], nadir[s] = I.ideal_point(pcos, s, f_num[s])
            cvg.cal_con(pcos, s, ideal[s], nadir[s], f_num[s])


    r.write_xlsx(pcos, scenario, test_function, path, name = "_test_{}".format(test_number))


def exe_main(test_list, read_list, test_number, path):
    bigstart = time.time()


    for i in range(len(test_list)):
        test_function = test_list[i]
        read = read_list[i]
        print(test_function + " the {} iteration".format(test_number))
        main(test_function, test_number, path)

    print("the total time is: " + str(time.time() - bigstart))