# TODO: Cleanup


# TOILET_MIN = 8 # Minimum number on toilet card, inclusive
# TOILET_MAX = 15 # Maximum number on toilet card, exclusive
# TOILET_REPEATS = 1 # Number of toilet cards per capacity



# SOME RANDOM TRASH


    # def prompt_console(self, state):
        # def parse(s):
            # g = re.search(r'^[0-9]+$', s)
            # if g:
                # return int(g.group(0))
            # g = re.search(r'^[rgbRGB][0-4sS]$', s)
            # if g:
                # m = g.group(0)
                # if m[0] == 'r' or m[0] == 'R':
                    # c = 0
                # elif m[0] == 'g' or m[0] == 'G':
                    # c = 1
                # else:
                    # c = 2
                # 
                # if m[1] == 's' or m[1] == 'S':
                    # rel = Card.POOP_MAX - Card.POOP_MIN
                # else:
                    # rel = int(m[1])
                # return c * Card.NUM_CARD_TYPES + rel
# 
            # return None
# 
        # card_idx = None
        # while card_idx == None:
            # print('Your Cards: {}'.format(self.deck))
            # card_idx = input('{}, choose a Card Index: '.format(self.name)).strip()
            # card_idx = parse(card_idx)
# 
            # if card_idx == None:
                # continue
# 
            # if card_idx < 0 or card_idx >= Card.TOTAL_CARDS:
                # card_idx = None
                # continue
# 
            # if self.deck.cardcount[card_idx] <= 0:
                # card_idx = None
                # continue
        # return card_idx


    # def prompt_turn(self, state):
        # card_idx = self.prompt(state)
        # for c in self.deck.cardlist:
            # if c.index() == card_idx:
                # card = c
                # break
# 
        # return card
