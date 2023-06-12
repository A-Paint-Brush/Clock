import pygame
import math
import time
import Timer
import Hour_Hand
import Minute_Hand
import Second_Hand
import Alarm_Hand


class Main:
    def __init__(self):
        pygame.init()
        self.monitor_width = pygame.display.Info().current_w
        self.monitor_height = pygame.display.Info().current_h
        self.hour_hand = Hour_Hand.Hand()
        self.minute_hand = Minute_Hand.Hand()
        self.second_hand = Second_Hand.Hand()
        self.alarm_hand = Alarm_Hand.Hand()
        self.key_timer = Timer.Timer()
        self.snooze_timer = Timer.Timer()
        self.second = time.localtime().tm_sec
        self.font1 = pygame.font.SysFont("Times New Roman", 17)
        self.font2 = pygame.font.SysFont("Times New Roman", 12)
        self.week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.alarm_state = ["Alarm:Off", "Alarm:On"]
        self.full_screen = False
        self.alarm = False
        self.snoozing = False
        self.snooze_over = False
        self.beep = False
        self.update = False
        self.key_left = False
        self.first_press = True
        self.gameRun = True
        width = 480
        height = 360
        pygame.display.set_caption("Clock")
        self.screen = pygame.display.set_mode((480, 360), pygame.RESIZABLE)
        self.enter_fullscreen_icon = pygame.image.load("Images\\Enter Fullscreen Icon.png").convert_alpha()
        self.exit_fullscreen_icon = pygame.image.load("Images\\Exit Fullscreen Icon.png").convert_alpha()
        self.label = pygame.image.load("Images\\Label.png").convert_alpha()
        self.beeping = pygame.mixer.Sound("Sounds\\Alarm Clock Beeping.wav")
        self.clock = pygame.time.Clock()
        while self.gameRun:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameRun = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.display.Info().current_w - 28 < \
                            pygame.mouse.get_pos()[
                                0] < pygame.display.Info().current_w - 2 and pygame.display.Info().current_h - 28 < \
                            pygame.mouse.get_pos()[1] < pygame.display.Info().current_h - 2:
                        if not self.full_screen:
                            self.full_screen = True
                            self.screen = pygame.display.set_mode((self.monitor_width, self.monitor_height),
                                                                  pygame.FULLSCREEN)
                        else:
                            self.full_screen = False
                            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                elif event.type == pygame.VIDEORESIZE:
                    if not self.full_screen:
                        width = event.w
                        height = event.h
                        if width < 480:
                            width = 480
                        if height < 360:
                            height = 360
                        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.full_screen:
                            self.full_screen = False
                            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    elif event.key == pygame.K_SPACE:
                        if self.alarm:
                            self.alarm = False
                        else:
                            if self.snoozing:
                                self.beeping.stop()
                                self.alarm = False
                                self.snoozing = False
                                self.snooze_over = False
                            else:
                                self.alarm = True
                    elif event.key == pygame.K_s:
                        if self.beep:
                            self.snooze_timer.reset()
                            self.alarm = False
                            self.snoozing = True
                            self.beep = False
                            self.snooze_over = False
                            self.beeping.stop()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.key_left = True
                    self.first_press = True
                    self.key_timer.reset()
                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    self.key_left = False
            if self.key_left and self.key_timer.get_time() >= 0.2:
                self.alarm_hand.rotate()
                self.key_timer.reset()
            if self.key_left and self.first_press:
                self.alarm_hand.rotate()
                self.first_press = False
            if self.snoozing and self.snooze_timer.get_time() > 300 and not self.beep:
                self.snooze_over = True
                self.beep = True
                self.beeping.play(-1)
            self.hour_hand.update()
            self.minute_hand.update()
            self.second_hand.update()
            self.width = pygame.display.Info().current_w
            self.height = pygame.display.Info().current_h
            if self.hour_hand.angle == self.alarm_hand.angle:
                if self.alarm and not self.beep:
                    self.beep = True
                    self.beeping.play(-1)
            if not self.alarm and not self.snoozing:
                self.beep = False
                self.beeping.stop()
            self.screen.fill((255, 239, 201))
            pygame.draw.circle(self.screen, (255, 255, 255), [self.width // 2, self.height // 2], 154, 0)
            pygame.draw.circle(self.screen, (66, 128, 215), [self.width // 2, self.height // 2], 176, 22)
            self.screen.blit(self.label, (self.width // 2 - 149, self.height // 2 - 150))
            current_time = time.localtime()
            date = self.week[current_time.tm_wday] + "," + str(current_time.tm_year) + "," + str(
                current_time.tm_mon) + "," + str(current_time.tm_mday)
            self.screen.blit(
                self.font2.render("Press space to turn on/off the alarm.", True, (0, 0, 0), (255, 239, 201)), (10, 0))
            self.screen.blit(self.font2.render("Press 's' to snooze.", True, (0, 0, 0), (255, 239, 201)), (10, 15))
            self.screen.blit(self.font1.render(date, True, (0, 0, 0), (255, 255, 255)),
                             (self.width // 2 - self.font1.size(date)[0] // 2, self.height // 2 + 65))
            if self.snoozing and not self.snooze_over:
                self.screen.blit(self.font1.render("Alarm:Snoozing", True, (0, 0, 0), (255, 239, 201)),
                                 (10, self.height - self.font1.size("Alarm:Snoozing")[1]))
            elif self.snooze_over:
                self.screen.blit(self.font1.render("Alarm:On", True, (0, 0, 0), (255, 239, 201)),
                                 (10, self.height - self.font1.size("Alarm:On")[1]))
            else:
                self.screen.blit(self.font1.render(self.alarm_state[self.alarm], True, (0, 0, 0), (255, 239, 201)),
                                 (10, self.height - self.font1.size(self.alarm_state[self.alarm])[1]))
            pygame.draw.line(self.screen, (155, 155, 155), (self.width // 2, self.height // 2), (
                int(self.width // 2 + (60 * math.cos((-self.alarm_hand.angle - 90) / (180 / math.pi)))),
                int(self.height // 2 + (60 * math.sin((-self.alarm_hand.angle - 90) / (180 / math.pi))))), 3)
            pygame.draw.line(self.screen, (0, 0, 0), (self.width // 2, self.height // 2), (
                int(self.width // 2 + (80 * math.cos((-self.hour_hand.angle - 90) / (180 / math.pi)))),
                int(self.height // 2 + (80 * math.sin((-self.hour_hand.angle - 90) / (180 / math.pi))))), 3)
            pygame.draw.line(self.screen, (80, 255, 0), (self.width // 2, self.height // 2), (
                int(self.width // 2 + (130 * math.cos((-self.minute_hand.angle - 90) / (180 / math.pi)))),
                int(self.height // 2 + (130 * math.sin((-self.minute_hand.angle - 90) / (180 / math.pi))))), 3)
            pygame.draw.line(self.screen, (230, 0, 0), (self.width // 2, self.height // 2), (
                int(self.width // 2 + (150 * math.cos((-self.second_hand.angle - 90) / (180 / math.pi)))),
                int(self.height // 2 + (150 * math.sin((-self.second_hand.angle - 90) / (180 / math.pi))))), 2)
            pygame.draw.circle(self.screen, (216, 127, 0), [self.width // 2, self.height // 2], 5, 0)
            if self.full_screen:
                self.screen.blit(self.exit_fullscreen_icon, (self.width - 28, self.height - 28))
            else:
                self.screen.blit(self.enter_fullscreen_icon,
                                 (self.width - 28, self.height - 28))
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Main()
