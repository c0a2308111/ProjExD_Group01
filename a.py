import os
import time
import random
import sys
import pygame as pg
import math

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def impulse(screen :pg.Surface) -> None:
    pass

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 1〜10までの加速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    kk_images = {
        (0, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 1),  # 上
        (0, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 1),    # 下
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1),    # 左
        (5, 0): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1), True, False),   # 右
        (5, -5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 1), True, False),# 右上
        (-5, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 1),   # 左下
        (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 1), # 左上
        (5, 5): pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 1), True, False),  # 右下
    }
    return kk_images.get(sum_mv, pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1))

def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    norm = math.sqrt(dx**2 + dy**2)
    if norm != 0:
        vx = dx / norm * 5
        vy = dy / norm * 5
    else:
        vx, vy = 0, 0
    return vx, vy

def gameover(screen: pg.Surface) -> None:
    font = pg.font.SysFont("msgothic", 80)
    text = font.render("留年確定", True, (255,0,0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(5000)

def draw_hp_gauge(screen: pg.Surface, hp: int) -> None:
    gauge_width = 200
    gauge_height = 20
    fill_width = int((hp / 100) * gauge_width)
    pg.draw.rect(screen, (255, 255, 255), (20, 20, gauge_width, gauge_height), 2)
    pg.draw.rect(screen, (0, 255, 0), (20, 20, fill_width, gauge_height))

def random_non_overlapping_position(kk_rct: pg.Rect, bomb_size: int) -> tuple[int,int]:
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        bomb_rct = pg.Rect(x - bomb_size//2, y - bomb_size//2, bomb_size, bomb_size)
        if not kk_rct.colliderect(bomb_rct):
            return (x, y)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()

    # HP初期値
    hp = 100

    # 爆弾を3つ用意
    bombs = []
    for i in range(3):
        bb_size = bb_imgs[0].get_width()  
        x, y = random_non_overlapping_position(kk_rct, bb_size)
        bb_rct = bb_imgs[0].get_rect()
        bb_rct.centerx = x
        bb_rct.centery = y
        vx, vy = +5, -5
        bombs.append({'rct': bb_rct, 'vx': vx, 'vy': vy})

    flash_counter = 0
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.fill((0,0,0))

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        current_kk_img = get_kk_img(tuple(sum_mv))
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 250フレームごとにサイズ・スピードアップ、一段階進んだ状態で開始するため+1
        idx = min(tmr // 250 + 1, 9)

        # 各爆弾処理
        for bomb in bombs:
            bb_rct = bomb['rct']
            vx = bomb['vx']
            vy = bomb['vy']

            bb_img = bb_imgs[idx]
            bb_acc = bb_accs[idx]
            avx = vx * bb_acc
            avy = vy * bb_acc
            bb_rct.move_ip(avx, avy)

            yoko, tate = check_bound(bb_rct)
            if not yoko:
                bomb['vx'] *= -1
            if not tate:
                bomb['vy'] *= -1

            screen.blit(bb_img, bb_rct)

            # 当たり判定（無敵中は受けない）
            if flash_counter == 0:
                kk_mask = pg.mask.from_surface(current_kk_img)
                bb_mask = pg.mask.from_surface(bb_img)
                offset = (bb_rct.x - kk_rct.x, bb_rct.y - kk_rct.y)
                if kk_mask.overlap(bb_mask, offset):
                    hp = max(hp - 10, 0)
                    # 爆弾再配置
                    new_bb_size = bb_img.get_width()
                    x, y = random_non_overlapping_position(kk_rct, new_bb_size)
                    bb_rct.centerx = x
                    bb_rct.centery = y
                    bomb['vx'] = +5
                    bomb['vy'] = -5
                    # 2秒間無敵
                    flash_counter = 100

        if hp <= 0:
            gameover(screen)
            return

        # 点滅(無敵)処理
        if flash_counter > 0:
            flash_counter -= 1
            if (flash_counter // 5) % 2 == 0:
                screen.blit(current_kk_img, kk_rct)
        else:
            screen.blit(current_kk_img, kk_rct)

        draw_hp_gauge(screen, hp)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
