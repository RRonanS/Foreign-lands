# Este arquivo é responsável pelo gerenciamento do carregamento e armazenamento das imagens das sprites
import pygame
from codigos.variaveis import char_size
from codigos.outros.auxiliares import img_load

diretorio_base = 'arquivos/imagens/monstros/'
sprite_size = 150, 150
imagens = {'monstros': {}, 'npcs': {}, 'bosses': {}, 'personagem': {}, 'projetis': {}}

#  Imagens de monstros

# Imagens do Esqueleto
diretorio = diretorio_base+'Skeleton/'
size = char_size[0], char_size[1]
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Walk.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True)}
imagens['monstros']['esqueleto'] = atualimages

# Imagens do Olho
diretorio = diretorio_base+'Flying eye/'
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Flight.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(walk, sprite_size, char_size, True),
               'attack': img_load(attack, sprite_size, char_size, True),
               'walk': img_load(walk, sprite_size, char_size, True),
               'death': img_load(dead, sprite_size, char_size, True)}
imagens['monstros']['olho'] = atualimages

# Imagens do Goblin
diretorio = diretorio_base+'Goblin/'
size = char_size[0] * 1.5, char_size[1] * 1.5
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Run.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True)}
imagens['monstros']['goblin'] = atualimages

#  Imagens do cogumelo
diretorio = diretorio_base+'Mushroom/'
size = char_size[0] * 1.5, char_size[1] * 1.5
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Run.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True)}
imagens['monstros']['cogumelo'] = atualimages

#  Imagens do Bringer of death
sprite_size = 140, 93
diretorio = diretorio_base+'bringerofdeath/'
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Run.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
cast = pygame.image.load(diretorio + 'Cast.png').convert_alpha()
spell = pygame.image.load(diretorio + 'Spell.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, char_size, False),
               'attack': img_load(attack, sprite_size, char_size, False),
               'walk': img_load(walk, sprite_size, char_size, False),
               'death': img_load(dead, sprite_size, char_size, False),
               'cast': img_load(cast, sprite_size, char_size, False),
               'spell': img_load(spell, sprite_size, char_size, False)}
imagens['monstros']['bringerdeath'] = atualimages

# Imagens do executor(Summon do Executioner)
sprite_size = 50, 50
diretorio = diretorio_base+'Executioner/Executor/'
size = char_size[0]*0.8, char_size[1]*0.8
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
appear = pygame.image.load(diretorio + 'Appear.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True),
               'appear': img_load(appear, sprite_size, size, True)}
imagens['monstros']['executor'] = atualimages
sprite_size = 150, 150

# Imagens de Bosses

# Imagens do Boss1 (Esqueleto gigante)
diretorio = diretorio_base+'Skeleton/'
size = char_size[0]*2, char_size[1]*2
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Walk.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True)}
imagens['bosses']['boss1'] = atualimages

# Imagens do Boss2 Executioner
diretorio = diretorio_base+'Executioner/'
size = char_size[0]*2, char_size[1]*2
sprite_size = 100, 100
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
summoning = pygame.image.load(diretorio + 'Summon.png').convert_alpha()
skill = pygame.image.load(diretorio + 'Skill.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True),
               'summon': img_load(summoning, sprite_size, size, True),
               'skill': img_load(skill, sprite_size, size, True)}
imagens['bosses']['executioner'] = atualimages


# Imagens do personagem
diretorio = 'arquivos/imagens/Knight/'
atualimages = {'idle': [], 'run': [], 'attack': [], 'jump': [],
               'jump_fall': []}
idle = pygame.image.load(diretorio + '_Idle.png').convert_alpha()
run = pygame.image.load(diretorio + '_Run.png').convert_alpha()
attack = pygame.image.load(diretorio + '_Attack.png').convert_alpha()
jump = pygame.image.load(diretorio + '_Jump.png').convert_alpha()
jump_fall = pygame.image.load(diretorio + '_JumpFallInbetween.png').convert_alpha()
death = pygame.image.load(diretorio + '_Death.png').convert_alpha()
foot = pygame.image.load(diretorio + '-foot.png').convert_alpha()
atualimages['idle'] = img_load(idle, (120, 80), char_size)
atualimages['run'] = img_load(run, (120, 80), char_size)
atualimages['attack'] = img_load(attack, (120, 80), char_size)
atualimages['jump'] = img_load(jump, (120, 80), char_size)
atualimages['jump_fall'] = img_load(jump_fall, (120, 80), char_size)
atualimages['death'] = img_load(death, (120, 80), char_size)
atualimages['foot'] = img_load(foot, (120, 80), char_size)
imagens['personagem'] = atualimages

# Imagens do Golem
diretorio = diretorio_base+'Golem/'
size = char_size[0]*1, char_size[1]*1
sprite_size = 100, 100
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
projetil = pygame.image.load(diretorio + 'Projetil.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True),
               'projetil': img_load(projetil, sprite_size, size, True)
               }
imagens['monstros']['golem'] = atualimages
imagens['projetis']['golem'] = atualimages['projetil']

# Imagens do Lobo
diretorio = diretorio_base+'Wolf/'
size = char_size[0]*0.5, char_size[1]*0.5
sprite_size = 64, 64
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Walk.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'walk': img_load(attack, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True),
               }
imagens['monstros']['lobo'] = atualimages

# Imagens do Boss3 Demon
diretorio = diretorio_base+'Demon/'
size = char_size[0]*2.5, char_size[1]*2.5
sprite_size = 864, 480
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
attack = pygame.image.load(diretorio + 'Attack.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Walk.png').convert_alpha()
dead = pygame.image.load(diretorio + 'Death.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'attack': img_load(attack, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'death': img_load(dead, sprite_size, size, True)
               }
imagens['bosses']['demon'] = atualimages

# Imagens do mercador
diretorio = diretorio_base.replace('monstros/', 'mercador/')
size = char_size[0]*0.6, char_size[1]*0.6
sprite_size = 94, 91
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
talk = pygame.image.load(diretorio + 'Talk.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'talk': img_load(talk, sprite_size, size, True)
               }
imagens['npcs']['Mercador'] = atualimages

# Imagens do mago
diretorio = diretorio_base.replace('monstros/', 'mago/')
size = char_size[0]*0.6, char_size[1]*0.6
sprite_size = 48, 48
idle = pygame.image.load(diretorio + 'Idle.png').convert_alpha()
walk = pygame.image.load(diretorio + 'Walk.png').convert_alpha()
especial = pygame.image.load(diretorio + 'Special.png').convert_alpha()
atualimages = {'idle': img_load(idle, sprite_size, size, True),
               'walk': img_load(walk, sprite_size, size, True),
               'special': img_load(especial, sprite_size, size, True)
               }
imagens['npcs']['Mago'] = atualimages

# Imagens de spawner
diretorio = diretorio_base + 'Spawner/'
size = char_size[0]*1, char_size[1]*1
sprite_size = 64, 64
altar = pygame.image.load(diretorio + 'altar.png').convert_alpha()
death = pygame.image.load(diretorio + 'altar_death.png').convert_alpha()
atualimages = {'idle': img_load(altar, sprite_size, size, True),
               'walk': img_load(altar, sprite_size, size, True),
               'attack': img_load(altar, sprite_size, size, True),
               'death': img_load(death, sprite_size, size, True)
               }

imagens['monstros']['spawner'] = atualimages
