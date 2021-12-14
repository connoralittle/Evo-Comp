def mu_plus_lambda_w_dynamic_pop(current_pop, current_fitness, offspring, offspring_fitness, mu, ka_prev, ks_prev):#gen_max, gen, ini_max_fitness):
    #combine current and new populations into a single sorted list
    current = list(zip(current_fitness, current_pop, [0] * len(current_pop)))
    new = list(zip(offspring_fitness, offspring, [1] * len(offspring)))
    updated = sorted(current + new)

    #take the current_pop best individuals from the overall list
    population = [x[1] for x in updated][:mu]
    fitness = [x[0] for x in updated][:mu]

    #profiga
    #I explored another control mechanism here

    # increase_factor = 1 
    # eval_num_factor = gen_max - gen
    # fitness_factor = abs(min(fitness) - min(current_fitness)) / min(current_fitness)

    # scaling = increase_factor * eval_num_factor * fitness_factor

    # mu = mu + mu * scaling

    # if max(fitness) == max(current_fitness) or scaling < 0.05:
    #     scaling = 0.95
    #     mu = mu * scaling

    #ka is non synonymous changes
    ka = sum(el not in current_fitness for el in fitness)
    #ks is synonymous
    ks = sum(el in current_fitness for el in fitness)

    #try to find the ratio
    try:
        div = ka/ks
    #this is if ks is 0
    except:
        div = mu

    #record the previous attempts
    try:
        div_prev = ka_prev / ks_prev
    except:
        div_prev = mu

    #if teh ratio is too large or too small adjust the population
    if div > 0.5:
        mu = int(mu*(1+abs(div - div_prev)))
    elif div < 0.5:
        mu = int(mu*(1 + div - div_prev))

    #hard cap mu so that it can't shrink to 0 or grow too large
    mu = max(50, min(1000, mu))
    return population, mu, ka, ks

#mu, kaprev and ksprev only get passed so that i dont have to make 2 different calls. they do nothing
def mu_plus_lambda(current_pop, current_fitness, offspring, offspring_fitness, mu, ka_prev, ks_prev):
    #combine current and new populations into a single sorted list
    current = list(zip(current_fitness, current_pop))
    new = list(zip(offspring_fitness, offspring))
    updated = sorted(current + new)

    #take the current_pop best individuals from the overall list
    population = [x[1] for x in updated][:len(current_pop)]
    fitness = [x[0] for x in updated][:len(current_pop)]
    
    
    return population, mu, 1, 1

def replacement_w_dynamic_pop(current_pop, current_fitness, offspring, offspring_fitness, mu, ka_prev, ks_prev):
    lam = int(mu / 2)
    #combine current and new populations into 2 sorted lists
    current = sorted(list(zip(current_fitness, current_pop)))
    new = sorted(list(zip(offspring_fitness, offspring)))

    #take the best lam from the parents and replace the worst lam with the best n from the offspring
    updated = current[:len(current_pop) - lam] + new[:lam]

    population = [x[1] for x in updated][:mu]
    fitness = [x[0] for x in updated][:mu]

    #perform the same population control as above
    ka = sum(el not in current_fitness for el in fitness)
    ks = sum(el in current_fitness for el in fitness)

    try:
        div = ka/ks
    except:
        div = mu

    try:
        div_prev = ka_prev / ks_prev
    except:
        div_prev = mu

    if div > 1:
        mu = int(mu*(1+abs(div - div_prev)))
    elif div < 1:
        mu = int(mu*(1 + div - div_prev))

    mu = max(50, min(1000, mu))
    return population, mu, ka, ks

