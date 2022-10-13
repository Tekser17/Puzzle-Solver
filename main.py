import copy
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from settings import PASSWORD, NAME

global_field = list()


def main():
    EXE_PATH = r'E:\driver\yandexdriver.exe'
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=EXE_PATH, options=chr_options)
    driver.set_window_size(1440, 900)
    autorization(driver)
    driver.get('http://www.hacker.org/coil/index.php')
    while True:
        field = driver.find_element(By.ID, 'coilgame_inner')
        st = field.get_attribute('style')
        cells = field.find_elements(By.CLASS_NAME, 'cell')
        sz = take_sizes(st, len(cells))
        width = sz[0]
        height = sz[1]
        f = make_field(cells, width)
        paths = find_path(f, height, width)
        with open('all_pathes.txt', 'w') as file:
            #file.write('')
            json.dump(paths, file)
        print(paths[0])
        solve_puzzle(driver, paths[0])
        time.sleep(0.5)



def autorization(driver):
    driver.get('http://www.hacker.org/forum/login.php')
    login = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    auth = driver.find_element(By.NAME, 'login')
    login.send_keys(NAME)
    password.send_keys(PASSWORD)
    auth.click()


def solve_puzzle(driver, settings):
    path = settings[0]
    x = settings[1]
    y = settings[2]
    field = driver.find_element(By.ID, 'coilgame_inner')
    st = field.get_attribute('style')
    cells = field.find_elements(By.CLASS_NAME, 'cell')
    sz = take_sizes(st, len(cells))
    width = sz[0]
    height = sz[1]
    position = x * width + y
    cells[position].click()
    global global_field
    f = copy.deepcopy(global_field)
    f[x][y] = 1
    for i in path:
        if i == 'R':
            while y + 1 < width and f[x][y + 1] == 0:
                y += 1
                f[x][y] = 1
            position = x * width + y
            cells[position].click()
        if i == 'D':
            while x + 1 < height and f[x + 1][y] == 0:
                x += 1
                f[x][y] = 1
            position = x * width + y
            cells[position].click()
        if i == 'L':
            while y - 1 >= 0 and f[x][y - 1] == 0:
                y -= 1
                f[x][y] = 1
            position = x * width + y
            cells[position].click()
        if i == 'U':
            while x - 1 >= 0 and f[x - 1][y] == 0:
                x -= 1
                f[x][y] = 1
            position = x * width + y
            cells[position].click()
    continue_button = driver.find_element(By.ID, 'coilcontinue')
    continue_button.click()


def take_sizes(st, ln):
    width = ''
    height = 0
    for i in range(st.find('repeat(') + 7, len(st)):
        if st[i] == ',':
            break
        else:
            width += st[i]
    width = int(width)
    height = ln // width
    return [width, height]


def make_field(cells, width):
    f = list()
    q = list()
    for i in range(len(cells)):
        cell = cells[i]
        cell_type = cell.get_attribute('class')
        is_blocked = 0
        if 'blocked' in cell_type:
            is_blocked = 1
        q.append(is_blocked)
        if (i + 1) % width == 0:
            f.append(q)
            q = []
    global global_field
    global_field = copy.deepcopy(f)
    return f


def find_path(f, height, width):
    query = list()
    sum = height * width
    cur_sum = 0
    for i in range(len(f)):
        for j in range(len(f[i])):
            if f[i][j] == 0:
                query.append([i, j])
            elif f[i][j] == 1:
                cur_sum += 1
    response = []
    for i in range(len(query)):
        global global_field
        q = copy.deepcopy(global_field)
        x = check_x_y_start(query[i][0], query[i][1], q, height, width, sum, cur_sum + 1)
        if x is not False:
            response.append([x, query[i][0], query[i][1]])
    return response


def check_x_y_start(start_x, start_y, f, height, width, required_sum, cur_sum):
    st = [[start_x, start_y, '', copy.deepcopy(f), cur_sum]]
    while len(st) > 0:
       # if start_y == 2 and start_x == 0 and st[0][2].find('LDRURDR') != -1:
        #    print(st[0])
        #    for i in st[0][3]:
        #        print(i)
        x = st[0][0]
        y = st[0][1]
        save_path = st[0][2]
        ff = st[0][3]
        current_sum = st[0][4]
        st.pop(0)
        # L - Left, U - Up, R - Right, D - Down
        path = save_path
        if can_to_go(x, y, 'L', ff, height, width):
            path += 'L'
            change_x = 0
            change_y = -1
            pre_field = copy.deepcopy(ff)
            c_sum = current_sum
            pre_field[x][y] = 1
            xx = x + change_x
            yy = y + change_y
            if check_range(xx, yy, height, width):
                while pre_field[xx][yy] == 0:
                    pre_field[xx][yy] = 1
                    xx += change_x
                    yy += change_y
                    c_sum += 1
                    if not check_range(xx, yy, height, width):
                        break
                if c_sum == required_sum:
                    return path
                xx -= change_x
                yy -= change_y
                st.append([xx, yy, path, pre_field, c_sum])
        path = save_path
        if can_to_go(x, y, 'U', ff, height, width):
            path += 'U'
            change_x = -1
            change_y = 0
            pre_field = copy.deepcopy(ff)
            c_sum = current_sum
            pre_field[x][y] = 1
            xx = x + change_x
            yy = y + change_y
            if check_range(xx, yy, height, width):
                while pre_field[xx][yy] == 0:
                    pre_field[xx][yy] = 1
                    xx += change_x
                    yy += change_y
                    c_sum += 1
                    if not check_range(xx, yy, height, width):
                        break
                if c_sum == required_sum:
                    return path
                xx -= change_x
                yy -= change_y
                st.append([xx, yy, path, pre_field, c_sum])
        path = save_path
        if can_to_go(x, y, 'R', ff, height, width):
            path += 'R'
            change_x = 0
            change_y = 1
            pre_field = copy.deepcopy(ff)
            c_sum = current_sum
            pre_field[x][y] = 1
            xx = x + change_x
            yy = y + change_y
            if check_range(xx, yy, height, width):
                while pre_field[xx][yy] == 0:
                    pre_field[xx][yy] = 1
                    xx += change_x
                    yy += change_y
                    c_sum += 1
                    if not check_range(xx, yy, height, width):
                        break
                if c_sum == required_sum:
                    return path
                xx -= change_x
                yy -= change_y
                st.append([xx, yy, path, pre_field, c_sum])
        path = save_path
        if can_to_go(x, y, 'D', ff, height, width):
            path += 'D'
            change_x = 1
            change_y = 0
            pre_field = copy.deepcopy(ff)
            c_sum = current_sum
            pre_field[x][y] = 1
            xx = x + change_x
            yy = y + change_y
            if check_range(xx, yy, height, width):
                while pre_field[xx][yy] == 0:
                    pre_field[xx][yy] = 1
                    xx += change_x
                    yy += change_y
                    c_sum += 1
                    if not check_range(xx, yy, height, width):
                        break
                if c_sum == required_sum:
                    return path
                xx -= change_x
                yy -= change_y
                st.append([xx, yy, path, pre_field, c_sum])
    return False


def can_to_go(x, y, z, f, height, width):
    xm = 0
    ym = 0
    if z == 'U':
        xm -= 1
    if z == 'D':
        xm += 1
    if z == 'L':
        ym -= 1
    if z == 'R':
        ym += 1
    x = x + xm
    y = y + ym
    if check_range(x, y, height, width) and f[x][y] == 0:
        return True
    else:
        return False


def check_range(x, y, height, width):
    res = True
    if x < 0 or x >= height:
        res = False
    if y < 0 or y >= width:
        res = False
    return res


if __name__ == "__main__":
    main()
