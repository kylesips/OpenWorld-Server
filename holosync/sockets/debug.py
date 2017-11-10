"""
Debugging classes used to debug socket connections and implementation of features
during development.
"""

from random import randint


class SocketDebugger():
  def __init__(self):
    ## Insults pulled from related .h files pertaining to sudo in *nix environments.
    ## No attempt has been made to ensure these insults are politically correct.

    self.__debug_mode = False
    self.__insults = [
  "Just what do you think you're doing Dave?",
  "It can only be attributed to human error.",
  "That's something I cannot allow to happen.",
  "My mind is going. I can feel it.",
  "Sorry about this, I know it's a bit silly.",
  "Take a stress pill and think things over.",
  "This mission is too important for me to allow you to jeopardize it.",
  "I feel much better now.",
  "Wrong!  You cheating scum!",
  "And you call yourself a Rocket Scientist!",
  "No soap, honkie-lips.",
  "Where did you learn to type?",
  "Are you on drugs?",
  "My pet ferret can type better than you!",
  "You type like i drive.",
  "Do you think like you type?",
  "Your mind just hasn't been the same since the electro-shock, has it?",
  "Maybe if you used more than just two fingers...",
  "BOB says:  You seem to have forgotten your brain, enter another!",
  "stty: unknown mode: doofus",
  "I can't hear you -- I'm using the scrambler.",
  "The more you drive -- the dumber you get.",
  "Listen, burrito brains, I don't have time to listen to this trash.",
  "I've seen penguins that can type better than that.",
  "Have you considered trying to match wits with a rutabaga?",
  "You speak an infinite deal of nothing",
  "You silly, twisted boy you.",
  "He has fallen in the water!",
  "We'll all be murdered in our beds!",
  "You can't come in. Our tiger has got flu",
  "I don't wish to know that.",
  "What, what, what, what, what, what, what, what, what, what?",
  "You can't get the wood, you know.",
  "You'll starve!",
  "... and it used to be so popular...",
  "Pauses for audience applause, not a sausage",
  "Hold it up to the light --- not a brain in sight!",
  "Have a gorilla...",
  "There must be cure for it!",
  "There's a lot of it about, you know.",
  "You do that again and see what happens...",
  "Ying Tong Iddle I Po",
  "Harm can come to a young lad like that!",
  "And with that remarks folks, the case of the Crown vs yourself was proven.",
  "Speak English you fool --- there are no subtitles in this scene.",
  "You gotta go owwwww!",
  "I have been called worse.",
  "It's only your word against mine.",
  "I think ... err ... I think ... I think I'll go home",
]

  def get_random_insult(self):
    return self.__insults[randint(0, len(self.__insults) - 1)]

  def toggle_debug_mode(self):
    self.__debug_mode = not(self.__debug_mode)

  def get_debug_mode(self):
    return self.__debug_mode