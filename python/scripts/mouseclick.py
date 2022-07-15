#! python3
# mouse click automation with user-defined numbers of mouse coordinates & clicks
# 1.0.0 1st stable release
import pyautogui, time

def main():
    numMouseCoor = input('Number of mouse target: ')
    numMouseCoor = int(numMouseCoor)

    mouseCoorList = []

    for i in range(numMouseCoor):
        if i == 0:
            print('Move your mouse to the 1st target')
        elif i == 1:
            print('Move your mouse to the 2nd target')
        elif i == 2:
            print('Move your mouse to the 3rd target')
        else:
            print(f'Move your mouse to the {i+1}th target')

        time.sleep(5)
        mouseCoor = pyautogui.position()
        print(f'Mouse coordinates saved: {mouseCoor}\n')
        mouseCoorList.append(mouseCoor)

    clickNum = input('Total Clicks: ')

    # click to activate the window
    pyautogui.click(mouseCoorList[0])

    for clickclick in range(int(clickNum)):
        for i in range(numMouseCoor):
            pyautogui.click(mouseCoorList[i])
            time.sleep(0.1)

    print('\nmouse click finished')

if __name__ == '__main__':
    main()
