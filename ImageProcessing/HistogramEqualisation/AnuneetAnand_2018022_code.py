# Anuneet Anand
# 2018022
# DIP Assignment 2

import cv2
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)
np.random.seed(0)

# Solution for Q3
def A():

    src = "AnuneetAnand_2018022_Image.jpg"
    img = cv2.imread(src,0)
    m,n = img.shape
    z = 256

    h = np.array([(img==i).sum()/(m*n) for i in range(z)])
    
    c, H = 0, []
    for i in h:
        c+=i
        H.append(c)

    s = np.round(np.array(H)*(z-1))
    
    new = img.copy()
    for r in range(z):
        new[np.where(img==r)] = s[r]

    e = np.array([(new==i).sum()/(m*n) for i in range(z)])

    print(">>> Input Image")
    print(img)
    plt.figure()
    plt.title("Input Image")
    plt.imshow(img)
    plt.gray()
    
    print(">>> Normalized Histogram of Input Image")
    print(h)
    plt.figure()
    plt.title("Normalized Histogram of Input Image")
    plt.bar([i for i in range(z)],h)

    print(">>> Equalized Image")
    print(new)
    plt.figure()
    plt.title("Equalized Image")
    plt.imshow(new)
    plt.gray()

    print(">>> Normalized Histogram of Equalized Image")
    print(e)
    plt.figure()
    plt.title("Normalized Histogram of Equalized Image")
    plt.bar([i for i in range(z)],e)

# Solution for Q4
def B():
    
    src = "AnuneetAnand_2018022_Image.jpg"
    I = cv2.imread(src,0)
    m,n = I.shape
    z = 256

    gamma = 0.5
    T = np.round( (z-1) * ((I**gamma)/(I.max()**gamma)) )

    h = np.array([(I==i).sum()/(m*n) for i in range(z)])
    c, H = 0, []
    for i in h:
        c+=i
        H.append(c)
    H = np.array(H)
    
    g = np.array([(T==i).sum()/(m*n) for i in range(z)])
    c, G = 0, []
    for i in g:
        c+=i
        G.append(c)
    G = np.array(G)

    Val = np.array([np.argmin(abs(H[r]-G)) for r in range(z)])

    O = I.copy()
    for r in range(z):
        O[np.where(I==r)] = Val[r]

    f = np.array([(O==i).sum()/(m*n) for i in range(z)])

    print(">>> Input Image")
    print(I)
    plt.figure()
    plt.title("Input Image")
    plt.imshow(I)
    plt.gray()
    
    print(">>> Normalized Histogram of Input Image")
    print(h)
    plt.figure()
    plt.title("Normalized Histogram of Input Image")
    plt.bar([i for i in range(z)],h)

    print(">>> Target Image [ Gamma:"+str(gamma)+" ]")
    print(T)
    plt.figure()
    plt.title("Target Image [ Gamma:"+str(gamma)+" ]")
    plt.imshow(T)
    plt.gray()
    
    print(">>> Normalized Histogram of Target Image")
    print(g)
    plt.figure()
    plt.title("Normalized Histogram of Target Image")
    plt.bar([i for i in range(z)],g)

    print(">>> Matched Image")
    print(O)
    plt.figure()
    plt.title("Matched Image")
    plt.imshow(O)
    plt.gray()
    
    print(">>> Normalized Histogram of Matched Image")
    print(f)
    plt.figure()
    plt.title("Normalized Histogram of Matched Image")
    plt.bar([i for i in range(z)],f)

# Solution for Q5
def C():

    # M1 = np.random.randint(3,size = (3,3))
    # M2 = np.random.randint(3,size = (3,3))

    M1 = np.array([[1,1]])
    M2 = np.array([[1,1]])

    # M1 = np.array([[-1,2,-1],[3,0,1],[-2,1,2]])
    # M2 = np.array([[-1],[0],[1]])

    Ix, Iy = M1.shape
    Fx, Fy = M2.shape
    Ox, Oy = (Ix+Fx-1, Iy+Fy-1)

    I = np.pad(M1,((Fx-1,Fx-1),(Fy-1,Fy-1)),'constant')
    O = np.zeros((Ox,Oy),dtype="int")
    RF = np.rot90(M2,2)

    for i in range(Ox):
        for j in range(Oy):
            O[i][j] = (I[i:i+Fx,j:j+Fy] * RF).sum()
    
    print(">>> Input: ")
    print(M1)
    print(">>> Original Filter: ")
    print(M2)
    print(">>> Rotated Filter: ")
    print(RF)
    print(">>> Output: ")
    print(O)

if __name__ == '__main__':
    #A()
    #B()
    C()
    plt.show()
