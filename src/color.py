from typing import Tuple

# Utility function to clamp the values between 0 and 255
def clamp(value: float) -> float:
    return max(0.0, min(255.0, value))

# Blends two colors using mix
def mix(color1: Tuple[float, float, float], color2: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (clamp((color1[0] + color2[0]) / 2),
            clamp((color1[1] + color2[1]) / 2),
            clamp((color1[2] + color2[2]) / 2))

# Blends two colors using multiply
def multiply(color1: Tuple[float, float, float], color2: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (clamp((color1[0] * color2[0]) / 255),
            clamp((color1[1] * color2[1]) / 255),
            clamp((color1[2] * color2[2]) / 255))

# Adds two colors
def add(color1: Tuple[float, float, float], color2: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (clamp(color1[0] + color2[0]),
            clamp(color1[1] + color2[1]),
            clamp(color1[2] + color2[2]))

# Subtracts color2 from color1
def sub(color1: Tuple[float, float, float], color2: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (clamp(color1[0] - color2[0]),
            clamp(color1[1] - color2[1]),
            clamp(color1[2] - color2[2]))

# Blends two colors using screen
def screen(color1: Tuple[float, float, float], color2: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (clamp(255 - (255 - color1[0]) * (255 - color2[0]) / 255),
            clamp(255 - (255 - color1[1]) * (255 - color2[1]) / 255),
            clamp(255 - (255 - color1[2]) * (255 - color2[2]) / 255))

# Linearly interpolates between two colors
def lerp(color1: Tuple[float, float, float], color2: Tuple[float, float, float], t: float) -> Tuple[float, float, float]:
    t = clamp(t)  # Ensure t is between 0 and 1
    return (clamp(color1[0] + t * (color2[0] - color1[0])),
            clamp(color1[1] + t * (color2[1] - color1[1])),
            clamp(color1[2] + t * (color2[2] - color1[2])))

# Example usage
if __name__ == "__main__":
    color_a = (128, 51, 179)
    color_b = (26, 230, 77)

    print("Mix:", mix(color_a, color_b))
    print("Multiply:", multiply(color_a, color_b))
    print("Add:", add(color_a, color_b))
    print("Sub:", sub(color_a, color_b))
    print("Screen:", screen(color_a, color_b))
    print("Lerp (t=0.25):", lerp(color_a, color_b, 0.25))
