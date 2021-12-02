from math import floor, log
# Digits for k: 3
# Digits for m: 6
# Digits for b: 9
# Digits for t: 12
# Digits for q: 15
# Digits for Q: 18
# Digits for s: 21
def human_format(number):
    units = ['', 'k', 'm', 'b', 'T', 'q', 'Q', 's', 'S', 'o', 'N']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.3f%s' % (number / k**magnitude, units[magnitude])

def calculateEB(soulEggs: str, prophecyEggs: int, prophecyBonus: int = 5, soulFood: int = 140):
    if soulEggs.endswith("k"):
        soulEggs = float(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000    
    elif soulEggs.endswith("m"):
        soulEggs = float(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000
    elif soulEggs.endswith("b"):
        soulEggs = float(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000
    elif soulEggs.endswith('t'):
        soulEggs = float(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000
    elif soulEggs.endswith('q'):
        soulEggs = float(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000
    elif soulEggs.endswith('Q'):
        soulEggs = float(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000000
    elif soulEggs.endswith('s'):
        soulEggs = float(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000000000
    else:
        soulEggs = float(soulEggs)
    try:
        prophecyEggBonus = (1 + 0.05 + (0.01 * prophecyBonus))**prophecyEggs * (10 + soulFood)
        EB = prophecyEggBonus * soulEggs
        EB = human_format(EB)
        return EB
    except:
        return False

EB = calculateEB("100", 0, 0, 0)
print(EB)