# Anuneet Anand
# 2018022
# DIP Assignment 1

import cv2
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)

def bilinear_interpolate(img, c):
    ''' Performs Bilinear Interpolation
        img : Image to be Interpolated
        c : Interpolation Factor
    '''
    m,n = int(img.shape[0]*c),int(img.shape[1]*c)
    org = np.pad(img,1,'constant')[1:,1:]
    new = np.zeros((m,n))
    
    for i in range(m):
        for j in range(n):
            x,y = i/c,j/c

            if int(x)!=x or x == 0:
                x1, x2 = int(x), int(x)+1
            else:
                x1, x2 = int(x)-1, int(x)

            if int(y)!=y or y == 0:
                y1, y2 = int(y), int(y)+1
            else:
                y1, y2 = int(y)-1, int(y)

            V = np.array([ [x1,y1,x1*y1,1], [x1,y2,x1*y2,1], [x2,y1,x2*y1,1], [x2,y2,x2*y2,1]])
            Y = np.array([org[x1][y1], org[x1][y2], org[x2][y1], org[x2][y2]])
            Vi = np.linalg.pinv(V)
            A = np.dot(Vi,Y)

            new[i][j] = np.dot([x,y,x*y,1],A)
    
    return new

def translate(tx = 0, ty = 0):
    ''' Returns Transformation Matrix for Translation
        tx : Translation along x
        ty : Translation along y
    '''
    T = np.array([[1, 0, 0],[0, 1, 0],[tx, ty, 1]])
    return T

def scale(sx = 1, sy = 1):
    ''' Returns Transformation Matrix for Scaling
        sx : Scaling Factor along x
        sy : Scaling Factor along y
    '''
    T = np.array([[sx, 0, 0],[0, sy, 0],[0, 0, 1]])
    return T

def rotate(theta = 0):
    ''' Returns Transformation Matrix for Rotation
        theta : Rotation angle in degrees
    '''
    o = (np.pi*theta)/180
    T = np.array([[np.cos(o), -np.sin(o), 0],[np.sin(o), np.cos(o), 0 ],[0, 0, 1 ]])
    return T

def transformation(org, T):
    ''' Performs Geometric Transformation on Image
        org : Image
        T : Transformation Matrix
    '''

    size = len(org)
    new = np.zeros(org.shape)
    ox, oy = (size//2,size//2)
    Ti = np.linalg.pinv(T)

    for i in range(size):
        for j in range(size):
            x, y, z = np.array([i-ox, j-oy, 1]).dot(Ti)
            x, y = x+ox, y+oy

            if int(x)!=x or x == 0:
                x1,x2 = int(x), int(x)+1
            else:
                x1,x2 = int(x)-1, int(x)

            if int(y)!=y or y == 0:
                y1,y2 = int(y), int(y)+1
            else:
                y1,y2 = int(y)-1, int(y)

            if 0<=x1 and x2<size and 0<=y1 and y2<size:

                V = np.array([ [x1,y1,x1*y1,1], [x1,y2,x1*y2,1], [x2,y1,x2*y1,1], [x2,y2,x2*y2,1]])
                Y = np.array([org[x1][y1], org[x1][y2], org[x2][y1], org[x2][y2]])
                Vi = np.linalg.pinv(V)
                A = np.dot(Vi,Y)
                
                new[i][j] = np.dot([x,y,x*y,1],A)

    return new

# Solution for Q3
def A():

    print("-"*100)
    print(">>> Q3")
    print("-"*100)

    src = "AnuneetAnand_2018022_Image_512x512.bmp"
    c = 2
    org = cv2.imread(src,0)
    new = bilinear_interpolate(org,c)
    
    plt.figure()
    plt.title("Original Image")
    plt.imshow(org)
    plt.gray()

    plt.figure()
    plt.title("Interpolated Image"+" [ Interpolation Factor = "+str(c)+"] ")
    plt.imshow(new)
    plt.gray()

# Solution for Q4
def B():

    print("-"*100)
    print(">>> Q4")
    print("-"*100)

    src = "AnuneetAnand_2018022_Image_64x64.jpg"
    img = cv2.imread(src,0)

    size = 500
    org = np.zeros((size,size))
    ox, oy = (size//2,size//2)
    m,n = img.shape

    for i in range(m):
        for j in range(n):
            org[ox+i][oy+j]=img[i][j]

    T = np.matmul(np.matmul(rotate(45),scale(2,2)),translate(30,30))
    new = transformation(org,T)

    print("Transformation Matrix T")
    print(T)

    plt.figure()
    plt.title("Original Image")
    plt.imshow(org, extent=[-size//2,size//2,-size//2,size//2])
    plt.gray()

    plt.figure()
    plt.title("Image after Geometric Transformation")
    plt.imshow(new, extent=[-size//2,size//2,-size//2,size//2])
    plt.gray()

# Solution for Q5
def C():

    print("-"*100)
    print(">>> Q5")
    print("-"*100)

    src = "AnuneetAnand_2018022_Image_64x64.jpg"
    img = cv2.imread(src,0)

    size = 500
    I = np.zeros((size,size))
    ox, oy = (size//2,size//2)
    m,n = img.shape

    for i in range(m):
        for j in range(n):
            I[ox+i][oy+j]=img[i][j]

    T = np.matmul(np.matmul(rotate(45),scale(2,2)),translate(30,30))
    O = transformation(I,T)

    PI = np.array([[0,0,1],[0,63,1],[63,0,1],[63,63,1]])
    PO = np.array([[30,30,1],[119,119,1],[120,-60,1],[208,30,1]])

    Z = np.matmul(np.linalg.pinv((PI.T)@PI)@(PI.T),PO) 
    R = transformation(O,np.linalg.pinv(Z))

    print("Transformation Matrix Z")
    print(Z)

    plt.figure()
    plt.title("Reference Image (I)")
    plt.imshow(I, extent=[-size//2,size//2,-size//2,size//2])
    plt.gray()

    plt.figure()
    plt.title("Unregistered Input Image (O)")
    plt.imshow(O, extent=[-size//2,size//2,-size//2,size//2])
    plt.gray()

    plt.figure()
    plt.title("Registered Image (R)")
    plt.imshow(R, extent=[-size//2,size//2,-size//2,size//2])
    plt.gray()


if __name__ == '__main__':
    A()
    B()
    C()
    plt.show()
