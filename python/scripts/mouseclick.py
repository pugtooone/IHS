#! python3
# introduce pyinputplus for inter input validation
# 1.0.1 1st stable release
import pyautogui, time
import pyinputplus as pyin

def main():
    numMouseCoor = pyin.inputInt('Number of mouse target: ')

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

    clickNum = pyin.inputInt('Total Clicks: ')

    # click to activate the window
    pyautogui.click(mouseCoorList[0])

    for clickclick in range(clickNum):
        for i in range(numMouseCoor):
            pyautogui.click(mouseCoorList[i])
            time.sleep(0.1)

    print('\nmouse click finished')

if __name__ == '__main__':
    main()
