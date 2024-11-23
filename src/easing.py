import math

def linear(t):
    return t

def easeInSine(t):
    return -math.cos(t * math.pi / 2) + 1

def easeOutSine(t):
    return math.sin(t * math.pi / 2)

def easeInOutSine(t):
    return -(math.cos(math.pi * t) - 1) / 2

def easeInQuad(t):
    return t * t

def easeOutQuad(t):
    return -t * (t - 2)

def easeInOutQuad(t):
    t *= 2
    if t < 1:
        return t * t / 2
    else:
        t -= 1
        return -(t * (t - 2) - 1) / 2

def easeInCubic(t):
    return t * t * t

def easeOutCubic(t):
    t -= 1
    return t * t * t + 1

def easeInOutCubic(t):
    t *= 2
    if t < 1:
        return t * t * t / 2
    else:
        t -= 2
        return (t * t * t + 2) / 2

def easeInQuart(t):
    return t * t * t * t

def easeOutQuart(t):
    t -= 1
    return -(t * t * t * t - 1)

def easeInOutQuart(t):
    t *= 2
    if t < 1:
        return t * t * t * t / 2
    else:
        t -= 2
        return -(t * t * t * t - 2) / 2

def easeInQuint(t):
    return t * t * t * t * t

def easeOutQuint(t):
    t -= 1
    return t * t * t * t * t + 1

def easeInOutQuint(t):
    t *= 2
    if t < 1:
        return t * t * t * t * t / 2
    else:
        t -= 2
        return (t * t * t * t * t + 2) / 2

def easeInExpo(t):
    return math.pow(2, 10 * (t - 1))

def easeOutExpo(t):
    return -math.pow(2, -10 * t) + 1

def easeInOutExpo(t):
    t *= 2
    if t < 1:
        return math.pow(2, 10 * (t - 1)) / 2
    else:
        t -= 1
        return -math.pow(2, -10 * t) - 1

def easeInCirc(t):
    return 1 - math.sqrt(1 - t * t)

def easeOutCirc(t):
    t -= 1
    return math.sqrt(1 - t * t)

def easeInOutCirc(t):
    t *= 2
    if t < 1:
        return -(math.sqrt(1 - t * t) - 1) / 2
    else:
        t -= 2
        return (math.sqrt(1 - t * t) + 1) / 2