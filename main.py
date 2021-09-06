#single button game
#press space to boost up
#avoid the walls
import pygame
import os
import pickle
import neat
import sprite_classes
from game_classes import Game
from pygame.constants import K_RETURN, K_ESCAPE, KEYDOWN #buttons used in game
from constants import *

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a game window with given size 

#start the main game
def start_game(game):
    running = True
    game.start() 
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE:
                    game.write_high_score() #save the current high score
                    running = False
                if event.key == K_RETURN: #restart game if enter is pressed
                    game.restart()
            elif event.type == pygame.QUIT: #exit game if windows closed
                game.write_high_score() #save the current high score
                running = False
        game.update() #keep updating the main game
        if len(game.players) == 0:
            running = False

#evaluate genomes using the game
def eval_genomes(genomes, config):
    game = Game(60, COLOR_WHITE, win, WIDTH, HEIGHT)  
    for genome_id, genome in genomes:
        game.players.append(sprite_classes.Player(WIDTH, HEIGHT, (WIDTH/4, HEIGHT/2)))
        game.nets.append(neat.nn.RecurrentNetwork.create(genome, config))
        #game.nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        game.genomes.append(genome)
        genome.fitness = 0.0
    start_game(game)
    game.write_high_score() #save the current high score

#evaluate the best genomes from the last run
def eval_best(config):
    prev_nets = [pickle.load(open( "gen0.pickle", "rb" )), pickle.load(open( "gen1.pickle", "rb" )), pickle.load(open( "gen2.pickle", "rb" ))]
    game = Game(60, COLOR_WHITE, win, WIDTH, HEIGHT)
    for gen in prev_nets:
        gen.fitness = 0.0
        game.players.append(sprite_classes.Player(WIDTH, HEIGHT, (WIDTH/4, HEIGHT/2)))
        game.nets.append(neat.nn.RecurrentNetwork.create(gen, config))
        #game.nets.append(neat.nn.FeedForwardNetwork.create(gen, config))
        game.genomes.append(gen)
    start_game(game)
    game.write_high_score() #save the current high score

#evaluate a population of genomes for 100 generations and then save the best 3
def run(config):
    population = neat.Population(config)
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)
    population.add_reporter(neat.StdOutReporter(True))
    winner = population.run(eval_genomes, 100)
    print(winner)
    best_gen = statistics.best_unique_genomes(3)
    for i in range(len(best_gen)):
        with open("gen" + str(i) + ".pickle", 'wb') as f:
            pickle.dump(best_gen[i], f)

#evaluate the best genomes form last run 10 times
def run_best(config):
    for i in range(10):
        eval_best(config)
    
def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.ini')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run(config)
    #run_best(config) #uncomment to run the best nets from the last run
    pygame.quit()

if __name__ == "__main__":
    main()