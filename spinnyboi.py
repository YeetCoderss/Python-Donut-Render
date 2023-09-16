import pygame
import math

pygame.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

theta_spacing = 0.05
phi_spacing = 0.03
R1 = 1
R2 = 2
K2 = 5

output = [[' ' for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
zbuffer = [[-10000 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

def clear_screen():
	for i in range(SCREEN_HEIGHT):
		for j in range(SCREEN_WIDTH):
			output[i][j] = ' '
			zbuffer[i][j] = -10000

def render_frame(A, B):
	K1 = SCREEN_WIDTH/2
	clear_screen()
	cosA = math.cos(A)
	sinA = math.sin(A)
	cosB = math.cos(B)
	sinB = math.sin(B)

	for theta in range(0, int(2 * math.pi / theta_spacing)):
		for phi in range(0, int(2 * math.pi / phi_spacing)):
			cosphi = math.cos(phi * phi_spacing)
			sinphi = math.sin(phi * phi_spacing)
			circlex = R2 + R1 * math.cos(theta * theta_spacing)
			circley = R1 * math.sin(theta * theta_spacing)
			x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
			y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
			z = K2 + cosA * circlex * sinphi + circley * sinA
			ooz = 1 / z
			xp = int(SCREEN_WIDTH / 2 + K1 * x * ooz)
			yp = int(SCREEN_HEIGHT / 2 - K1 * y * ooz)

			if (0 <= xp < SCREEN_WIDTH) and (0 <= yp < SCREEN_HEIGHT):
				L = cosphi * math.cos(theta * theta_spacing) * sinB - cosA * math.cos(theta * theta_spacing) * sinphi - sinA * math.sin(theta * theta_spacing) + cosB * (cosA * math.sin(theta * theta_spacing) - math.cos(theta * theta_spacing) * sinA * sinphi)
				if L > 0 and ooz > zbuffer[yp][xp]:
					zbuffer[yp][xp] = ooz
					luminanceIndex = int(L*8)
					if luminanceIndex >= 8:
						luminanceIndex = 7
					output[yp][xp] = ".,-~:;=!*#$@"[luminanceIndex]


def main():
	A = 0
	B = 0
	clock = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
		render_frame(A, B)

		for i in range(SCREEN_HEIGHT):
			for j in range(SCREEN_WIDTH):
				if output[i][j] != ' ':
					char_index = ".,-~:;=!*#$@".index(output[i][j])
					luminance = char9_index / 7.0 * 255
					screen.set_at((j, i), (luminance, luminance, luminance))

		pygame.display.flip()
		screen.fill((0, 0, 0))
		A += 0.08
		B += 0.08

		clock.tick(60)


if __name__ == "__main__":
	main()