import cv2
import numpy as np

def annotate(mergedname = 'merged_U0000_L0000', image = 'C:/Users/Anand/Desktop/Sai Anand Maringanti/toWeb\\public\\images\\embryo-d_lifeact_000\\embryo-d_lifeact_000_U0000_L0000.jpg', responses = 'C:/Users/Anand/Desktop/Sai Anand Maringanti/responses.txt'):
    cells = cv2.imread(image)[..., ::-1]

    lineList = [line.rstrip('\n') for line in open(responses)]
    li = lineList[0][lineList[0].find('[')+1:-1]
    newli = li.split(',')

    zerocells = 0*np.ones_like(cells)
    for i in range(0, len(newli), 2):
        #print(newli[i], newli[i+1])
        try:
            zerocells[int(newli[i]), int(newli[i+1])] = 255
        except:
            None
    zerocells = cv2.rotate(zerocells, cv2.ROTATE_90_CLOCKWISE)
    zerocells = cv2.flip(zerocells, 1)
    addedimg = cv2.add(zerocells, cells)

    cv2.imwrite('corrected/' + mergedname + '_annotation.jpg', zerocells)
    cv2.imwrite('corrected/' + mergedname + '.jpg', addedimg[..., ::-1])

  # Main method.
if __name__ == '__main__':
    annotate()