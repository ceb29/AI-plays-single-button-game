import configparser #"" : "",
config = configparser.ConfigParser()
config["NEAT"] = {"fitness_criterion": "max", #min, max, mean
                  "fitness_threshold": "100.0",  #float
                  "no_fitness_termination": "False", #True, False (defaults to False)
                  "pop_size" : "50",  #number per generation
                  "reset_on_extinction" : "False"} #True, False

config["DefaultStagnation"] = {"species_fitness_func" : "max", #min, max, mean, median (defaults to mean)
                               "max_stagnation" : "15", #number of generations without improvement (defaults to 15)
                               "species_elitism" : "2"} #number of species protected from stagnation (defaults to 0)

config["DefaultReproduction"] = {"elitism" : "2", #number of species preserved for next generation
                                 "survival_threshold" : "0.2", #number of species allowed to reproduce for the next generation (defaults to 0.2)
                                 "min_species_size" : "2"} #minumum per species (defaults to 2)


config["DefaultGenome"] = {"activation_default" : "sigmoid", #(defaults to random)
                           "activation_mutate_rate" : "0.0", #probability of change to different activation function [0.0, to 1.0]
                           "activation_options" : "sigmoid", #space seperated list of activation functions (defaults to sigmoid) 
                           "aggregation_default" : "sum", #aggregation function(defaults to random)
                           "aggregation_mutate_rate" : "0.0",#probability of change
                           "aggregation_options" : "sum", #space seperated list of sum, product, min, max, mean, median, maxabs(defaults to sum)
                           "bias_init_mean" : "0.0", #mean of ditribution
                           "bias_init_stdev" : "1.0", #standard deviation of ditribution
                           "bias_init_type" : "gaussian", #gaussian, normal, uniform (defaults gaussian)
                           "bias_max_value" : "30.0", 
                           "bias_min_value" : "-30.0",
                           "bias_mutate_power" : "0.4", #standard deviation of zero centered distribution
                           "bias_mutate_rate" : "0.8", #probability of bias changing by adding random number
                           "bias_replace_rate" : "0.02", #probability of replacing bias with random number
                           "compatibility_disjoint_coefficient" : "1.0",
                           "compatibility_weight_coefficient" : "0.5",
                           "conn_add_prob" : "0.1", #values [0.0, 1.0]
                           "conn_delete_prob" : "0.1", #values [0.0, 1.0]
                           "enabled_default" : "True", #True or False
                           "enabled_mutate_rate" : "0.01", #values [0.0, 1.0]
                           "enabled_rate_to_false_add" : "0.0", 
                           "enabled_rate_to_true_add" : "0.0",
                           "feed_forward" : "True", #True or False
                           "initial_connection" : "partial 0.5", #unconnected, fs_neat_nohidden, fs_neat_hidden, full_nodirect, full_direct, partial_nodirect # [0.0, 1.0], partial_direct # [0.0, 1.0] (defaults to unconnected)
                           "node_add_prob" : "0.2", #values [0.0, 1.0]
                           "node_delete_prob" : "0.2", #values [0.0, 1.0]
                           "num_hidden" : "0",
                           "num_inputs" : "6",
                           "num_outputs" : "1",
                           "response_init_mean" : "1.0", 
                           "response_init_stdev" : "0.0", 
                           "response_init_type" : "gaussian", #gaussian, normal, uniform (defaults gaussian)
                           "response_max_value" : "30.0",
                           "response_min_value" : "-30.0",
                           "response_mutate_power" : "0.01",
                           "response_mutate_rate" : "0.1",
                           "response_replace_rate" : "0.01",
                           "single_structural_mutation" : "False", #True, False (defaults to False)
                           "structural_mutation_surer" : "default", #True, False (defaults to default)
                           "weight_init_mean" : "0.0",
                           "weight_init_stdev" : "1.0",
                           "weight_init_type" : "gaussian", #gaussian, normal, uniform (defaults gaussian)
                           "weight_max_value" : "30.0",
                           "weight_min_value" : "-30.0",
                           "weight_mutate_power" : "0.5",
                           "weight_mutate_rate" : "0.8",
                           "weight_replace_rate" : "0.01"}

config["DefaultSpecieSet"] = {"compatibility_threshold" : "3.0"}

with open('example.ini', 'w') as configfile:
    config.write(configfile)