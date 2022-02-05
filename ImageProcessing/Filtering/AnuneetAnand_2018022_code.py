# Anuneet Anand
# 2018022
# DIP Assignment 3

import cv2
import numpy as np
import scipy.signal as sps
import matplotlib.pyplot as plt
np.set_printoptions(suppress = True)
plt.rc('font', size = 8) 


def LogT(I):
    '''Performs Log Transformation on Image I
    '''
    return np.round((255)*(np.log(1+I)/np.log(1+I.max())))

def CenterT(I):
    ''' Performs Centering on Image I
    '''
    O = I.copy()
    x,y = I.shape
    for i in range(x):
        for j in range(y):
            O[i][j] *= (-1)**(i+j)
    return O

def ScaleT(I):
    ''' Applies Min Max Scaling on Image
    '''
    return np.round(((I-I.min())/(I.max()-I.min()))*255)

def Plot_Util(pos,img,title=""):
    '''Plots img as a subplot
    '''
    plt.subplot(pos)
    plt.gca().set_title(title)
    plt.imshow(img, cmap="gray")
    
def BW_Filter(d,n,x,y):
    ''' Returns a Butterworth filter of order n with cut-off d
    '''
    F = np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            c = ( (i-x//2)**2 + (j-y//2)**2 )**0.5
            F[i][j] = 1/( 1 + (c/d)**(2*n) )
    return F

def A(t):
    src = "AnuneetAnand_2018022_cameraman.jpg"
    img = cv2.imread(src,0).astype(np.float64)
    n,m = img.shape
    
    I = np.pad(img,((0,n),(0,m)),'constant')
    MS_I = LogT(np.abs(np.fft.fft2(I)))
    IC = CenterT(I)
    
    DFT_I = np.fft.fft2(IC)
    MS_IC = LogT(np.abs(DFT_I))

    DFT_F = BW_Filter(t,2,n*2,m*2)
    MS_F = LogT(np.abs(DFT_F))

    IDFT = np.fft.ifft2(DFT_I * DFT_F)
    OC = IDFT.real

    O = CenterT(OC)
    out = ScaleT(O[:n,:m]) 

    fig = plt.figure()
    fig.suptitle("Butterworth Filtering with Cut-Off : "+str(t), size=12)
    Plot_Util(241,img,'Input Image')
    Plot_Util(242,I,'Padded Input Image')
    Plot_Util(243,MS_I,'Magnitude Spectrum of \n Padded Input Image')
    Plot_Util(244,MS_IC,'Centered Magnitude Spectrum of \n Padded Input Image')
    Plot_Util(245,DFT_F,'Filter')
    Plot_Util(246,MS_F,'Magnitude Spectrum of Filter')
    Plot_Util(247,out,'Output Image')

def B():
    src = "AnuneetAnand_2018022_cameraman.jpg"
    img = cv2.imread(src,0).astype(np.float64)
    n,m = img.shape

    BF = (1/81) * np.ones((9,9))
    p,q = BF.shape

    I = np.pad(img,((0,p-1),(0,q-1)),'constant') 
    F = np.pad(BF,((0,n-1),(0,m-1)),'constant')

    DFT_I = np.fft.fft2(I)
    DFT_F = np.fft.fft2(F)
    IDFT_IF = np.fft.ifft2(DFT_I*DFT_F)
    O = IDFT_IF.real
    out = ScaleT(O)
    
    ref = sps.convolve2d(img,BF)

    fig = plt.figure()
    fig.suptitle("Convolution with 9x9 Box Filter",size=12)
    Plot_Util(131,img,"Input Image")
    Plot_Util(132,out,"Convolution Using DFT")
    Plot_Util(133,ref,"Convolution Using Spatial Convolution")

def C(t):
    src = "AnuneetAnand_2018022_noiseIm.jpg"
    img = cv2.imread(src,0).astype(np.float64)
    n,m = img.shape
    D = t*(n*2)

    I = np.pad(img,((0,n),(0,m)),'constant')
    IC = CenterT(I)
    DFT_I = np.fft.fft2(IC)
    MS_IC = LogT(np.abs(DFT_I))

    # Found by manually analysing MS_IC
    a = (192,192)
    b = (320,320)

    F = np.ones((n*2,m*2))
    for i in range(n*2):
        for j in range(m*2):
            d1 = ( (i-a[0])**2 + (j-a[1])**2 )**0.5
            d2 = ( (i-b[0])**2 + (j-b[1])**2 )**0.5
            if d1<D or d2<D: F[i][j] = 0
    
    OC = np.fft.ifft2(DFT_I*F).real
    O = CenterT(OC)
    out = ScaleT(O[:n,:m])

    ref = "AnuneetAnand_2018022_denoiseIm.jpg"
    org = cv2.imread(ref,0).astype(np.float64)

    fig = plt.figure()
    fig.suptitle("Image Denoising", size=12)
    Plot_Util(331,img,"Noisy Image")
    Plot_Util(332,MS_IC,"Centered Magnitude Spectrum of \n Padded Noisy Image")
    Plot_Util(333,F,"Custom Filter")
    Plot_Util(334,out,"Denoised Image")
    Plot_Util(335,org,"Reference Image")

if __name__ == "__main__":
    A(10)
    A(30)
    A(60)
    B()
    C(0.05)
    plt.show()
